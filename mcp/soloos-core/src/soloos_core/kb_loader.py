"""
Knowledge Base Loader — Parses SoloOS markdown intelligence into structured Python data.

Parses at import time (once), cached in module-level globals.
No external dependencies. Pure stdlib.
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


# ─────────────────────────────────────────────────────────────
# Locate knowledge-base root (walk up from this file)
# ─────────────────────────────────────────────────────────────

def _find_kb_root() -> Path:
    """Walk up directory tree to find knowledge-base/ folder."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = current / "knowledge-base"
        if candidate.is_dir():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Fallback: assume running from repo root
    return Path.cwd() / "knowledge-base"


KB_ROOT = _find_kb_root()
CONTEXT_ROOT = KB_ROOT.parent / "context"


# ─────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────

@dataclass
class Pattern:
    id: str                    # P01, P02, ...
    name: str                  # "The Levels Test"
    category: str              # "PRODUCT DECISIONS"
    situation: str             # When to apply
    pattern: str               # The core rule
    real_example: str          # Evidence from real founders
    kill_signal: str           # What proves this wrong
    reversibility: str         # X/10 score
    apply_when: str = ""       # Additional trigger condition
    raw: str = ""              # Full raw text for fuzzy search

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k != "raw"}


@dataclass
class FounderCase:
    founder: str               # Pieter Levels, Marc Lou, etc.
    product: str               # Nomad List, ShipFast, etc.
    peak_mrr: str              # "$60K+ MRR"
    stage: str                 # The stage this applies to
    decision: str              # What they did
    outcome: str               # What happened
    pattern_id: str            # Linked pattern (P01, etc.)
    tags: list[str] = field(default_factory=list)
    raw: str = ""


@dataclass
class MarketCategory:
    name: str
    saturation: str            # "Dead" / "Saturated" / "Viable-with-niche" / "Open" / "Emerging"
    signal: str                # Evidence for saturation level
    gross_margin: str          # "85-90%"
    ltv_cac: str               # "4-8x"
    churn_monthly: str         # "2-5%"
    notes: str = ""
    raw: str = ""


# ─────────────────────────────────────────────────────────────
# PATTERN_LIBRARY.md parser
# ─────────────────────────────────────────────────────────────

def load_patterns() -> list[Pattern]:
    """Parse PATTERN_LIBRARY.md into structured Pattern objects."""
    path = KB_ROOT / "PATTERN_LIBRARY.md"
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    patterns = []

    # Split on pattern headers: ### P01 — Name
    # Also handles: ### P01 — Name\n or ### P36 (Validated...)
    blocks = re.split(r"\n(?=### P\d+)", text)

    current_category = "GENERAL"
    category_re = re.compile(r"^## CATEGORY\s+\w+:\s*(.+)$", re.MULTILINE)

    # Track categories from the full text
    cat_positions = [(m.start(), m.group(1).strip()) for m in category_re.finditer(text)]

    for block in blocks:
        header_match = re.match(r"### (P\d+)\s*[—–-]+\s*(.+)", block.strip())
        if not header_match:
            continue

        pid = header_match.group(1).strip()
        pname = header_match.group(2).strip()

        # Determine category based on position in original text
        block_pos = text.find(f"### {pid}")
        current_category = "GENERAL"
        for pos, cat in cat_positions:
            if pos < block_pos:
                current_category = cat
            else:
                break

        def extract_field(block: str, *labels: str) -> str:
            for label in labels:
                # Try bold label: **Label**: value
                m = re.search(
                    rf"\*\*{re.escape(label)}\*\*:?\s*(.+?)(?=\n\*\*|\n###|\Z)",
                    block, re.DOTALL
                )
                if m:
                    return m.group(1).strip()
                # Try plain: Label: value
                m = re.search(
                    rf"^{re.escape(label)}:?\s*(.+?)(?=\n[A-Z]|\n###|\Z)",
                    block, re.DOTALL | re.MULTILINE
                )
                if m:
                    return m.group(1).strip()
            return ""

        situation = extract_field(block, "Situation", "Apply when", "When")
        pattern = extract_field(block, "Pattern", "Rule")
        example = extract_field(block, "Real example", "Evidence", "Real examples", "Numbers")
        kill_signal = extract_field(block, "Kill signal")
        reversibility = extract_field(block, "Reversibility")
        apply_when = extract_field(block, "Apply when", "Apply")

        # Fallback: grab all text after header as pattern if nothing parsed
        if not pattern:
            lines = block.strip().split("\n")[1:]
            pattern = " ".join(l.strip() for l in lines[:3] if l.strip())

        patterns.append(Pattern(
            id=pid,
            name=pname,
            category=current_category,
            situation=situation or apply_when,
            pattern=pattern,
            real_example=example,
            kill_signal=kill_signal,
            reversibility=reversibility,
            apply_when=apply_when,
            raw=block.strip(),
        ))

    return patterns


