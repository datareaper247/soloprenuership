"""
Log Manager — Read/write founder-log.md, context files, and kill signal tracking.

All file operations are atomic (write to temp, then rename).
"""

import re
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional

from .kb_loader import _find_kb_root

KB_ROOT = _find_kb_root()
CONTEXT_ROOT = KB_ROOT.parent / "context"
FOUNDER_LOG_PATH = KB_ROOT / "personal" / "founder-log.md"
BUSINESS_CONTEXT_PATH = CONTEXT_ROOT / "business-context.md"
EXPERIMENT_LOG_PATH = CONTEXT_ROOT / "experiment-log.md"
DECISION_LOG_PATH = CONTEXT_ROOT / "decision-log.md"
CUSTOMER_VOICE_PATH = CONTEXT_ROOT / "customer-voice.md"


# ─────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────

@dataclass
class FounderLogEntry:
    id: str                         # FL-001
    date: str                       # 2026-03-22
    type: str                       # Decision / Experiment / Pivot
    summary: str                    # One sentence
    context: str                    # What prompted this
    pattern_applied: str            # P-07, etc.
    hypothesis: str                 # Expected outcome
    kill_signal: str                # What would prove it wrong
    kill_signal_due: str            # Due date (YYYY-MM-DD)
    outcome: str                    # PENDING OUTCOME / result text
    outcome_due: str                # YYYY-MM-DD
    outcome_status: str             # ⏳ Pending / ✅ Confirmed / ❌ Invalidated / 🔄 Partial

    def is_overdue(self) -> bool:
        if self.outcome_status != "⏳ Pending":
            return False
        try:
            due = datetime.strptime(self.outcome_due, "%Y-%m-%d")
            return datetime.now() > due
        except Exception:
            return False

    def days_overdue(self) -> int:
        try:
            due = datetime.strptime(self.outcome_due, "%Y-%m-%d")
            delta = datetime.now() - due
            return max(0, delta.days)
        except Exception:
            return 0

    def days_until_kill_signal(self) -> Optional[int]:
        try:
            due = datetime.strptime(self.kill_signal_due, "%Y-%m-%d")
            delta = due - datetime.now()
            return delta.days
        except Exception:
            return None

    def to_markdown(self) -> str:
        return f"""---
**[[{self.id}]]**
- **Date:** {self.date}
- **Type:** {self.type}
- **Summary:** {self.summary}
- **Context:** {self.context}
- **Pattern applied:** {self.pattern_applied}
- **Hypothesis:** {self.hypothesis}
- **Kill signal set:** {self.kill_signal}
- **Kill signal due:** {self.kill_signal_due}
- **Outcome:** {self.outcome}
- **Outcome due:** {self.outcome_due}
- **Outcome status:** {self.outcome_status}

"""


# ─────────────────────────────────────────────────────────────
# Parse founder-log.md
# ─────────────────────────────────────────────────────────────

def parse_log_entries(text: str) -> list[FounderLogEntry]:
    """Parse markdown founder-log entries into FounderLogEntry objects."""
    entries = []

    # Split on --- separator between entries
    # Each entry starts with **[[FL-XXX]]**
    entry_pattern = re.compile(r"\*\*\[\[FL-(\d+)\]\]\*\*(.+?)(?=\*\*\[\[FL-\d+\]\]\*\*|\Z)", re.DOTALL)

    for m in entry_pattern.finditer(text):
        num = m.group(1)
        block = m.group(2)

        def get_field(label: str, fallback: str = "") -> str:
            match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n- \*\*|\Z)", block, re.DOTALL)
            return match.group(1).strip() if match else fallback

        entries.append(FounderLogEntry(
            id=f"FL-{num.zfill(3)}",
            date=get_field("Date"),
            type=get_field("Type"),
            summary=get_field("Summary"),
            context=get_field("Context"),
            pattern_applied=get_field("Pattern applied"),
            hypothesis=get_field("Hypothesis"),
            kill_signal=get_field("Kill signal set"),
            kill_signal_due=get_field("Kill signal due"),
            outcome=get_field("Outcome"),
            outcome_due=get_field("Outcome due"),
            outcome_status=get_field("Outcome status", "⏳ Pending"),
        ))

    return entries


def load_log() -> list[FounderLogEntry]:
    """Load all entries from founder-log.md."""
    if not FOUNDER_LOG_PATH.exists():
        return []
    text = FOUNDER_LOG_PATH.read_text(encoding="utf-8")
    return parse_log_entries(text)


