"""
SoloOS Core MCP Server — V10 Architecture

Thin router. Business logic lives in tools/*.py, data/*.py, core/*.py.
V10 additions: multi-tier caching, structlog observability, analyze_self,
Pydantic-validated data layer, tag-indexed KB.

Run: python -m soloos_core.server
Or:  uvx --from soloos-core soloos-mcp
"""

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Annotated

from mcp.server.fastmcp import FastMCP

# ── KB + log primitives (still used by inline tools) ───────────
from .kb_loader import (
    get_patterns, get_founders, get_markets,
    search_patterns, search_founders, KB_ROOT,
)
from .log_manager import (
    load_log, append_log_entry, check_kill_signals,
    read_business_context, next_log_id,
    FounderLogEntry, today_str, due_date_str,
)

# ── Module imports ──────────────────────────────────────────────
from .tools.memory import (
    get_stage_advice,
    session_synthesis,
    get_business_context,
    update_context,
    knowledge_base_stats,
    log_decision,
    check_kill_signals_tool,
    reject_if_overdue,
)
from .tools.decisions import (
    calculate_ev,
    validate_idea_gates,
    score_pmf,
    simulate_business_change,
    get_decision_intelligence_brief,
)
from .tools.financial import (
    calculate_unit_economics as _fn_unit_economics,
    calculate_runway as _fn_runway,
    calculate_valuation as _fn_valuation,
    get_stripe_mrr as _fn_stripe_mrr,
    get_mercury_runway as _fn_mercury_runway,
)
from .tools.agents import run_council_brief, ask_role_agent
from .tools.intelligence import (
    run_morning_intelligence,
    mine_pain_points as _fn_mine_pain,
    read_url_content,
    get_competitor_intel,
)
from .tools.decisions import _CAUSAL_CHAINS as _DECISION_CAUSAL_CHAINS

# ── V10: Data + Observability layers ────────────────────────────
from .data.cache import get_cache_stats, clear_all_cache, clear_cache_by_prefix
from .core.observability import get_log_stats
from .core.scheduler import (
    scheduler_status as _sched_status,
    scheduler_run_now as _sched_run_now,
    scheduler_configure as _sched_configure,
)
from .data.connectors.registry import get_registry as _get_connector_registry
from .data.growthbook_client import get_growthbook_client as _get_growthbook_client
from .core.observability import rate_tool_call as _rate_tool_call


# ─────────────────────────────────────────────────────────────
# Server init
# ─────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="soloos-core",
    instructions="""
You are the SoloOS Core intelligence server. You provide structured founder intelligence
to Claude Code, allowing Claude to query real founder data, decision patterns, market intelligence,
and kill signal tracking instead of relying on static markdown references.

Always return structured JSON that Claude can reason over. Be specific, not generic.
When patterns match, cite the real founder evidence. When EV is calculated, show the math.
""",
)


# ─────────────────────────────────────────────────────────────
# Register tools from tools/memory.py  (return str — direct)
# ─────────────────────────────────────────────────────────────

mcp.tool()(get_stage_advice)
mcp.tool()(session_synthesis)
mcp.tool()(get_business_context)
mcp.tool()(update_context)
mcp.tool()(knowledge_base_stats)
mcp.tool()(log_decision)
mcp.tool()(check_kill_signals_tool)
mcp.tool()(reject_if_overdue)


# ─────────────────────────────────────────────────────────────
# Register tools from tools/decisions.py  (return str — direct)
# ─────────────────────────────────────────────────────────────

mcp.tool()(calculate_ev)
mcp.tool()(validate_idea_gates)
mcp.tool()(score_pmf)
mcp.tool()(simulate_business_change)
mcp.tool()(get_decision_intelligence_brief)


# ─────────────────────────────────────────────────────────────
# Financial tools — wrappers (tools/financial.py returns dict)
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_unit_economics(
    arpu: Optional[float] = None,
    churn_rate_monthly_pct: Optional[float] = None,
    cac: float = 0.0,
    gross_margin_pct: float = 85.0,
    expansion_mrr_pct: float = 0.0,
) -> str:
    """
    Calculate LTV, LTV:CAC, payback period, and net revenue retention.
    Returns full unit economics dashboard for a SaaS business.

    Zero-input when Stripe data is connected: arpu and churn are auto-filled
    from DuckDB (last-30-day charges / customer count). Provide manually
    when no Stripe sync is configured.

    Args:
        arpu: Average Revenue Per User per month ($). Auto-filled from Stripe if omitted.
        churn_rate_monthly_pct: Monthly churn rate as % (e.g. 5.0). Auto-filled from Stripe if omitted.
        cac: Customer Acquisition Cost ($, optional)
        gross_margin_pct: Gross margin percentage (default 85% for SaaS)
        expansion_mrr_pct: Monthly expansion MRR as % of base (e.g. 2.0 = 2%)
    """
    return json.dumps(_fn_unit_economics(
        arpu=arpu,
        churn_rate_monthly_pct=churn_rate_monthly_pct,
        cac=cac,
        gross_margin_pct=gross_margin_pct,
        expansion_mrr_pct=expansion_mrr_pct,
    ), indent=2)


@mcp.tool()
def calculate_runway(
    cash_on_hand: float,
    monthly_burn: float,
    mrr: Optional[float] = None,
    expected_mrr_growth_pct: float = 0.0,
) -> str:
    """
    Calculate true runway with MRR trajectory, break-even, and month-by-month projection.

    MRR is auto-filled from Stripe/DuckDB when omitted and data is connected.
    cash_on_hand and monthly_burn are always required (Mercury Phase C data).

    Args:
        cash_on_hand: Current bank balance ($)
        monthly_burn: Monthly operating expenses ($)
        mrr: Current MRR ($). Auto-filled from Stripe/DuckDB if omitted.
        expected_mrr_growth_pct: Expected MRR growth per month % (e.g. 10.0 = 10%)
    """
    return json.dumps(_fn_runway(
        cash_on_hand=cash_on_hand,
        monthly_burn=monthly_burn,
        mrr=mrr,
        expected_mrr_growth_pct=expected_mrr_growth_pct,
    ), indent=2)


@mcp.tool()
def calculate_valuation(
    mrr: float,
    growth_rate_monthly_pct: float = 0.0,
    churn_rate_monthly_pct: float = 5.0,
    nrr_pct: float = 100.0,
    model: str = "saas",
    profitable: bool = False,
) -> str:
    """
    Estimate company valuation using SaaS multiples (ARR, revenue, EBITDA).
    Returns realistic range + acquisition multiple breakdown.

    Args:
        mrr: Current Monthly Recurring Revenue ($)
        growth_rate_monthly_pct: Monthly MRR growth % (e.g. 8.0 = 8%/mo)
        churn_rate_monthly_pct: Monthly churn % (e.g. 3.0 = 3%)
        nrr_pct: Net Revenue Retention % (e.g. 105.0 = 105% NRR)
        model: Valuation model — "saas" | "micro_saas" | "ebitda"
        profitable: True if the business is profitable
    """
    return json.dumps(_fn_valuation(
        mrr=mrr,
        growth_rate_monthly_pct=growth_rate_monthly_pct,
        churn_rate_monthly_pct=churn_rate_monthly_pct,
        nrr_pct=nrr_pct,
        model=model,
        profitable=profitable,
    ), indent=2)


@mcp.tool()
def get_mrr_live(
    stripe_api_key: str = "",
    include_trials: bool = False,
) -> str:
    """
    Pull live MRR from Stripe. Checks DuckDB cache first (valid for 1 hour after
    last sync). Falls back to direct Stripe API when cache is stale or missing.

    Response includes data_source: "live_stripe_cached" | "live_stripe".

    Returns: current MRR, ARPU (from cache or live), and cache freshness metadata.

    Args:
        stripe_api_key: Stripe secret key (reads STRIPE_API_KEY env var if empty)
        include_trials: Count trialing subscriptions toward MRR (default False)
    """
    return json.dumps(_fn_stripe_mrr(
        stripe_api_key=stripe_api_key,
        include_trials=include_trials,
    ), indent=2)


@mcp.tool()
def get_runway_live(
    mercury_api_key: str = "",
    monthly_burn: float = 0.0,
    mrr: float = 0.0,
) -> str:
    """
    Pull live cash balance and runway from Mercury bank. Checks DuckDB cache first
    (valid for 1 hour after last Mercury sync). Falls back to direct API when stale.

    Response includes data_source: "live_mercury_cached" | "live_mercury".
    MRR is auto-filled from Stripe/DuckDB when mrr=0 and data is connected.

    Args:
        mercury_api_key: Mercury API key (reads MERCURY_API_KEY env var if empty)
        monthly_burn: Monthly operating expenses for runway calculation ($)
        mrr: Current MRR to calculate net burn ($, auto-filled from DuckDB if 0)
    """
    return json.dumps(_fn_mercury_runway(
        mercury_api_key=mercury_api_key,
        monthly_burn=monthly_burn,
        mrr=mrr,
    ), indent=2)