# ─────────────────────────────────────────────────────────────
# FOUNDER_INTELLIGENCE.md parser
# ─────────────────────────────────────────────────────────────

_KNOWN_FOUNDERS = [
    "Pieter Levels", "Marc Lou", "Tony Dinh", "Danny Postma",
    "Arvid Kahl", "Adam Wathan", "Jon Yongfook", "Justin Welsh",
    "Daniel Vassallo", "Nathan Barry", "Danielle Simpson",
    "Justin Jackson", "Tyler Tringas", "Andrew Gazdecki",
    "Arjun Jain", "Andrey Azimov", "Josh Pigford",
]

_KNOWN_PRODUCTS = [
    "Nomad List", "PhotoAI", "ShipFast", "HeadshotPro", "FeedbackPanda",
    "SiteGPT", "DevUtils", "BlackMagic", "Xnapper", "Tailwind UI",
    "Remote OK", "Hackerpreneur", "Hype Fury", "Tweet Hunter",
    "Supercreator", "MicroAcquire", "Baremetrics",
]


def load_founder_cases() -> list[FounderCase]:
    """Extract founder case studies from FOUNDER_INTELLIGENCE.md."""
    path = KB_ROOT / "FOUNDER_INTELLIGENCE.md"
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    cases = []

    # Extract paragraphs that contain founder names + revenue figures
    mrr_pattern = re.compile(r"\$[\d,]+K?\+?\s*MRR", re.IGNORECASE)
    evidence_blocks = re.findall(
        r"\*\*Evidence\*\*:(.+?)(?=\n\*\*|\n###|\n---|\Z)", text, re.DOTALL
    )

    for block in evidence_blocks:
        block = block.strip()
        if not block:
            continue

        # Find founders mentioned
        founders_mentioned = [f for f in _KNOWN_FOUNDERS if f in block]
        products_mentioned = [p for p in _KNOWN_PRODUCTS if p in block]

        # Find MRR figures
        mrr_matches = mrr_pattern.findall(block)

        # Find linked pattern (look backwards in text for Px context)
        block_pos = text.find(block[:50])
        # Check preceding lines for ### X. pattern or P0x reference
        preceding = text[max(0, block_pos - 500):block_pos]
        pattern_match = re.search(r"P(\d+)", preceding)
        pattern_id = f"P{pattern_match.group(1):>02}" if pattern_match else ""

        if founders_mentioned or products_mentioned:
            cases.append(FounderCase(
                founder=", ".join(founders_mentioned) or "Unknown",
                product=", ".join(products_mentioned) or "Unknown",
                peak_mrr=mrr_matches[0] if mrr_matches else "unknown",
                stage=_infer_stage(block),
                decision=_extract_decision(block),
                outcome=_extract_outcome(block),
                pattern_id=pattern_id,
                tags=_extract_tags(block),
                raw=block,
            ))

    # Deduplicate by founder+product
    seen = set()
    unique = []
    for c in cases:
        key = (c.founder, c.product)
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique


def _infer_stage(text: str) -> str:
    for marker, stage in [
        ("$50K", "$50K+ MRR"), ("$20K", "$20K+ MRR"),
        ("$5K", "$5K+ MRR"), ("$1K", "$1K+ MRR"),
    ]:
        if marker in text:
            return stage
    return "unknown"


def _extract_decision(text: str) -> str:
    # First sentence is usually the decision
    sentences = re.split(r"\. ", text.strip())
    return sentences[0].strip() if sentences else text[:200]


def _extract_outcome(text: str) -> str:
    # Look for outcome indicators
    m = re.search(r"(reached|hit|grew|achieved|result|outcome).{0,200}", text, re.IGNORECASE)
    if m:
        return m.group(0)[:200]
    sentences = re.split(r"\. ", text.strip())
    return sentences[-1].strip() if len(sentences) > 1 else ""


def _extract_tags(text: str) -> list[str]:
    tags = []
    tag_map = {
        "distribution": ["distribution", "audience", "twitter", "HN", "reddit"],
        "pricing": ["price", "pricing", "MRR", "$"],
        "community": ["community", "Facebook group", "Slack", "Discord"],
        "seo": ["SEO", "programmatic", "organic", "keyword"],
        "compliance": ["compliance", "regulatory", "GDPR", "HIPAA"],
        "ai_product": ["AI", "GPT", "LLM", "headshot", "generate"],
        "b2b": ["B2B", "enterprise", "SMB", "business"],
        "b2c": ["B2C", "consumer", "individual"],
    }
    for tag, keywords in tag_map.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            tags.append(tag)
    return tags


# ─────────────────────────────────────────────────────────────
# MARKET_INTELLIGENCE.md parser
# ─────────────────────────────────────────────────────────────