def next_log_id(entries: list[FounderLogEntry]) -> str:
    """Return next FL-XXX id."""
    if not entries:
        return "FL-001"
    nums = [int(e.id.split("-")[1]) for e in entries]
    return f"FL-{max(nums) + 1:03d}"


def append_log_entry(entry: FounderLogEntry) -> None:
    """Append a new entry to founder-log.md (atomic write)."""
    FOUNDER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if FOUNDER_LOG_PATH.exists():
        text = FOUNDER_LOG_PATH.read_text(encoding="utf-8")
    else:
        text = _default_founder_log_header()

    marker = "<!-- YOUR ENTRIES START HERE -->"
    new_entry_md = entry.to_markdown()

    if marker in text:
        text = text.replace(marker, marker + "\n\n" + new_entry_md)
    else:
        text += "\n\n" + new_entry_md

    _atomic_write(FOUNDER_LOG_PATH, text)


def _default_founder_log_header() -> str:
    return """# Founder Log — Personal Pattern Accrual

> Auto-generated by SoloOS. Each entry = one decision with a hypothesis and kill signal.

---

## HOW TO READ THIS FILE

- `[PENDING OUTCOME]` = outcome not yet known
- `✅ CONFIRMED` = hypothesis validated
- `❌ INVALIDATED` = hypothesis wrong
- `🔄 PARTIAL` = partially right

---

## ENTRIES

<!-- YOUR ENTRIES START HERE -->

"""


# ─────────────────────────────────────────────────────────────
# Kill signal checker
# ─────────────────────────────────────────────────────────────

@dataclass
class KillSignalAlert:
    entry_id: str
    summary: str
    kill_signal: str
    due_date: str
    days_remaining: Optional[int]
    is_overdue: bool
    urgency: str          # "OVERDUE" / "URGENT" (≤7d) / "WARNING" (≤14d) / "OK"


def check_kill_signals(entries: list[FounderLogEntry]) -> list[KillSignalAlert]:
    """Check all pending entries for overdue or approaching kill signals."""
    alerts = []
    for e in entries:
        if e.outcome_status != "⏳ Pending":
            continue
        days = e.days_until_kill_signal()
        overdue = e.is_overdue()

        if days is None:
            continue

        if overdue or days < 0:
            urgency = "OVERDUE"
        elif days <= 7:
            urgency = "URGENT"
        elif days <= 14:
            urgency = "WARNING"
        else:
            urgency = "OK"

        alerts.append(KillSignalAlert(
            entry_id=e.id,
            summary=e.summary,
            kill_signal=e.kill_signal,
            due_date=e.kill_signal_due,
            days_remaining=days,
            is_overdue=days < 0,
            urgency=urgency,
        ))

    alerts.sort(key=lambda a: (
        {"OVERDUE": 0, "URGENT": 1, "WARNING": 2, "OK": 3}[a.urgency],
        a.days_remaining if a.days_remaining is not None else 999
    ))
    return alerts


# ─────────────────────────────────────────────────────────────
# Business context reader
# ─────────────────────────────────────────────────────────────

def read_business_context() -> dict:
    """Read business-context.md and extract key fields."""
    if not BUSINESS_CONTEXT_PATH.exists():
        return {"status": "not_found", "message": "No business-context.md found. Run /onboard."}

    text = BUSINESS_CONTEXT_PATH.read_text(encoding="utf-8")

    def extract(label: str) -> str:
        m = re.search(rf"\*?\*?{re.escape(label)}\*?\*?\s*:?\s*(.+?)(?=\n\*|\n#|\Z)", text, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip()[:300] if m else ""

    # Try to find MRR
    mrr_match = re.search(r"\$[\d,]+\s*(?:MRR|/mo|/month|ARR)", text, re.IGNORECASE)
    mrr = mrr_match.group(0) if mrr_match else ""

    return {
        "mrr": mrr,
        "icp": extract("ICP") or extract("Ideal Customer"),
        "stage": extract("Stage") or extract("Business stage"),
        "top_channel": extract("Top channel") or extract("Primary channel"),
        "biggest_challenge": extract("Biggest challenge") or extract("Key challenge"),
        "open_decisions": extract("Open decisions"),
        "raw_excerpt": text[:500],
    }


# ─────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────

def _atomic_write(path: Path, content: str) -> None:
    """Write content atomically using a temp file."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def due_date_str(days: int) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