# ─────────────────────────────────────────────────────────────
# Agent wrappers — tools/agents.py
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def council_brief(
    decision: str,
    stage_mrr: str = "",
    context_notes: str = "",
) -> str:
    """
    5-seat parallel intelligence council: Market Signal + Financial Health +
    Pattern Match + Risk Assessment + Opportunity Score.

    Each seat is a real Claude API call (haiku-4-5) running in parallel.
    Returns structured per-seat analysis + synthesized verdict.

    Use when: DECIDE trigger fires on reversibility ≤5/10 decisions.
    Replaces the keyword-matching heuristic council with real AI analysis.

    Args:
        decision: What the founder is considering
        stage_mrr: Current MRR (e.g. "$5K", "pre-revenue")
        context_notes: Additional business context for the council
    """
    result = run_council_brief(
        decision=decision,
        stage_mrr=stage_mrr,
        context_notes=context_notes,
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def ask_agent(
    role: str,
    question: str,
    context: str = "",
) -> str:
    """
    Ask a single specialist agent (CEO, CFO, CMO, CTO, etc.) a targeted question.
    Uses the agent's role-specific system prompt from agents/roles/.

    Available roles: ceo, cfo, cmo, coo, cto, pm, growth, analyst, sdr, ae, cs,
                     seo, finance, legal

    Args:
        role: Agent role to consult
        question: The specific question to ask
        context: Business context to include
    """
    return ask_role_agent(role=role, question=question, context=context)


# ─────────────────────────────────────────────────────────────
# Shared helpers (used by inline tools below)
# ─────────────────────────────────────────────────────────────

def _parse_reversibility(text: str) -> int:
    """Extract numeric reversibility score from text like '8/10' or '3/10'."""
    m = re.search(r"(\d+)/10", text)
    return int(m.group(1)) if m else 5


def _parse_mrr_string(mrr_str: str) -> int:
    """Convert '$3.5K', '$40,000', 'pre-revenue', '0' to integer."""
    mrr_str = mrr_str.lower().strip()
    if any(x in mrr_str for x in ["0", "pre", "none", "nothing", "zero"]):
        return 0
    cleaned = re.sub(r"[$,]", "", mrr_str)
    m = re.search(r"([\d.]+)\s*k", cleaned)
    if m:
        return int(float(m.group(1)) * 1000)
    m = re.search(r"([\d,]+)", cleaned)
    if m:
        return int(m.group(1).replace(",", ""))
    return 0


def _general_market_heuristics(category: str) -> dict:
    """Fallback heuristics when category not in database."""
    keywords = category.lower()
    if any(k in keywords for k in ["ai", "gpt", "llm", "generative"]):
        return {"note": "AI tools: likely saturated unless niche. Check ChatGPT substitution test first.", "default_margin": "80-90%"}
    if any(k in keywords for k in ["compliance", "gdpr", "hipaa", "legal"]):
        return {"note": "Compliance: high retention (80-90% 6-month). Structural moat.", "default_margin": "85-95%"}
    if any(k in keywords for k in ["crm", "project management", "task", "to-do"]):
        return {"note": "Heavily saturated. Need 10x differentiation or extremely narrow ICP.", "default_margin": "80-85%"}
    return {"note": "Run full validation gates before assuming viability.", "default_margin": "75-90%"}


_DECISION_TYPE_KEYWORDS: dict[str, list[str]] = {
    "pricing_increase": ["raise price", "increase price", "charge more", "premium", "price higher"],
    "pricing_decrease": ["lower price", "discount", "cheaper", "free tier", "reduce price"],
    "hire_first_employee": ["hire", "first employee", "bring someone on", "contractor", "VA"],
    "launch_new_feature": ["build", "add feature", "launch", "ship", "new feature"],
    "pivot": ["pivot", "change direction", "rebrand", "new market", "new idea", "start over"],
    "raise_funding": ["raise", "funding", "investors", "seed", "SAFE", "cap table", "dilution"],
    "enter_new_market": ["international", "new market", "expand to", "different segment", "new country"],
}


def _detect_decision_type(decision: str) -> str:
    dl = decision.lower()
    for dtype, keywords in _DECISION_TYPE_KEYWORDS.items():
        if any(kw in dl for kw in keywords):
            return dtype
    return "default"


# Causal chain map — single source of truth lives in tools/decisions.py
_CAUSAL_CHAINS = _DECISION_CAUSAL_CHAINS


# ─────────────────────────────────────────────────────────────
# Paid API recommendations (used by score_opportunity)
# ─────────────────────────────────────────────────────────────

_API_RECOMMENDATIONS: dict[str, list[dict]] = {
    "prospecting": [
        {"name": "Apollo.io", "url": "apollo.io", "free_tier": True,
         "paid_from_mrr": "$1K", "cost": "$49-99/mo",
         "unlocks": "50M+ B2B contacts, email sequences, intent signals",
         "best_for": "outbound prospecting at scale"},
        {"name": "Hunter.io", "url": "hunter.io", "free_tier": True,
         "paid_from_mrr": "$1K", "cost": "$49/mo",
         "unlocks": "Email finding + verification, domain search",
         "best_for": "finding decision-maker emails"},
        {"name": "Clay", "url": "clay.com", "free_tier": False,
         "paid_from_mrr": "$10K", "cost": "$149-800/mo",
         "unlocks": "Waterfall enrichment across 50+ data sources, AI personalization",
         "best_for": "hyper-personalized outbound at $10K+ MRR"},
    ],
    "competitive_intel": [
        {"name": "SimilarWeb", "url": "similarweb.com", "free_tier": True,
         "paid_from_mrr": "$5K", "cost": "$167-833/mo",
         "unlocks": "Competitor traffic, channels, audience overlap",
         "best_for": "understanding how competitors acquire users"},
        {"name": "Semrush", "url": "semrush.com", "free_tier": True,
         "paid_from_mrr": "$5K", "cost": "$130-500/mo",
         "unlocks": "Competitor keywords, backlinks, ad copy, content gaps",
         "best_for": "SEO + paid channel intelligence"},
        {"name": "Ahrefs", "url": "ahrefs.com", "free_tier": False,
         "paid_from_mrr": "$5K", "cost": "$99-399/mo",
         "unlocks": "Backlink analysis, keyword research, content explorer",
         "best_for": "Content-led growth strategy"},
    ],
    "customer_analytics": [
        {"name": "PostHog", "url": "posthog.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "Free up to 1M events",
         "unlocks": "Product analytics, session replay, feature flags, A/B tests",
         "best_for": "Understanding product behaviour — use from day 1"},
        {"name": "Mixpanel", "url": "mixpanel.com", "free_tier": True,
         "paid_from_mrr": "$5K", "cost": "$28-833/mo",
         "unlocks": "Funnel analysis, cohort retention, user paths",
         "best_for": "Retention analysis and churn diagnosis"},
        {"name": "LogRocket", "url": "logrocket.com", "free_tier": True,
         "paid_from_mrr": "$5K", "cost": "$99-500/mo",
         "unlocks": "Session replay, error tracking, performance monitoring",
         "best_for": "Debugging why users churn at specific steps"},
    ],
    "customer_intelligence": [
        {"name": "Intercom", "url": "intercom.com", "free_tier": False,
         "paid_from_mrr": "$5K", "cost": "$74-374/mo",
         "unlocks": "Live chat, product tours, surveys, knowledge base",
         "best_for": "Customer success at scale + in-app messaging"},
        {"name": "Crisp", "url": "crisp.chat", "free_tier": True,
         "paid_from_mrr": "$1K", "cost": "$25-95/mo",
         "unlocks": "Live chat, CRM, email campaigns, chatbots",
         "best_for": "Affordable Intercom alternative for early stage"},
        {"name": "Attio", "url": "attio.com", "free_tier": True,
         "paid_from_mrr": "$1K", "cost": "$34-119/mo",
         "unlocks": "CRM with real-time data enrichment, relationship intelligence",
         "best_for": "Modern CRM that enriches contacts automatically"},
    ],
    "payments": [
        {"name": "Stripe", "url": "stripe.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "2.9% + 30¢ per transaction",
         "unlocks": "Subscriptions, usage billing, invoicing, tax, Stripe Sigma",
         "best_for": "Default choice — deepest ecosystem and reporting"},
        {"name": "LemonSqueezy", "url": "lemonsqueezy.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "5% + 50¢ (Merchant of Record)",
         "unlocks": "Global tax compliance handled, easy setup, EU VAT",
         "best_for": "Solo founders who want zero tax headaches globally"},
        {"name": "Paddle", "url": "paddle.com", "free_tier": False,
         "paid_from_mrr": "$5K", "cost": "5% + 50¢ (Merchant of Record)",
         "unlocks": "Subscription management, global tax, localized pricing",
         "best_for": "B2B SaaS with international customers"},
    ],
    "financial_ops": [
        {"name": "Pilot.com", "url": "pilot.com", "free_tier": False,
         "paid_from_mrr": "$20K", "cost": "$599-1500/mo",
         "unlocks": "Automated bookkeeping, financial statements, tax prep",
         "best_for": "Replacing a part-time bookkeeper"},
        {"name": "Mercury", "url": "mercury.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "Free (+ Treasury at $0)",
         "unlocks": "Business banking, no fees, API, multi-user, runway dashboard",
         "best_for": "Default business bank for startups — use from day 1"},
        {"name": "Ramp", "url": "ramp.com", "free_tier": True,
         "paid_from_mrr": "$5K", "cost": "Free (+ Premium $15/user/mo)",
         "unlocks": "Corporate cards, spend management, bill pay, auto-categorization",
         "best_for": "Expense management once you have recurring business spend"},
    ],
    "email_marketing": [
        {"name": "Resend", "url": "resend.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "Free up to 3K/mo, then $20+",
         "unlocks": "Transactional email API, React Email, excellent deliverability",
         "best_for": "Transactional emails from day 1 — best developer experience"},
        {"name": "Customer.io", "url": "customer.io", "free_tier": False,
         "paid_from_mrr": "$5K", "cost": "$100-1000/mo",
         "unlocks": "Event-triggered campaigns, user segmentation, lifecycle automation",
         "best_for": "Sophisticated lifecycle email sequences tied to product events"},
        {"name": "Beehiiv", "url": "beehiiv.com", "free_tier": True,
         "paid_from_mrr": "$0", "cost": "Free up to 2.5K subscribers",
         "unlocks": "Newsletter platform with monetization, referral program, analytics",
         "best_for": "Content-founder building audience before product launch"},
    ],
    "legal_compliance": [
        {"name": "Stripe Atlas", "url": "stripe.com/atlas", "free_tier": False,
         "paid_from_mrr": "$0", "cost": "$500 one-time",
         "unlocks": "US LLC/C-Corp incorporation, bank account, EIN in days",
         "best_for": "Non-US founders incorporating a US entity quickly"},
        {"name": "Clerky", "url": "clerky.com", "free_tier": False,
         "paid_from_mrr": "$0", "cost": "$499-2000",
         "unlocks": "Incorporation, SAFEs, NDAs, employment docs — lawyer-quality",
         "best_for": "Founders who will raise funding — documents are VC-standard"},
        {"name": "Vanta", "url": "vanta.com", "free_tier": False,
         "paid_from_mrr": "$50K", "cost": "$800+/mo",
         "unlocks": "SOC 2, ISO 27001, HIPAA automated compliance",
         "best_for": "Enterprise sales requiring security certification"},
    ],
}


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: match_pattern
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def match_pattern(
    situation: str,
    top_n: int = 3,
    stage_mrr: str = "",
) -> str:
    """
    Find the most relevant decision patterns from the SoloOS PATTERN_LIBRARY
    for a given founder situation. Returns ranked patterns with real-world evidence
    and kill signals.

    Use when: A founder describes a decision, challenge, or situation and you need
    to surface the right framework with real evidence (not generic advice).

    Args:
        situation: Description of the founder's current situation or decision
        top_n: Number of patterns to return (default 3, max 5)
        stage_mrr: Current MRR for stage filtering e.g. "$3K" or "pre-revenue"
    """
    patterns = get_patterns()
    if not patterns:
        return json.dumps({"error": "PATTERN_LIBRARY.md not found or empty", "patterns": []})

    top_n = min(max(1, top_n), 5)
    matched = search_patterns(situation, patterns, top_n=top_n)

    if not matched:
        return json.dumps({
            "query": situation,
            "patterns_found": 0,
            "message": "No strong pattern match. Describe the specific decision type for better results.",
            "patterns": []
        })

    result = {
        "query": situation,
        "stage_context": stage_mrr or "unknown",
        "patterns_found": len(matched),
        "patterns": []
    }

    for p in matched:
        result["patterns"].append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "situation": p.situation,
            "pattern": p.pattern,
            "real_example": p.real_example,
            "kill_signal": p.kill_signal,
            "reversibility": p.reversibility,
            "apply_when": p.apply_when,
        })

    if matched:
        first = matched[0]
        rev_str = first.reversibility or ""
        rev_num = _parse_reversibility(rev_str)
        if rev_num >= 7:
            result["routing"] = "SYSTEM_1_FAST — reversibility ≥7/10. Strong pattern match. Can decide quickly."
        elif rev_num <= 4:
            result["routing"] = "SYSTEM_2_DELIBERATE — reversibility ≤4/10. Hard to reverse. Run full adversarial debate."
        else:
            result["routing"] = "SYSTEM_2_MEDIUM — moderate reversibility. Standard analysis warranted."

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: search_founder_cases
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def search_founder_cases(
    query: str,
    founder: str = "",
    tag: str = "",
    top_n: int = 3,
) -> str:
    """
    Search the SoloOS founder case database for real examples matching a query.
    Returns actual founder decisions with outcomes — not generic advice.

    Use when: You need to cite real evidence for a recommendation ("Pieter Levels did X
    at $Y MRR and got Z result") instead of making a generic claim.

    Args:
        query: What you're looking for (e.g. "pricing strategy", "distribution hack", "free tier")
        founder: Filter by specific founder name (e.g. "Marc Lou", "Pieter Levels")
        tag: Filter by tag (pricing, distribution, community, seo, compliance, ai_product, b2b, b2c)
        top_n: Number of cases to return (default 3)
    """
    cases = get_founders()
    if not cases:
        return json.dumps({"error": "FOUNDER_INTELLIGENCE.md not found or empty", "cases": []})

    if founder:
        cases = [c for c in cases if founder.lower() in c.founder.lower()]
    if tag:
        cases = [c for c in cases if tag.lower() in [t.lower() for t in c.tags]]

    top_n = min(max(1, top_n), 8)
    matched = search_founders(query, cases, top_n=top_n)

    if not matched:
        return json.dumps({
            "query": query,
            "filters": {"founder": founder, "tag": tag},
            "cases_found": 0,
            "message": "No matching cases. Try broader query or remove filters.",
            "cases": []
        })

    result = {
        "query": query,
        "filters": {"founder": founder, "tag": tag},
        "cases_found": len(matched),
        "cases": []
    }

    for c in matched:
        result["cases"].append({
            "founder": c.founder,
            "product": c.product,
            "peak_mrr": c.peak_mrr,
            "stage": c.stage,
            "decision": c.decision,
            "outcome": c.outcome,
            "pattern_id": c.pattern_id,
            "tags": c.tags,
        })

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: check_market
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def check_market(
    category: str,
) -> str:
    """
    Check market saturation, unit economics, and viability for a product category.
    Pulls from the SoloOS MARKET_INTELLIGENCE database.

    Use when: A founder mentions building in a specific category and you need
    to know if it's viable, saturated, or dead before giving advice.

    Args:
        category: Market category to check (e.g. "AI resume builder", "compliance SaaS",
                  "developer tools", "project management", "scheduling")
    """
    markets = get_markets()

    if not markets:
        return json.dumps({
            "category": category,
            "status": "no_data",
            "message": "MARKET_INTELLIGENCE.md not found. Using general heuristics.",
            "heuristics": _general_market_heuristics(category),
        })

    from .kb_loader import _tokenize
    query_tokens = _tokenize(category)
    scored = []
    for m in markets:
        m_tokens = _tokenize(m.name + " " + m.raw)
        overlap = len(query_tokens & m_tokens)
        scored.append((overlap, m))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored or scored[0][0] == 0:
        return json.dumps({
            "category": category,
            "status": "not_found",
            "message": f"'{category}' not in market database. Check MARKET_INTELLIGENCE.md.",
            "closest_categories": [m.name for _, m in scored[:3]],
            "heuristics": _general_market_heuristics(category),
        })

    m = scored[0][1]

    saturation_advice = {
        "Dead": "⛔ DEAD — Do not build. No viable revenue path exists in this exact category.",
        "Saturated": "🔴 SATURATED — Only viable with extreme niche focus or superior distribution.",
        "Viable-with-niche": "🟡 VIABLE WITH NICHE — Strong opportunity IF you narrow ICP ruthlessly.",
        "Open": "🟢 OPEN — Good opportunity. Move fast before saturation.",
        "Emerging": "🚀 EMERGING — First-mover advantage available. Validate fast.",
    }

    return json.dumps({
        "category": m.name,
        "saturation": m.saturation,
        "verdict": saturation_advice.get(m.saturation, "Unknown"),
        "signal": m.signal,
        "unit_economics": {
            "gross_margin": m.gross_margin or "85-90% (SaaS default)",
            "monthly_churn": m.churn_monthly or "3-7% (varies)",
            "ltv_cac_ratio": m.ltv_cac or "4-8x target",
        },
        "notes": m.notes,
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: generate_competitor_brief
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def generate_competitor_brief(
    competitor_name: str,
    known_pricing: str = "",
    known_target_icp: str = "",
    known_complaints: list[str] | None = None,
    your_mrr: str = "",
    your_icp: str = "",
) -> str:
    """
    Generate a structured 5-layer competitor autopsy template pre-filled with
    known data and a research agenda for what to find next.

    Use when: Any competitor is mentioned. Returns the full Intel Engine template
    populated with known facts and a prioritized research agenda.

    Args:
        competitor_name: Name of the competitor to profile
        known_pricing: Any known pricing info (e.g. "$49-199/mo", "freemium")
        known_target_icp: Their stated target customer
        known_complaints: List of known complaints from reviews, Reddit, etc.
        your_mrr: Your current MRR (for Mandala positioning)
        your_icp: Your target ICP (for displacement opportunity detection)
    """
    if known_complaints is None:
        known_complaints = []

    research_agenda = []
    mandala_position = "Ring 1 (Direct Enemy)" if your_icp and known_target_icp else "Unknown — research needed"

    if not known_pricing:
        research_agenda.append("🔍 Pricing: Visit their pricing page. Note plan names, prices, annual discount, free tier limits.")
    if not known_target_icp:
        research_agenda.append("🔍 Real ICP: Search LinkedIn for people who list this tool in their profile. What's their title and company size?")
    if not known_complaints:
        research_agenda.append(f"🔍 Complaints: Search Reddit for 'alternative to {competitor_name}' and 'switched away from {competitor_name}'. Search G2 for 1-3 star reviews.")
    research_agenda.append(f"🔍 Distribution: Check {competitor_name}.com/blog for content strategy. Check SimilarWeb for traffic sources.")
    research_agenda.append(f"🔍 Achilles Heel: Check Glassdoor for company reviews — insider complaints reveal strategic weaknesses.")

    displacement_ops = []
    for complaint in known_complaints:
        displacement_ops.append(f"→ Complaint detected: '{complaint}' — this is a displacement opening. If you solve this, target their users with this specific pain.")

    if your_mrr:
        mrr_val = _parse_mrr_string(your_mrr)
        if mrr_val < 50000:
            upaya = "SAMA (alliance) — you're the smaller force. Don't fight them directly. Find the ICP segment they explicitly ignore and own it."
        else:
            upaya = "DANA + DANDA — you have resources. Use DANA (superior pricing/features for switchers) and DANDA (displacement campaigns targeting their churn)."
    else:
        upaya = "SAMA → Research their weakest ICP segment first before declaring war."

    template = f"""
COMPETITOR PROFILE: {competitor_name}
Date: {today_str()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 1: THE OFFER
→ Core product: [RESEARCH NEEDED]
→ Target ICP: {known_target_icp or "[RESEARCH: Who does their website say they serve?]"}
→ Pricing: {known_pricing or "[RESEARCH: Check their pricing page]"}
→ Free tier: [RESEARCH: Yes/No + what's included]
→ Positioning: [RESEARCH: Their tagline from homepage]
→ Primary differentiator claim: [RESEARCH: What do they say makes them different?]

LAYER 2: THE REAL ICP
→ LinkedIn profile mentions: [RESEARCH: Search LinkedIn, filter by tool in profile]
→ Twitter/X builders: [RESEARCH: Who builds in public using this?]
→ Subreddits that recommend it: [RESEARCH: Where does it get mentioned positively?]
→ True ICP conclusion: [Does real ICP differ from Layer 1 claim?]

LAYER 3: SWITCH-AWAY REASONS (Their Churn Intel)
{chr(10).join(f'→ Known complaint: "{c}"' for c in known_complaints) if known_complaints else "→ [RESEARCH: Search Reddit + G2 1-3 star reviews for verbatim complaints]"}
→ Feature gaps: [RESEARCH: What do users say they wish it had?]
→ Pricing complaints: [RESEARCH: Too expensive? Recent increases?]
→ Support complaints: [RESEARCH: Response time, AI-only support?]

LAYER 4: THEIR DISTRIBUTION
→ Primary channel: [RESEARCH: SEO / Paid / Community / Viral / Sales-led]
→ Content strategy: [RESEARCH: Blog frequency, SEO topics, traffic estimate]
→ Social presence: [RESEARCH: Twitter/X, LinkedIn, YouTube — size + engagement]
→ Integrations: [RESEARCH: Which tools integrate with them?]
→ Marketplace presence: [RESEARCH: App stores — Slack, Notion, HubSpot?]

LAYER 5: THE ACHILLES HEEL
→ Technical: [What does their architecture prevent them from doing?]
→ Pricing: [Who can't afford them? Who do they over-charge?]
→ ICP gap: [Who are they explicitly NOT serving well?]
→ Feature gap: [Most-requested feature they haven't shipped?]
→ Speed: [How fast do they ship? Check their changelog/blog frequency]

STRATEGIC RESPONSE:
→ Mandala position: {mandala_position}
→ Upaya to apply: {upaya}
→ Our asymmetry: [Where can you win that they cannot match at your ICP?]
→ Displacement targets: [Who specifically is complaining about them?]
→ Kill signal: "They are losing to us if: [specific metrics]"
"""

    return json.dumps({
        "competitor": competitor_name,
        "template": template.strip(),
        "known_data": {
            "pricing": known_pricing or "unknown",
            "stated_icp": known_target_icp or "unknown",
            "complaints_collected": len(known_complaints),
        },
        "research_agenda": research_agenda,
        "displacement_opportunities": displacement_ops,
        "chanakya_upaya": upaya,
        "mandala_position": mandala_position,
        "live_research_commands": [
            f'reddit_search_reddit(query="alternative to {competitor_name}", limit=25)',
            f'reddit_search_reddit(query="switched from {competitor_name}", limit=25)',
            f'reddit_search_reddit(query="{competitor_name} complaints", limit=25)',
            f'hackernews search: "{competitor_name}" in getTopStories and getShowHNStories',
            f'jina_reader: "{competitor_name}.com/pricing" for pricing page scrape',
        ],
        "next_step": "Run the live research commands above using Reddit MCP and HN MCP. Then fill in Layers 2-5 with real data.",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: monitor_competitor
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def monitor_competitor(
    competitor_name: str,
    competitor_url: str = "",
    your_mrr: str = "$0",
    your_icp: str = "",
    known_recent_changes: str = "",
    category: str = "",
) -> str:
    """
    Generate a structured weekly competitive intelligence brief for a specific competitor.
    Provides a monitoring checklist, signal classification, and strategic response recommendations.

    Args:
        competitor_name: Name of the competitor to monitor
        competitor_url: Their website URL (optional but improves output)
        your_mrr: Your current MRR for stage-calibrated framing
        your_icp: Your ideal customer profile
        known_recent_changes: Any changes you already know about
        category: Market category (e.g., "AI email tools")
    """
    founder_mrr_val = _parse_mrr_string(your_mrr)

    if founder_mrr_val < 5000:
        monitoring_intensity = "LIGHT — check monthly, focus on pricing/positioning only"
        threat_level_context = "At your stage, competitor moves matter less than getting first customers."
    elif founder_mrr_val < 20000:
        monitoring_intensity = "MODERATE — check bi-weekly, track pricing + new features + customer complaints"
        threat_level_context = "At your stage, competitor weaknesses = your acquisition opportunities."
    else:
        monitoring_intensity = "ACTIVE — weekly monitoring, full signal tracking"
        threat_level_context = "At your stage, competitor intelligence directly informs positioning and roadmap."

    offer_signals = [
        f"Pricing page changes (scrape {competitor_url}/pricing if available)",
        "Free tier limits and paid tier feature gates",
        "New product lines or feature announcements",
        "Trial length and onboarding flow changes",
        "Integration additions (their API/integrations page)",
    ]

    icp_signals = [
        f"Who is upvoting their ProductHunt page (job titles, company sizes)",
        f"Case studies and testimonials (which company types they highlight)",
        f"Job postings (what roles they're hiring = what segments they're going after)",
        "LinkedIn page followers — company size and industry breakdown",
        "Content topics (what customer segments their blog/content targets)",
    ]

    sentiment_sources = [
        f"Reddit: search '{competitor_name} review', '{competitor_name} alternative', '{competitor_name} problems'",
        f"HackerNews: search '{competitor_name}' in comments (hn.algolia.com)",
        f"G2 / Capterra: most recent 1-star and 2-star reviews",
        f"Twitter/X: '{competitor_name} -filter:retweets' sorted by Latest",
        f"Indie Hackers: search their name in community posts",
    ]

    distribution_signals = [
        "Content publishing frequency and topics (Similarweb/Semrush for free estimate)",
        "Backlink profile changes (new partnerships indicated by referring domains)",
        "Social media posting cadence and engagement",
        f"Podcast / conference appearances (Google: 'site:buzzsprout.com OR site:transistor.fm {competitor_name}')",
        "Affiliate / partner program activity",
    ]

    achilles_patterns = {
        "complexity": "Complex product targeting power users → opportunity: simpler tool for same outcome",
        "price": "High price point → opportunity: lower entry price for specific segment",
        "support": "Poor support reviews → opportunity: obsessive customer success as differentiator",
        "niche": "Broad generalist product → opportunity: deep specialization for one vertical",
        "legacy": "Legacy tech/UX → opportunity: modern stack, better developer experience",
        "size": "Large company, slow roadmap → opportunity: faster shipping, founder relationship with customers",
    }

    mcp_commands = [
        f"mcp__reddit__reddit_search_reddit(query='{competitor_name} problems OR sucks OR alternative OR switch', limit=25)",
        f"mcp__reddit__reddit_search_reddit(query='{competitor_name} review', subreddit='SaaS', limit=10)",
        f"mcp__hackernews__getItem (search HN Algolia for '{competitor_name}')",
    ]
    if competitor_url:
        mcp_commands.append(f"mcp__jina__jina_reader(url='{competitor_url}/pricing') — extract current pricing")
        mcp_commands.append(f"mcp__jina__jina_reader(url='{competitor_url}/blog') — track content topics")

    signal_types = {
        "🔴 THREAT (act within 1 week)": [
            "Price cut >20% (may pull price-sensitive customers)",
            "Feature launch that directly matches your core value prop",
            "Funding announcement (more resources incoming)",
            "Partnership with your distribution channel",
        ],
        "🟡 MONITOR (track monthly)": [
            "New enterprise tier (signals upmarket move — opens SMB)",
            "New integrations (what tools their customers use)",
            "Content pivots to new ICP",
            "Leadership changes (new CEO/CMO = strategy change possible)",
        ],
        "🟢 OPPORTUNITY (act within 30 days)": [
            "Spike in 1-star reviews (capture their churning customers)",
            "Raising prices (offer price-locked migration deal)",
            "Shutting down feature (announce yours is staying)",
            "Layoffs / support degradation (outreach to their customers)",
        ],
    }

    return json.dumps({
        "competitor": competitor_name,
        "monitoring_intensity": monitoring_intensity,
        "stage_context": threat_level_context,
        "five_layer_monitoring": {
            "layer_1_offer": offer_signals,
            "layer_2_icp_signals": icp_signals,
            "layer_3_customer_sentiment": sentiment_sources,
            "layer_4_distribution": distribution_signals,
            "layer_5_achilles_heel_patterns": achilles_patterns,
        },
        "known_recent_changes": known_recent_changes if known_recent_changes else "None provided — start with live search",
        "mcp_commands_to_run_now": mcp_commands,
        "signal_classification": signal_types,
        "weekly_brief_format": {
            "pricing_changes": "[none / raised / lowered / new tier added]",
            "new_features": "[list or none]",
            "customer_sentiment_trend": "[improving / stable / declining]",
            "top_complaint_this_week": "[from review sites / reddit]",
            "recommended_action": "[one specific response this week]",
        },
        "displacement_outreach_trigger": (
            f"If their review sentiment is declining: search Reddit for '{competitor_name} alternative' posters. "
            f"DM them directly with: 'I saw you're looking for alternatives to {competitor_name}. "
            f"I built [your product] specifically for [ICP]. Happy to show you — what's your biggest pain with them?'"
        ),
        "kill_signal": (
            f"If {competitor_name} launches a feature that directly replicates your core value prop within 30 days "
            f"AND you cannot name a defensible differentiator → pause acquisition spend and define new positioning before continuing."
        ),
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: enrich_prospect
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def enrich_prospect(
    company_name: str,
    contact_name: str = "",
    contact_role: str = "",
    your_icp: str = "",
    your_product: str = "",
    your_mrr: str = "$0",
) -> str:
    """
    Generate a comprehensive prospect research brief to replace 30-45 minutes of manual research.
    Produces: company context, pain hypothesis, conversation starters, and 3 outreach variants.

    Args:
        company_name: Target company name
        contact_name: Decision-maker name (optional)
        contact_role: Their role/title (optional)
        your_icp: Your ideal customer profile description
        your_product: What your product does (1 sentence)
        your_mrr: Your current MRR (for ACV routing)
    """
    founder_mrr_val = _parse_mrr_string(your_mrr)

    if founder_mrr_val < 10000:
        outreach_motion = "HIGH-TOUCH: Personal DM → short value observation → ask for 20-min call"
        follow_up_sequence = "Day 0: initial DM/email | Day 3: value-add resource | Day 7: ask | Day 14: final"
    elif founder_mrr_val < 50000:
        outreach_motion = "STRUCTURED: Cold email sequence + LinkedIn connection + call offer"
        follow_up_sequence = "Day 0: email | Day 2: LinkedIn connect | Day 5: email 2 (case study) | Day 10: final ask"
    else:
        outreach_motion = "SALES-LED: Full SDR sequence, discovery call targeting, demo offer"
        follow_up_sequence = "Day 0: research + personalized email | Day 3: LinkedIn | Day 7: phone | Day 14: email | Day 21: final"

    research_checklist = {
        "company_signals": [
            f"Recent news: Google '{company_name} news site:techcrunch.com OR site:linkedin.com last 90 days'",
            f"Hiring signals: search '{company_name}' on LinkedIn Jobs → what roles? = their priorities",
            f"Funding history: Crunchbase '{company_name}' → when last funded? How much? Stage?",
            f"Tech stack: BuiltWith '{company_name}' → what tools they use reveals pain points",
            f"Employee count trajectory: LinkedIn company page → growth rate signals health",
        ],
        "contact_signals": [
            f"LinkedIn activity: what has {contact_name or 'the contact'} posted/liked/commented in last 30 days?",
            f"Pain signals: search '{contact_name or contact_role} {company_name}' on Twitter/X — any public frustrations?",
            f"Mutual connections: LinkedIn → who do you share that can make an intro?",
            f"Content: have they written any articles, talks, podcasts? What topics?",
        ],
        "pain_hypothesis_triggers": [
            f"mcp__reddit__reddit_search_reddit(query='{contact_role or company_name} pain problem struggle', limit=10)",
            f"Search Indie Hackers for '[industry] problems' to understand their context",
            f"Check G2/Capterra for tools they likely use → their reviews reveal workflow frustrations",
        ],
    }

    pain_hypothesis = {
        "template": f"If {company_name} is a [size] company doing [activity], their biggest pain in [your product category] is probably: [specific problem].",
        "validation_question": f"'I've been talking to {contact_role or 'founders'} at similar companies and the most common challenge I hear is [X]. Is that something you deal with, or is it different for you?'",
        "note": "Never assume the pain — use this as a hypothesis to validate in the opening question, not as a claim.",
    }

    outreach_variants = {
        "variant_1_insight": {
            "approach": "Lead with a relevant insight specific to their company/role",
            "template": f"Hi {contact_name or '[Name]'},\n\nI noticed [company_specific_observation — from hiring/news/product/content].\n\nMost {contact_role or 'teams'} I talk to at [similar company type] are dealing with [specific pain] because of this.\n\nIs that relevant for you, or are you in a different place?\n\n[Your name]",
            "best_for": "Cold email, LinkedIn DM to someone who posts actively",
        },
        "variant_2_case_study": {
            "approach": "Lead with a relevant outcome from a similar company",
            "template": f"Hi {contact_name or '[Name]'},\n\nI helped [similar company type] [specific outcome] using [your product].\n\nGiven what {company_name} is building, it might apply.\n\nWorth a 15-minute call to see if the situation is similar?\n\n[Your name]",
            "best_for": "Cold email when you have a relevant case study",
        },
        "variant_3_resource": {
            "approach": "Lead with pure value — no ask",
            "template": f"Hi {contact_name or '[Name]'},\n\nI've been researching [their industry/problem space] and wrote up [relevant resource]. Thought it might be useful given what {company_name} is working on.\n\n[Link or attach]\n\nNo ask — just hope it's useful. [Your name]",
            "best_for": "First touch when you want to start a relationship without a pitch",
        },
    }

    discovery_openers = [
        f"'What's the most painful part of [relevant workflow] for your team right now?'",
        f"'I saw you're hiring for [role from job board] — what's driving that decision?'",
        f"'I noticed {company_name} recently [news/product/hiring signal] — is [related challenge] something you're focused on?'",
        f"'What does your current workflow for [relevant activity] look like today?'",
    ]

    return json.dumps({
        "prospect": {
            "company": company_name,
            "contact": contact_name or "Not specified",
            "role": contact_role or "Not specified",
        },
        "outreach_motion": outreach_motion,
        "follow_up_sequence": follow_up_sequence,
        "research_agenda": research_checklist,
        "pain_hypothesis_framework": pain_hypothesis,
        "outreach_variants": outreach_variants,
        "discovery_openers": discovery_openers,
        "qualification_checklist": {
            "budget_signal": "Are they funded / profitable? (Crunchbase funding round or employee count trend)",
            "authority_signal": f"Is {contact_name or 'the contact'} a decision maker or influencer?",
            "need_signal": "Do their hiring signals or content indicate the pain your product solves?",
            "timing_signal": "Are there triggers suggesting NOW is the right time? (new hire, new initiative, funding)",
        },
        "kill_signal": (
            "If after 2 full outreach sequences (14 touchpoints) there is zero response: "
            "either wrong ICP, wrong channel, or wrong pain hypothesis. Do not increase volume — improve targeting."
        ),
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: get_system_state
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_system_state(
    decision: str,
    stage_mrr: str = "",
    show_causal_chain: bool = True,
) -> str:
    """
    Cross-domain system state snapshot BEFORE a significant decision.

    Pulls business context, kill signal status, relevant patterns, and causal chain
    in ONE call instead of requiring 4-5 separate tool calls.

    Use BEFORE any reversibility ≤5/10 decision.

    Args:
        decision: What the founder is considering (e.g. "raise prices from $49 to $99")
        stage_mrr: Current MRR for stage calibration (e.g. "$3K", "pre-revenue")
        show_causal_chain: Include downstream variable impact map (default True)

    Returns:
        Unified JSON: business_state + kill_signals + patterns + causal_chain + system_health
    """
    result: dict = {
        "decision_being_evaluated": decision,
        "timestamp": today_str(),
    }

    ctx = read_business_context()
    mrr = stage_mrr or ctx.get("mrr", "unknown")
    result["business_state"] = {
        "mrr": mrr,
        "stage": ctx.get("stage", "unknown"),
        "icp": ctx.get("icp", "not set"),
        "biggest_challenge": ctx.get("biggest_challenge", "not set"),
        "open_decisions": ctx.get("open_decisions", "none"),
        "context_populated": ctx.get("status") != "not_found",
    }

    entries = load_log()
    alerts = check_kill_signals(entries)
    pending = [e for e in entries if e.outcome_status == "⏳ Pending"]
    overdue = [a for a in alerts if a.urgency == "OVERDUE"]
    urgent = [a for a in alerts if a.urgency == "URGENT"]

    result["kill_signal_health"] = {
        "pending_count": len(pending),
        "overdue_count": len(overdue),
        "urgent_count": len(urgent),
        "warning": len(overdue) > 0 or len(urgent) > 0,
        "note": (
            f"⚠️ {len(overdue)} OVERDUE kill signal(s). Resolve before committing to new decisions."
            if overdue else
            f"🟡 {len(urgent)} urgent kill signal(s) due within 7 days." if urgent else
            "✅ No overdue kill signals."
        ),
        "alerts": [
            {"id": a.entry_id, "urgency": a.urgency, "summary": a.summary,
             "kill_signal": a.kill_signal, "days_remaining": a.days_remaining}
            for a in alerts
        ],
    }

    patterns = get_patterns()
    matched = search_patterns(decision, patterns, top_n=2) if patterns else []
    result["relevant_patterns"] = [
        {"id": p.id, "name": p.name, "situation": p.situation[:200],
         "kill_signal": p.kill_signal if hasattr(p, "kill_signal") else ""}
        for p in matched
    ] if matched else [{"note": "No strong pattern match in PATTERN_LIBRARY.md"}]

    if show_causal_chain:
        dtype = _detect_decision_type(decision)
        chain = _CAUSAL_CHAINS.get(dtype, _CAUSAL_CHAINS["default"])
        result["causal_chain"] = {
            "decision_type_detected": dtype,
            "downstream_effects": chain,
            "second_order_note": (
                "These effects compound. High-reversibility (≥7/10): proceed. "
                "Low-reversibility (≤4/10): gather 3 data points first."
            ),
        }

    health_flags: list[str] = []
    if ctx.get("status") == "not_found":
        health_flags.append("❌ No business context — run /onboard for calibrated advice")
    if overdue:
        health_flags.append(f"❌ {len(overdue)} overdue kill signal(s) — resolve first")
    if urgent:
        health_flags.append(f"⚠️ {len(urgent)} kill signal(s) expiring within 7 days")
    if not ctx.get("icp"):
        health_flags.append("⚠️ ICP not set — stage-calibrated advice is generic")

    health_score = max(0, 10 - (len(overdue) * 3) - (len(urgent) * 1) -
                       (2 if ctx.get("status") == "not_found" else 0))

    result["system_health"] = {
        "score": f"{health_score}/10",
        "flags": health_flags if health_flags else ["✅ System state looks healthy"],
        "recommendation": (
            "RESOLVE OVERDUE KILL SIGNALS BEFORE THIS DECISION"
            if overdue else
            "Proceed with decision — review causal chain above"
        ),
    }

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: run_morning_brief
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def run_morning_brief(
    include_kill_signals: bool = True,
    include_experiments: bool = True,
) -> str:
    """
    Morning intelligence brief — synthesizes overnight business state.

    Parallel analysis: kill signal health + active experiments + context
    summary + stage advice + recommended single action for today.

    Call at session start when: "good morning", "what should I focus on today",
    or any morning/daily planning message.

    Returns:
        Structured brief: pulse + alerts + experiments + recommended action
    """
    ctx = read_business_context()
    entries = load_log()
    alerts = check_kill_signals(entries)

    pending = [e for e in entries if e.outcome_status == "⏳ Pending"]
    overdue_alerts = [a for a in alerts if a.urgency == "OVERDUE"]
    urgent_alerts  = [a for a in alerts if a.urgency == "URGENT"]
    warning_alerts = [a for a in alerts if a.urgency == "WARNING"]

    mrr = ctx.get("mrr", "unknown")
    stage = ctx.get("stage", "unknown")
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0

    if mrr_int == 0:
        focus_rec = "Get your first paying customer today. ONE outreach, ONE demo, ONE close attempt."
    elif mrr_int < 5000:
        focus_rec = "Talk to a customer. Not build. Not design. Talk. What made them pay? What almost stopped them?"
    elif mrr_int < 20000:
        focus_rec = "What's the #1 thing blocking the next $5K MRR? Work only on that."
    elif mrr_int < 50000:
        focus_rec = "What's churning and why? Retention beats acquisition at this stage every time."
    else:
        focus_rec = "Systematise. What are you still doing manually that should be automated or delegated?"

    brief = {
        "date": today_str(),
        "pulse": {
            "mrr": mrr,
            "stage": stage,
            "icp": ctx.get("icp", "not set"),
            "context_populated": ctx.get("status") != "not_found",
        },
        "kill_signal_status": {
            "total_pending": len(pending),
            "overdue": len(overdue_alerts),
            "urgent": len(urgent_alerts),
            "warning": len(warning_alerts),
            "alerts": [{"id": a.entry_id, "urgency": a.urgency,
                        "summary": a.summary[:100],
                        "days_remaining": a.days_remaining}
                       for a in alerts[:5]],
        },
        "active_experiments": [
            {"id": e.id, "summary": e.summary[:100],
             "due": e.outcome_due, "days_left": e.days_until_kill_signal()}
            for e in pending[:5]
        ],
        "highest_leverage_action": focus_rec,
        "live_queries_to_run": {
            "market_pulse": {
                "reddit": "mcp__reddit__reddit_search_reddit — search your category for new pain points",
                "hackernews": "mcp__hackernews__getTopStories — filter for your market keywords",
            },
            "competitor_check": "mcp__soloos-core__generate_competitor_brief — if competitor changed pricing/features",
        },
        "decision_to_clear": ctx.get("open_decisions", "none logged — run /onboard to set one"),
        "session_intent": (
            "🚨 RESOLVE OVERDUE KILL SIGNALS" if overdue_alerts else
            "⚠️ Review urgent experiments" if urgent_alerts else
            "✅ Clear today's one decision. Then execute."
        ),
    }

    return json.dumps(brief, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: score_opportunity
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def score_opportunity(
    idea: str,
    market_size_signal: str = "",
    founder_background: str = "",
    competitor_count: int = -1,
    target_price: float = 0,
    stage_mrr: str = "",
    goal: str = "",
) -> str:
    """
    Unified opportunity scoring across 5 dimensions + API recommendations.

    Scores market_size, founder_fit, timing, competition, monetization
    and recommends the specific paid APIs/services needed to execute this
    opportunity based on the goal and stage.

    Args:
        idea: The opportunity being evaluated
        market_size_signal: Any evidence about market size (search volume, subreddit size, etc.)
        founder_background: Relevant founder experience
        competitor_count: How many direct competitors exist (-1 = unknown)
        target_price: Expected monthly price point
        stage_mrr: Current MRR
        goal: Primary goal (e.g. "reach $10K MRR", "sell in 18 months", "lifestyle")
    """
    ctx = read_business_context()
    mrr = stage_mrr or ctx.get("mrr", "unknown")
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0

    scores: dict[str, dict] = {}

    # Market Size
    ms_score = 5
    ms_note = "No market size signal provided — run Reddit/HN scan to validate"
    if market_size_signal:
        kw = market_size_signal.lower()
        if any(x in kw for x in ["billion", "b market", "100m+", "large"]):
            ms_score, ms_note = 8, "Large market signal detected — validate narrowing strategy"
        elif any(x in kw for x in ["million", "m market", "10m"]):
            ms_score, ms_note = 6, "Mid-size market — sufficient for lifestyle, tight for venture scale"
        elif any(x in kw for x in ["niche", "small", "few thousand"]):
            ms_score, ms_note = 4, "Niche market — verify pricing supports revenue goals"
    scores["market_size"] = {"score": ms_score, "max": 10, "note": ms_note}

    # Founder Fit
    ff_score = 5
    ff_note = "No founder background provided"
    if founder_background:
        fb = founder_background.lower()
        if any(x in fb for x in ["built", "sold", "exited", "worked at", "domain expert", "years in"]):
            ff_score, ff_note = 8, "Strong domain signal — unfair advantage likely"
        elif any(x in fb for x in ["interested", "learning", "exploring", "curious"]):
            ff_score, ff_note = 4, "Interest signal — validate you have edge over someone already in this domain"
    elif ctx.get("icp"):
        ff_note = f"ICP known ({ctx['icp'][:60]}) — assess if you can reach them credibly"
        ff_score = 6
    scores["founder_fit"] = {"score": ff_score, "max": 10, "note": ff_note}

    # Timing
    timing_score = 5
    timing_note = "Run Kaala assessment: mcp__soloos-core__get_system_state for position vs market window"
    if competitor_count == 0:
        timing_score, timing_note = 9, "No direct competitors — either pioneer or premature"
    elif 0 < competitor_count <= 3:
        timing_score, timing_note = 7, "Early market with few players — differentiation achievable"
    elif 4 <= competitor_count <= 10:
        timing_score, timing_note = 5, "Crowded enough to need sharp positioning"
    elif competitor_count > 10:
        timing_score, timing_note = 3, "Saturated — need category creation or significant wedge"
    scores["timing"] = {"score": timing_score, "max": 10, "note": timing_note}

    # Competition
    comp_score = max(0, 10 - (competitor_count if competitor_count >= 0 else 5))
    comp_note = (f"{competitor_count} known competitors" if competitor_count >= 0
                 else "Competitor count unknown — run generate_competitor_brief")
    scores["competition"] = {"score": min(comp_score, 10), "max": 10, "note": comp_note}

    # Monetization
    mon_score = 5
    mon_note = "Target price not specified"
    if target_price > 0:
        if target_price >= 200:
            mon_score, mon_note = 9, f"${target_price}/mo — B2B pricing, strong unit economics"
        elif target_price >= 50:
            mon_score, mon_note = 7, f"${target_price}/mo — viable if CAC < $300"
        elif target_price >= 15:
            mon_score, mon_note = 5, f"${target_price}/mo — needs volume, tight on margin"
        else:
            mon_score, mon_note = 3, f"${target_price}/mo — requires mass scale or freemium-to-paid upgrade"
    scores["monetization"] = {"score": mon_score, "max": 10, "note": mon_note}

    total = sum(v["score"] for v in scores.values())
    max_total = sum(v["max"] for v in scores.values())
    overall_pct = round((total / max_total) * 100)
    verdict = (
        "🟢 HIGH conviction — pursue aggressively, set 30-day kill signal" if overall_pct >= 70 else
        "🟡 MEDIUM conviction — validate 2 weak dimensions before building" if overall_pct >= 50 else
        "🔴 LOW conviction — too many unknowns. Validate before committing any weeks"
    )

    # API recommendations by goal
    recommended_apis = []
    if goal:
        gl = goal.lower()
        if any(x in gl for x in ["mrr", "revenue", "customers", "sales", "outbound"]):
            recommended_apis.extend(_API_RECOMMENDATIONS.get("prospecting", [])[:2])
            recommended_apis.extend(_API_RECOMMENDATIONS.get("payments", [])[:1])
        if any(x in gl for x in ["retain", "churn", "product", "engagement"]):
            recommended_apis.extend(_API_RECOMMENDATIONS.get("customer_analytics", [])[:2])
        if any(x in gl for x in ["sell", "exit", "acquire", "valuation"]):
            recommended_apis.extend(_API_RECOMMENDATIONS.get("financial_ops", [])[:2])
        if any(x in gl for x in ["compete", "market", "seo", "content", "grow"]):
            recommended_apis.extend(_API_RECOMMENDATIONS.get("competitive_intel", [])[:2])
    recommended_apis.extend(_API_RECOMMENDATIONS.get("customer_analytics", [{}])[:1])
    recommended_apis.extend(_API_RECOMMENDATIONS.get("financial_ops", [{}])[:1])

    seen, unique_apis = set(), []
    for api in recommended_apis:
        if api.get("name") and api["name"] not in seen:
            seen.add(api["name"])
            api_mrr_str = api.get("paid_from_mrr", "$0").replace("$", "").replace("K", "000")
            try:
                api_mrr_int = int(api_mrr_str)
                if mrr_int >= api_mrr_int or api_mrr_int == 0:
                    unique_apis.append(api)
                else:
                    unique_apis.append({**api, "note": f"Unlocks at {api['paid_from_mrr']} MRR — bookmark for later"})
            except (ValueError, TypeError):
                unique_apis.append(api)

    kill_signal = (
        f"If [{idea[:40]}...] does not generate [measurable signal] within 30 days, "
        f"abandon or pivot the approach."
    )

    return json.dumps({
        "idea": idea,
        "overall_score": f"{overall_pct}%",
        "verdict": verdict,
        "dimensions": scores,
        "goal": goal or "not specified",
        "recommended_api_stack": unique_apis[:6],
        "kill_signal": kill_signal,
        "next_actions": [
            "Run mcp__soloos-core__validate_idea_gates for Gate 0-4 validation",
            "Run mcp__reddit__reddit_search_reddit to find real customer pain in this space",
            "Run mcp__soloos-core__get_decision_intelligence_brief for full swarm analysis",
            f"Set a 30-day kill signal: {kill_signal}",
        ],
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: get_market_signals
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_market_signals(
    founder_stage: str = "",
    focus_topics: Optional[list[str]] = None,
) -> str:
    """
    Live market intelligence swarm: HN top stories + Reddit founder signals + pain point mining.

    Fetches real-time data using public APIs (no auth required). Designed to work
    in both local Claude Code sessions and remote CCR morning triggers.

    Use when: morning brief, competitor context needed, market validation, or
    "what's happening in [space]?" questions.

    Args:
        founder_stage: Current MRR for relevance filtering (e.g. "$3K", "pre-revenue")
        focus_topics: Topics to bias toward (default: saas, startup, founder, indie hacker)
    """
    result = run_morning_intelligence(
        founder_stage=founder_stage,
        focus_topics=focus_topics,
    )
    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# INLINE TOOL: read_web_content
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def read_web_content(
    url: str,
    extract_competitor_intel: bool = True,
    max_chars: int = 3000,
) -> str:
    """
    Extract clean text from any URL using Jina AI reader (free, no auth).

    Best for: competitor pricing pages, blog posts, landing pages, changelog pages.
    Returns: clean text + pricing signals + feature signals (if competitor_intel=True).

    Args:
        url: The URL to read (must start with http/https)
        extract_competitor_intel: Also extract pricing/feature signals (default True)
        max_chars: Max characters to return from clean text (default 3000)
    """
    content = read_url_content(url, max_chars=max_chars)
    result: dict = {"url": url, "content": content}

    if extract_competitor_intel:
        intel = get_competitor_intel(url)
        result["pricing_signals"] = intel.get("pricing_signals", [])
        result["feature_signals"] = intel.get("feature_signals", [])

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# V10: System intelligence tools
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def analyze_self(period_days: int = 30) -> str:
    """
    [V10] Analyze SoloOS's own usage patterns and identify improvements.

    Reads tool_calls.jsonl for the last N days and returns:
    - Slowest tools (highest avg latency)
    - Most-called tools (usage patterns)
    - Highest error rate tools
    - Cache hit rates
    - Top 3 improvement proposals

    This is the Reflexive Metasystem capability — the system analyzes itself.

    Args:
        period_days: Lookback window in days (default 30)
    """
    stats = get_log_stats(period_hours=period_days * 24)
    tools_data = stats.get("tools", {})

    if not tools_data:
        return json.dumps({
            "status": "no_data",
            "message": f"No tool call logs found in the last {period_days} days.",
            "log_location": "~/.soloos/logs/tool_calls.jsonl",
            "hint": "Logs are written automatically after you use tools. Come back in a session or two.",
        }, indent=2)

    # Rank by different dimensions
    by_calls = sorted(tools_data.items(), key=lambda x: -x[1]["calls"])
    by_latency = sorted(tools_data.items(), key=lambda x: -x[1]["avg_ms"])
    by_errors = sorted(tools_data.items(), key=lambda x: -x[1]["error_rate"])

    # Generate improvement proposals
    proposals = []

    slowest = by_latency[0] if by_latency else None
    if slowest and slowest[1]["avg_ms"] > 5000:
        proposals.append({
            "priority": "HIGH",
            "issue": f"'{slowest[0]}' averages {slowest[1]['avg_ms']}ms — above 5s threshold",
            "proposal": "Add TTL_LLM cache (24h) to reduce repeated calls. Check if council seats can be parallelized further.",
        })

    highest_error = by_errors[0] if by_errors else None
    if highest_error and highest_error[1]["error_rate"] > 0.1:
        proposals.append({
            "priority": "HIGH",
            "issue": f"'{highest_error[0]}' has {highest_error[1]['error_rate']*100:.0f}% error rate",
            "proposal": "Add explicit error handling + fallback. Check if external API changed.",
        })

    most_called = by_calls[0] if by_calls else None
    if most_called and most_called[1]["calls"] > 10:
        proposals.append({
            "priority": "MEDIUM",
            "issue": f"'{most_called[0]}' called {most_called[1]['calls']}x in {period_days} days — high frequency",
            "proposal": "Ensure this tool has caching. Consider if it can return richer context to reduce follow-up calls.",
        })

    if not proposals:
        proposals.append({
            "priority": "LOW",
            "issue": "No critical performance issues detected",
            "proposal": "System is performing within normal parameters. Focus on new capabilities.",
        })

    result = {
        "period_days": period_days,
        "total_calls": stats.get("total_calls", 0),
        "total_errors": stats.get("total_errors", 0),
        "top_tools_by_usage": [
            {"tool": name, **data} for name, data in by_calls[:5]
        ],
        "slowest_tools": [
            {"tool": name, **data} for name, data in by_latency[:3]
        ],
        "improvement_proposals": proposals,
        "cache_stats": get_cache_stats(),
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def manage_cache(
    action: str,
    prefix: str = "",
) -> str:
    """
    [V10] Manage the SoloOS disk cache.

    Actions:
      stats    — Show cache size, item count, hit rates
      clear    — Clear entire cache (forces fresh data on next calls)
      clear_llm — Clear only LLM/council responses (force fresh council)
      clear_http — Clear only HTTP/market signal responses (force fresh signals)

    Args:
        action: "stats" | "clear" | "clear_llm" | "clear_http"
        prefix: For custom prefix clearing (advanced use)
    """
    if action == "stats":
        return json.dumps(get_cache_stats(), indent=2)

    elif action == "clear":
        count = clear_all_cache()
        return json.dumps({"cleared": count, "message": f"Cleared {count} cache entries."}, indent=2)

    elif action == "clear_llm":
        # LLM keys contain function names from agents.py
        count = clear_cache_by_prefix("soloos_core.tools.agents")
        return json.dumps({"cleared": count, "message": f"Cleared {count} LLM cache entries. Next council call will be fresh."}, indent=2)

    elif action == "clear_http":
        count = clear_cache_by_prefix("soloos_core.tools.intelligence")
        return json.dumps({"cleared": count, "message": f"Cleared {count} HTTP cache entries. Next market signal call will be fresh."}, indent=2)

    elif action == "clear_prefix" and prefix:
        count = clear_cache_by_prefix(prefix)
        return json.dumps({"cleared": count, "prefix": prefix}, indent=2)

    else:
        return json.dumps({
            "error": f"Unknown action '{action}'",
            "valid_actions": ["stats", "clear", "clear_llm", "clear_http"],
        }, indent=2)


# ─────────────────────────────────────────────────────────────
# Scheduler tools — Phase F
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def scheduler_status() -> str:
    """
    List all background scheduler jobs, their next run times, and configured
    delivery channels (Slack, ntfy, email).

    Returns JSON with: scheduler_enabled, timezone, jobs list (name, cron,
    enabled, next_run, status), delivery_channels_configured, apscheduler_available.

    Use this to verify the scheduler is running and jobs are scheduled correctly.
    """
    return json.dumps(_sched_status(), indent=2)


@mcp.tool()
def scheduler_run_now(
    job_name: str,
) -> str:
    """
    Trigger a scheduled job immediately without waiting for its cron schedule.

    Available job names:
      morning_brief_job     — run morning brief and deliver it
      kill_signal_check_job — check kill signals and alert if overdue
      data_sync_job         — sync data from connected integrations
      weekly_review_job     — run extended weekly review

    Args:
        job_name: Name of the job to run immediately
    """
    return json.dumps(_sched_run_now(job_name), indent=2)


@mcp.tool()
def scheduler_configure(
    job_name: str,
    enabled: bool,
    cron: str = "",
) -> str:
    """
    Enable or disable a scheduled job and optionally update its cron schedule.
    Changes are written to ~/.soloos/scheduler-config.yaml immediately.
    Restart the MCP server for changes to take effect.

    Args:
        job_name: Job to configure (e.g. "morning_brief", "kill_signal_check")
        enabled: True to enable the job, False to disable it
        cron: Optional cron expression (e.g. "0 8 * * *" for 08:00 daily).
              Leave empty to keep the existing schedule.
    """
    return json.dumps(_sched_configure(job_name=job_name, enabled=enabled, cron=cron), indent=2)


# ─────────────────────────────────────────────────────────────
# Connector tools — Phase C/D
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def connector_status() -> str:
    """
    List all data connectors (Stripe, Mercury, PostHog), which are configured,
    their last sync time, last cursor, and the DuckDB tables they write to.

    Use this to diagnose data freshness and check which integrations are active.
    Returns a list of connector status dicts — one per connector.
    """
    registry = _get_connector_registry()
    return json.dumps({
        "connectors": registry.status(),
        "configured_count": sum(1 for c in registry.status() if c["configured"]),
        "total_count": len(registry.all_connectors()),
    }, indent=2, default=str)


@mcp.tool()
def connector_sync(
    source: str = "all",
) -> str:
    """
    Trigger a data sync for one or all configured connectors.
    Reads the last cursor from sync_state for incremental sync.
    Returns sync results per connector: rows_synced, duration_ms, error.

    Args:
        source: Connector to sync — "stripe", "mercury", "posthog", or "all" (default)

    Use when: MRR/banking data feels stale, or after connecting a new integration.
    """
    registry = _get_connector_registry()

    if source == "all":
        results = registry.sync_all()
    else:
        # Find and sync a specific connector
        matched = [c for c in registry.configured_connectors() if c.source_name == source]
        if not matched:
            # Check if it exists but is not configured
            all_sources = [c.source_name for c in registry.all_connectors()]
            if source in all_sources:
                return json.dumps({
                    "error": f"Connector '{source}' exists but is not configured. Check env vars and SDK.",
                    "source": source,
                }, indent=2)
            return json.dumps({
                "error": f"Unknown connector '{source}'. Available: {all_sources}",
            }, indent=2)

        from soloos_core.data.analytics_db import get_analytics_db
        db = get_analytics_db()
        connector = matched[0]
        state = db.get_sync_state(source) or {}
        last_cursor = state.get("last_cursor")
        results = [connector._timed_sync(since_cursor=last_cursor)]

    return json.dumps({
        "synced": [r.to_dict() for r in results],
        "total_rows_synced": sum(r.rows_synced for r in results),
        "errors": [r.error for r in results if not r.ok],
    }, indent=2, default=str)




# ─────────────────────────────────────────────────────────────
# Phase G: A/B Testing tools — GrowthBook
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def create_ab_experiment(
    name: str,
    hypothesis: str,
    metric: str,
    variants: list[str],
    traffic_split: list[float] | None = None,
) -> str:
    """
    Create an A/B experiment in GrowthBook for a founder decision.

    Best for: pricing page copy, CTA text, onboarding flow variants,
    email subject lines, or any 2-way test where you need statistical
    confidence before shipping.

    Requires GrowthBook self-hosted (docker/growthbook-compose.yml) and:
      GROWTHBOOK_API_HOST=http://localhost:3100
      GROWTHBOOK_CLIENT_KEY=sdk-<key>

    Fail-open: if GrowthBook is not configured, returns setup instructions.

    Args:
        name: Experiment name (e.g. "Pricing CTA — Trial vs Free")
        hypothesis: What you expect (e.g. "Changing CTA to 'Start Free' increases trial signups by 15%")
        metric: Primary metric to optimise (e.g. "signup_conversion", "trial_to_paid", "mrr_per_user")
        variants: List of variant labels — first is treated as control
                  (e.g. ["control", "variant_a"])
        traffic_split: Weight per variant (must sum to 1.0). Default: equal split.
    """
    client = _get_growthbook_client()
    result = client.create_experiment(
        name=name,
        hypothesis=hypothesis,
        metric=metric,
        variants=variants,
        traffic_split=traffic_split,
    )
    return json.dumps(result, indent=2)


@mcp.tool()
def get_experiment_results(
    experiment_id: str,
) -> str:
    """
    Fetch results for a running or completed A/B experiment from GrowthBook.

    Returns: per-variant conversion rates, relative uplift, p-value, winner,
    and a plain-language statistical recommendation (ship / run longer / inconclusive).

    Requires GrowthBook self-hosted with GROWTHBOOK_API_HOST and GROWTHBOOK_CLIENT_KEY.
    Fail-open: returns a not-configured message if GrowthBook is unreachable.

    Args:
        experiment_id: The experiment ID returned by create_ab_experiment()
    """
    client = _get_growthbook_client()
    result = client.get_experiment_results(experiment_id=experiment_id)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_experiments(
    status: str = "all",
) -> str:
    """
    List all A/B experiments from GrowthBook with their status and metrics.

    Returns a table of experiments: id, name, status (running/completed/stopped),
    hypothesis, primary metric, and variant count.

    Fail-open: returns empty list with a setup guide if GrowthBook is not configured.

    Args:
        status: Filter by status — "running", "completed", "stopped", or "all" (default)
    """
    client = _get_growthbook_client()

    if not client.is_configured():
        return json.dumps({
            "configured": False,
            "experiments": [],
            "message": (
                "GrowthBook not configured. "
                "Run: docker compose -f docker/growthbook-compose.yml up -d "
                "then set GROWTHBOOK_API_HOST and GROWTHBOOK_CLIENT_KEY."
            ),
            "setup_guide": "docs/setup/growthbook-setup.md",
        }, indent=2)

    experiments = client.list_experiments(status=status)
    return json.dumps({
        "status_filter": status,
        "count": len(experiments),
        "experiments": experiments,
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# Phase H: Observability — rate_recommendation
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def rate_recommendation(
    call_id: str,
    score: int,
    reason: str = "",
) -> str:
    """
    Rate a previous tool recommendation to improve future quality.

    Logs to Langfuse (if configured) for LLM quality tracking, and writes
    to the SQLite feedback table for local persistence.

    Use when: a council recommendation, pattern match, or strategic advice
    was helpful or unhelpful — this feedback improves the system over time.

    Langfuse self-hosted: docker compose -f docker/langfuse-compose.yml up -d
    Set: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST

    Fail-open: if Langfuse is not configured, writes to SQLite only.
    Fail-open: if neither is available, returns acknowledgement anyway.

    Args:
        call_id: The 8-char hex call_id from the tool log (visible in tool_calls.jsonl)
        score: Rating 1-5 (1 = very unhelpful, 3 = neutral, 5 = excellent / spot-on)
        reason: Optional explanation (e.g. "Council was too cautious given our traction")
    """
    stored = _rate_tool_call(call_id=call_id, score=score, reason=reason)
    return json.dumps({
        "call_id": call_id,
        "score": max(1, min(5, int(score))),
        "reason": reason or "",
        "stored": stored,
        "message": (
            "Feedback recorded — thank you. This helps calibrate future recommendations."
            if stored else
            "Feedback acknowledged (no persistent storage configured — "
            "set up Langfuse or ensure context_db is writable)."
        ),
    }, indent=2)

# ─────────────────────────────────────────────────────────────
# Autonomous AI tools (NS-0 + Next-1 + Next-2)
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def action_registry_status() -> str:
    """
    Get the current status of the autonomous action registry.
    Returns: permissions summary, kill switch state, daily usage, pending approvals.
    """
    from .core.action_registry import get_action_registry
    return json.dumps(get_action_registry().get_permissions_summary(), indent=2)


@mcp.tool()
def approve_action(request_id: str) -> str:
    """
    Approve a queued autonomous action (Tier 4+ or when autonomous_mode=false).

    Args:
        request_id: The request_id from list_pending_approvals
    """
    from .core.action_registry import get_action_registry
    result = get_action_registry().approve(request_id)
    return json.dumps({"status": result.status, "error": result.error, "result": result.result}, indent=2)


@mcp.tool()
def reject_action(request_id: str, reason: str = "") -> str:
    """
    Reject a queued autonomous action.

    Args:
        request_id: The request_id from list_pending_approvals
        reason: Optional reason for rejection
    """
    from .core.action_registry import get_action_registry
    get_action_registry().reject(request_id, reason=reason)
    return json.dumps({"status": "rejected", "request_id": request_id})


@mcp.tool()
def list_pending_approvals() -> str:
    """
    List all Tier 4+ actions awaiting human approval.
    Returns list of pending actions with their request IDs.
    """
    from .core.action_registry import get_action_registry
    return json.dumps(get_action_registry().get_pending_approvals(), indent=2)


@mcp.tool()
def get_audit_log_tool(hours: int = 24) -> str:
    """
    Get recent autonomous actions taken by the AI founder system.

    Args:
        hours: How many hours back to look (default 24)
    """
    from .core.audit_log import get_audit_log
    stats = get_audit_log().get_stats(hours=hours)
    recent = get_audit_log().query({"status": "executed"})[-20:]  # last 20 executed
    return json.dumps({"stats": stats, "recent_actions": recent}, indent=2, default=str)


@mcp.tool()
def set_autonomous_mode(enabled: bool) -> str:
    """
    Toggle autonomous mode. When disabled, all Tier 2+ actions queue for approval.
    This is the software kill switch (separate from the env var kill switch).

    Args:
        enabled: True = autonomous execution, False = all actions queue for approval
    """
    config_path = __import__("pathlib").Path.home() / ".soloos" / "permissions.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import yaml  # type: ignore[import]
        existing = {}
        if config_path.exists():
            with config_path.open() as f:
                existing = yaml.safe_load(f) or {}
        existing["autonomous_mode"] = enabled
        with config_path.open("w") as f:
            yaml.dump(existing, f)
        return json.dumps({"autonomous_mode": enabled, "config_path": str(config_path)})
    except ImportError:
        # Fallback: write minimal YAML manually
        content = f"autonomous_mode: {'true' if enabled else 'false'}\n"
        if config_path.exists():
            lines = config_path.read_text().splitlines()
            lines = [l for l in lines if not l.startswith("autonomous_mode:")]
            lines.append(content.strip())
            config_path.write_text("\n".join(lines) + "\n")
        else:
            config_path.write_text(content)
        return json.dumps({"autonomous_mode": enabled, "config_path": str(config_path)})


@mcp.tool()
def take_action(
    action_type: str,
    params: str,
    reasoning: str,
) -> str:
    """
    Execute an autonomous action via the ActionRegistry with full safety gating.
    All actions are permission-checked, kill-switch-gated, and audit-logged.

    Args:
        action_type: Action name (send_email, deploy, post_social, reply_support, manage_dns)
        params: JSON string of action parameters
        reasoning: Why this action is being taken (used in audit log)
    """
    import json as _json
    from .core.action_registry import get_action_registry, ActionRequest
    from .actions.email_action import EmailAction
    from .actions.deploy_action import DeployAction
    from .actions.social_action import SocialAction
    from .actions.support_action import SupportAction
    from .actions.dns_action import DnsAction
    from .core.action_registry import ActionDefinition, Tier

    registry = get_action_registry()

    # Register actions if not already registered
    _action_map = {
        "send_email": (EmailAction(), Tier.COMMUNICATE, True, 50),
        "deploy": (DeployAction(), Tier.DEPLOY, False, None),
        "post_social": (SocialAction(), Tier.COMMUNICATE, True, 3),
        "reply_support": (SupportAction(), Tier.COMMUNICATE, True, 100),
        "manage_dns": (DnsAction(), Tier.DEPLOY, False, None),
    }

    if action_type not in registry._actions:
        if action_type in _action_map:
            action_obj, tier, reversible, daily_limit = _action_map[action_type]
            registry.register_action(
                ActionDefinition(action_type, tier, action_type, reversible, daily_limit),
                action_obj.execute,
            )

    try:
        params_dict = _json.loads(params) if isinstance(params, str) else params
    except Exception:
        return json.dumps({"error": f"Invalid params JSON: {params}"})

    result = registry.execute(ActionRequest(
        action=action_type,
        params=params_dict,
        reasoning=reasoning,
        agent_id="mcp_caller",
    ))
    return json.dumps({
        "status": result.status,
        "result": result.result,
        "error": result.error,
        "request_id": result.request_id,
        "audit_id": result.audit_id,
    }, indent=2)


@mcp.tool()
def list_available_actions() -> str:
    """
    List all registered autonomous actions with their configuration status.
    Shows tier, daily limits, and whether each action is configured (API keys present).
    """
    from .core.action_registry import get_action_registry, Tier
    from .actions.email_action import EmailAction
    from .actions.deploy_action import DeployAction
    from .actions.social_action import SocialAction
    from .actions.support_action import SupportAction
    from .actions.dns_action import DnsAction

    actions_info = [
        {"name": "send_email", "tier": "COMMUNICATE", "tier_num": 2, "daily_limit": 50, "configured": EmailAction().is_configured()},
        {"name": "deploy", "tier": "DEPLOY", "tier_num": 4, "daily_limit": None, "configured": DeployAction().is_configured()},
        {"name": "post_social", "tier": "COMMUNICATE", "tier_num": 2, "daily_limit": 3, "configured": SocialAction().is_configured()},
        {"name": "reply_support", "tier": "COMMUNICATE", "tier_num": 2, "daily_limit": 100, "configured": SupportAction().is_configured()},
        {"name": "manage_dns", "tier": "DEPLOY", "tier_num": 4, "daily_limit": None, "configured": DnsAction().is_configured()},
    ]
    return json.dumps(actions_info, indent=2)


@mcp.tool()
def get_task_queue_status() -> str:
    """
    Get current status of the autonomous task queue.
    Shows pending, running, done, and failed task counts.
    """
    from .agent.task_queue import get_task_queue
    queue = get_task_queue()
    return json.dumps({
        "stats": queue.stats(),
        "pending": queue.list_pending()[:10],
    }, indent=2, default=str)


@mcp.tool()
def enqueue_task(
    task_type: str,
    payload: str = "{}",
    priority: int = 5,
    agent_id: str = "founder",
) -> str:
    """
    Manually enqueue a task for autonomous processing.

    Args:
        task_type: Task type (morning_brief, respond_support, review_pr, etc.)
        payload: JSON string of task parameters
        priority: 1=critical, 10=low (default 5)
        agent_id: Which agent should handle it (founder, marketing, engineering, customer_success)
    """
    import json as _json
    from .agent.task_queue import get_task_queue

    try:
        payload_dict = _json.loads(payload) if isinstance(payload, str) else payload
    except Exception:
        payload_dict = {"raw": payload}

    task_id = get_task_queue().enqueue(task_type, payload_dict, priority=priority, agent_id=agent_id)
    return json.dumps({"task_id": task_id, "task_type": task_type, "priority": priority})


@mcp.tool()
def run_founder_loop_once() -> str:
    """
    Run one iteration of the autonomous founder loop.
    Processes the highest-priority task from the queue.
    Kill switch is enforced — if active, this returns 'blocked'.
    """
    from .agent.founder_loop import get_founder_loop
    result = get_founder_loop().run_once()
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def get_world_model_snapshot() -> str:
    """
    Get the current world model — the AI's understanding of the business state.
    Includes metrics, goals, experiments, and agent state.
    """
    from .agent.world_model import get_world_model
    return json.dumps(get_world_model().get(), indent=2, default=str)


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

def _warn_missing_optional_deps() -> None:
    """
    Emit a one-time advisory to stderr for optional deps that the user has
    configured (env var set) but whose package is not installed.
    Only warns — never blocks startup.
    """
    import importlib
    import os

    _OPTIONAL_DEPS: list[tuple[str, str, str]] = [
        # (env_var_that_signals_intent, python_package, install_hint)
        ("STRIPE_API_KEY",         "stripe",       "pip install 'soloos-core[connectors]'"),
        ("MERCURY_API_TOKEN",      "httpx",        "pip install httpx"),
        ("POSTHOG_API_KEY",        "posthog",      "pip install posthog"),
        ("RESEND_API_KEY",         "resend",       "pip install resend"),
        ("SLACK_BOT_TOKEN",        "slack_sdk",    "pip install slack-sdk"),
    ]

    for env_var, package, hint in _OPTIONAL_DEPS:
        if not os.environ.get(env_var):
            continue
        try:
            importlib.import_module(package)
        except ImportError:
            print(
                f"[SoloOS] WARNING: {env_var} is set but '{package}' is not installed. "
                f"Run: {hint}",
                file=sys.stderr,
            )


def main() -> None:
    """
    CLI entry point for soloos-mcp script.

    Supports --transport flag to select MCP transport:
      stdio             — default, for Claude Code / Cursor / Windsurf (MCP clients)
      sse               — legacy SSE transport (n8n, older clients)
      streamable-http   — new MCP Streamable HTTP spec

    For REST/OpenAPI access (ChatGPT, LangChain, any HTTP client):
      Use 'soloos-api' command instead (gateway/http_bridge.py)
    """
    import sys

    transport = "stdio"
    for i, arg in enumerate(sys.argv[1:]):
        if arg in ("--transport", "-t") and i + 1 < len(sys.argv) - 1:
            transport = sys.argv[i + 2]
        elif arg.startswith("--transport="):
            transport = arg.split("=", 1)[1]

    valid = {"stdio", "sse", "streamable-http"}
    if transport not in valid:
        print(f"Unknown transport '{transport}'. Valid: {', '.join(valid)}", file=sys.stderr)
        sys.exit(1)

    _warn_missing_optional_deps()
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