def load_market_categories() -> list[MarketCategory]:
    """Parse market category saturation and unit economics from MARKET_INTELLIGENCE.md."""
    path = KB_ROOT / "MARKET_INTELLIGENCE.md"
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    categories = []

    # Map section headers to saturation labels
    section_saturation_map = {
        "Dead on Arrival": "Dead",
        "Dead": "Dead",
        "Heavily Saturated": "Saturated",
        "Saturated": "Saturated",
        "Viable with Niche": "Viable-with-niche",
        "Viable-with-niche": "Viable-with-niche",
        "Open / Under-Served": "Open",
        "Open": "Open",
        "Emerging": "Emerging",
    }

    # Split into sections
    sections = re.split(r"\n###\s+", text)
    current_saturation = "Unknown"

    for section in sections:
        if not section.strip():
            continue

        # Determine saturation from section header
        header_line = section.split("\n")[0].strip()
        for key, sat in section_saturation_map.items():
            if key.lower() in header_line.lower():
                current_saturation = sat
                break

        # Parse table rows in this section
        rows = re.findall(r"^\|(.+)\|$", section, re.MULTILINE)
        for row in rows:
            cells = [c.strip() for c in row.split("|")]
            cells = [c for c in cells if c and c != "---" and not re.match(r"^-+$", c)]

            if not cells:
                continue

            name = cells[0].strip("* ")  # Remove bold markdown

            # Skip header rows
            skip_words = ["category", "market", "differentiation", "signal", "why", "reason", "who killed"]
            if any(name.lower().startswith(w) for w in skip_words):
                continue
            if len(name) < 3:
                continue

            # Second cell = signal/reason/differentiation
            signal = cells[1] if len(cells) > 1 else ""
            notes = cells[2] if len(cells) > 2 else ""

            categories.append(MarketCategory(
                name=name,
                saturation=current_saturation,
                signal=signal,
                gross_margin="",
                ltv_cac="",
                churn_monthly="",
                notes=notes,
                raw=row,
            ))

    # Also extract unit economics from the UE table if present
    ue_section = re.search(r"Unit Economics by Category(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if ue_section:
        ue_text = ue_section.group(1)
        for m in re.finditer(r"\|\s*([^|]+?)\s*\|\s*([\d-]+%)\s*\|\s*([\d-]+x)\s*\|\s*([\d-]+%)", ue_text):
            cat_name = m.group(1).strip()
            # Try to match to existing category
            for cat in categories:
                if cat_name.lower() in cat.name.lower() or cat.name.lower() in cat_name.lower():
                    cat.gross_margin = m.group(2)
                    cat.ltv_cac = m.group(3)
                    cat.churn_monthly = m.group(4)
                    break

    # Deduplicate by name
    seen = set()
    unique = []
    for c in categories:
        if c.name not in seen:
            seen.add(c.name)
            unique.append(c)

    return unique


def _find_percent(text: str, keyword: str) -> str:
    m = re.search(
        rf"{keyword}[^:]*:\s*([\d]{{1,3}}-[\d]{{1,3}}%|[\d]{{1,3}}%)",
        text, re.IGNORECASE
    )
    return m.group(1) if m else ""


def _find_ratio(text: str, *keywords: str) -> str:
    for kw in keywords:
        m = re.search(
            rf"{kw}[^:]*:\s*([\d]+-[\d]+x|[\d]+x)",
            text, re.IGNORECASE
        )
        if m:
            return m.group(1)
    return ""


# ─────────────────────────────────────────────────────────────
# Semantic search (keyword-based, no external embeddings)
# ─────────────────────────────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """Lower-case word tokens for matching."""
    return set(re.findall(r"\b\w{3,}\b", text.lower()))


def search_patterns(query: str, patterns: list[Pattern], top_n: int = 5) -> list[Pattern]:
    """Return top_n patterns most relevant to the query (keyword overlap scoring)."""
    query_tokens = _tokenize(query)
    if not query_tokens:
        return patterns[:top_n]

    scored = []
    for p in patterns:
        search_text = f"{p.name} {p.situation} {p.pattern} {p.apply_when} {p.raw}"
        p_tokens = _tokenize(search_text)
        overlap = len(query_tokens & p_tokens)
        # Bonus for ID match (e.g., "P07" in query)
        if p.id.lower() in query.lower():
            overlap += 20
        # Bonus for name match
        if any(word in p.name.lower() for word in query_tokens if len(word) > 4):
            overlap += 5
        scored.append((overlap, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for score, p in scored[:top_n] if score > 0]


def search_founders(query: str, cases: list[FounderCase], top_n: int = 5) -> list[FounderCase]:
    """Return top_n founder cases most relevant to the query."""
    query_tokens = _tokenize(query)
    if not query_tokens:
        return cases[:top_n]

    scored = []
    for c in cases:
        search_text = f"{c.founder} {c.product} {c.decision} {c.outcome} {' '.join(c.tags)} {c.raw}"
        c_tokens = _tokenize(search_text)
        overlap = len(query_tokens & c_tokens)
        if c.founder.lower() in query.lower():
            overlap += 15
        if c.product.lower() in query.lower():
            overlap += 10
        scored.append((overlap, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for score, c in scored[:top_n] if score > 0]


# ─────────────────────────────────────────────────────────────
# Module-level cache (loaded once on import)
# ─────────────────────────────────────────────────────────────

_PATTERNS: list[Pattern] = []
_FOUNDERS: list[FounderCase] = []
_MARKETS: list[MarketCategory] = []
_LOADED = False


def ensure_loaded() -> None:
    global _PATTERNS, _FOUNDERS, _MARKETS, _LOADED
    if _LOADED:
        return
    _PATTERNS = load_patterns()
    _FOUNDERS = load_founder_cases()
    _MARKETS = load_market_categories()
    _LOADED = True


def get_patterns() -> list[Pattern]:
    ensure_loaded()
    return _PATTERNS


def get_founders() -> list[FounderCase]:
    ensure_loaded()
    return _FOUNDERS


def get_markets() -> list[MarketCategory]:
    ensure_loaded()
    return _MARKETS
