"""
SoloOS Core MCP Server

Transforms SoloOS from passive markdown into active founder intelligence tools.
Claude calls these tools instead of referencing markdown files.

Run: python -m soloos_core.server
Or:  uvx --from soloos-core soloos-mcp
"""

import json
import random
import math
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Annotated

from mcp.server.fastmcp import FastMCP

from .kb_loader import (
    get_patterns, get_founders, get_markets,
    search_patterns, search_founders, KB_ROOT,
)
from .log_manager import (
    load_log, append_log_entry, check_kill_signals,
    read_business_context, next_log_id,
    FounderLogEntry, today_str, due_date_str,
)

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
# TOOL 1: match_pattern
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

    # System 1 / System 2 routing signal
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


def _parse_reversibility(text: str) -> int:
    """Extract numeric reversibility score from text like '8/10' or '3/10'."""
    import re
    m = re.search(r"(\d+)/10", text)
    return int(m.group(1)) if m else 5


# ─────────────────────────────────────────────────────────────
# TOOL 2: search_founder_cases
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

    # Apply filters
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
# TOOL 3: check_market
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

    # Find best match
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


# ─────────────────────────────────────────────────────────────
# TOOL 4: calculate_ev
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_ev(
    activities: list[dict],
    use_monte_carlo: bool = False,
    simulations: int = 1000,
) -> str:
    """
    Calculate Expected Value (EV) per hour for competing activities.
    Ranks options by EV/hr to identify highest-leverage use of founder time.

    Use when: A founder is torn between two or more activities and needs
    to know which has the highest expected return per hour invested.

    Args:
        activities: List of dicts, each with:
            - name (str): Activity name
            - hours (float): Hours required
            - probability (float): Probability of positive outcome (0.0–1.0)
            - revenue_impact (float): Revenue impact if successful ($)
            - downside (float, optional): Revenue impact if fails (default 0)
        use_monte_carlo: Run Monte Carlo simulation for uncertainty ranges
        simulations: Number of Monte Carlo iterations (default 1000)

    Example:
        activities = [
            {"name": "Cold email 50 leads", "hours": 3, "probability": 0.12, "revenue_impact": 2400},
            {"name": "Write SEO article", "hours": 4, "probability": 0.05, "revenue_impact": 5000},
        ]
    """
    if not activities:
        return json.dumps({"error": "No activities provided"})

    results = []

    for act in activities:
        name = act.get("name", "Unnamed")
        hours = float(act.get("hours", 1))
        prob = float(act.get("probability", 0.5))
        revenue = float(act.get("revenue_impact", 0))
        downside = float(act.get("downside", 0))

        # Clamp probability
        prob = max(0.0, min(1.0, prob))
        hours = max(0.1, hours)

        # Simple EV
        ev = (prob * revenue) + ((1 - prob) * downside)
        ev_per_hour = ev / hours

        item = {
            "name": name,
            "hours": hours,
            "probability": f"{prob:.0%}",
            "revenue_impact": f"${revenue:,.0f}",
            "ev": f"${ev:,.0f}",
            "ev_per_hour": f"${ev_per_hour:,.0f}/hr",
            "ev_per_hour_raw": ev_per_hour,
        }

        if use_monte_carlo and simulations > 0:
            mc_results = _monte_carlo_ev(prob, revenue, downside, hours, simulations)
            item["monte_carlo"] = mc_results

        results.append(item)

    # Rank by EV/hr
    results.sort(key=lambda x: x["ev_per_hour_raw"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
        del r["ev_per_hour_raw"]

    winner = results[0]
    comparison = ""
    if len(results) >= 2:
        ratio = float(results[0]["ev"].replace("$", "").replace(",", "")) / max(
            1, float(results[1]["ev"].replace("$", "").replace(",", ""))
        )
        comparison = f"'{winner['name']}' has {ratio:.1f}x the expected value of the next best option."

    return json.dumps({
        "ranked_activities": results,
        "winner": winner["name"],
        "winner_ev_per_hour": winner["ev_per_hour"],
        "comparison": comparison,
        "caveat": (
            "EV/hr is not the only factor. Consider: asymmetric upside (viral loops), "
            "compounding effects (SEO vs one-time outreach), strategic positioning, and founder energy cost."
        ),
    }, indent=2)


def _monte_carlo_ev(prob: float, revenue: float, downside: float, hours: float, n: int) -> dict:
    """Run Monte Carlo simulation for EV uncertainty."""
    outcomes = []
    for _ in range(n):
        # Sample probability with uncertainty (±20%)
        sampled_prob = max(0, min(1, random.gauss(prob, prob * 0.2)))
        result = revenue if random.random() < sampled_prob else downside
        outcomes.append(result / hours)

    outcomes.sort()
    p10 = outcomes[int(0.10 * n)]
    p50 = outcomes[int(0.50 * n)]
    p90 = outcomes[int(0.90 * n)]

    return {
        "p10_pessimistic": f"${p10:,.0f}/hr",
        "p50_median": f"${p50:,.0f}/hr",
        "p90_optimistic": f"${p90:,.0f}/hr",
        "note": f"Monte Carlo ({n} simulations) with ±20% probability uncertainty",
    }


# ─────────────────────────────────────────────────────────────
# TOOL 5: log_decision
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def log_decision(
    summary: str,
    context: str,
    hypothesis: str,
    kill_signal: str,
    kill_signal_days: int = 30,
    outcome_days: int = 30,
    decision_type: str = "Decision",
    pattern_applied: str = "",
) -> str:
    """
    Log a strategic decision to founder-log.md with a hypothesis and kill signal.
    Creates a trackable FL-XXX entry in the personal pattern accrual system.

    Use after any significant founder decision — especially after /decide runs.
    The kill signal becomes a tracked, date-aware obligation, not just text.

    Args:
        summary: One sentence: what was decided
        context: What prompted this decision (signal, conversation, data)
        hypothesis: What you expect to happen as a result
        kill_signal: Specific, measurable data that would prove this decision wrong
        kill_signal_days: Days from now to check kill signal (default 30)
        outcome_days: Days from now to assess outcome (default 30)
        decision_type: Type tag — "Decision" / "Experiment" / "Pivot" / "Hire" / "Pricing"
        pattern_applied: Pattern ID if one was applied, e.g. "P-07"
    """
    entries = load_log()
    entry_id = next_log_id(entries)
    today = today_str()

    entry = FounderLogEntry(
        id=entry_id,
        date=today,
        type=decision_type,
        summary=summary,
        context=context,
        pattern_applied=pattern_applied or "None",
        hypothesis=hypothesis,
        kill_signal=kill_signal,
        kill_signal_due=due_date_str(kill_signal_days),
        outcome="[PENDING OUTCOME]",
        outcome_due=due_date_str(outcome_days),
        outcome_status="⏳ Pending",
    )

    append_log_entry(entry)

    return json.dumps({
        "logged": True,
        "entry_id": entry_id,
        "date": today,
        "summary": summary,
        "kill_signal": kill_signal,
        "kill_signal_due": due_date_str(kill_signal_days),
        "outcome_due": due_date_str(outcome_days),
        "message": f"Decision logged as {entry_id}. Kill signal check due in {kill_signal_days} days.",
        "ekg_reference": f"[[{entry_id}]]",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 6: check_kill_signals
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def check_kill_signals_tool() -> str:
    """
    Check all pending decisions in founder-log.md for overdue or approaching kill signals.
    This is the CHRONOS CHECK — fires at session start to surface what needs review.

    Returns: All pending entries ranked by urgency (OVERDUE → URGENT → WARNING → OK).
    Use at the start of every session to prevent decision drift and assumption debt.
    """
    entries = load_log()

    if not entries:
        return json.dumps({
            "status": "no_entries",
            "message": "No entries in founder-log.md yet. Use log_decision to start tracking.",
            "alerts": [],
        })

    pending = [e for e in entries if e.outcome_status == "⏳ Pending"]
    if not pending:
        return json.dumps({
            "status": "all_resolved",
            "total_entries": len(entries),
            "pending": 0,
            "message": "All decisions have outcomes logged. Clean slate.",
            "alerts": [],
        })

    alerts = check_kill_signals(entries)
    overdue = [a for a in alerts if a.urgency == "OVERDUE"]
    urgent = [a for a in alerts if a.urgency == "URGENT"]
    warning = [a for a in alerts if a.urgency == "WARNING"]

    formatted_alerts = []
    for a in alerts:
        formatted_alerts.append({
            "entry_id": a.entry_id,
            "urgency": a.urgency,
            "summary": a.summary,
            "kill_signal": a.kill_signal,
            "due_date": a.due_date,
            "days_remaining": a.days_remaining,
            "action_required": _kill_signal_action(a),
        })

    return json.dumps({
        "status": "alerts_found" if overdue or urgent else "monitoring",
        "total_pending": len(pending),
        "overdue": len(overdue),
        "urgent": len(urgent),
        "warning": len(warning),
        "session_start_message": _build_session_message(overdue, urgent, warning),
        "alerts": formatted_alerts,
    }, indent=2)


def _kill_signal_action(alert) -> str:
    if alert.urgency == "OVERDUE":
        return f"⛔ OVERDUE by {abs(alert.days_remaining)} days. Record outcome NOW to unlock clean session."
    elif alert.urgency == "URGENT":
        return f"🔴 {alert.days_remaining} days left. Schedule kill signal check this week."
    elif alert.urgency == "WARNING":
        return f"🟡 {alert.days_remaining} days left. Plan review before due date."
    return f"🟢 {alert.days_remaining} days remaining. No action needed."


def _build_session_message(overdue, urgent, warning) -> str:
    if overdue:
        return (f"⛔ KILL SIGNAL CHECK: {len(overdue)} decision(s) OVERDUE for outcome review. "
                f"Address these before any new work.")
    elif urgent:
        return f"🔴 {len(urgent)} kill signal(s) due within 7 days. Review before committing to new strategy."
    elif warning:
        return f"🟡 {len(warning)} kill signal(s) approaching (14 days). Good momentum."
    return "🟢 All kill signals on track. Clean session."


# ─────────────────────────────────────────────────────────────
# TOOL 7: get_stage_advice
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_stage_advice(
    mrr: str,
    question_topic: str = "",
) -> str:
    """
    Get stage-calibrated advice based on current MRR. Returns what to focus on,
    what NOT to do, which patterns are relevant, and what the biggest mistake is at this stage.

    Use when: Inferring a founder's stage from conversation clues, or when they state their MRR.
    This is the STAGE AUTO-DETECTION logic encoded as a callable tool.

    Args:
        mrr: Current MRR as string — "$0", "$3K", "$15K", "$40K", "$80K", "pre-revenue", etc.
        question_topic: What they're asking about (optional, for context-specific advice)
    """
    mrr_value = _parse_mrr_string(mrr)

    if mrr_value == 0:
        stage = "pre_revenue"
    elif mrr_value <= 5000:
        stage = "early_traction"
    elif mrr_value <= 20000:
        stage = "pmf_search"
    elif mrr_value <= 50000:
        stage = "scaling"
    else:
        stage = "growth"

    stage_data = _STAGE_PLAYBOOKS[stage]

    # Check for topic-specific flags
    flags = []
    topic_lower = question_topic.lower()
    if mrr_value < 5000 and any(k in topic_lower for k in ["seo", "content", "blog", "backlink"]):
        flags.append("⚠️ STAGE MISMATCH: SEO requires 6-12 months. At <$5K MRR, direct outreach generates faster ROI.")
    if mrr_value < 20000 and any(k in topic_lower for k in ["hire", "va", "team", "employee"]):
        flags.append("⚠️ PROCESS FIRST: Document the process before hiring. Hiring before documentation = chaos.")
    if mrr_value < 50000 and any(k in topic_lower for k in ["international", "expand", "global", "europe"]):
        flags.append("⚠️ PREMATURE: Fix home-market churn first. International expansion at $50K+ MRR.")
    if mrr_value < 10000 and any(k in topic_lower for k in ["paid ads", "facebook ads", "google ads", "ppc"]):
        flags.append("⚠️ UNIT ECONOMICS FIRST: Need LTV data before paid ads. What's your D30 retention?")

    return json.dumps({
        "mrr_input": mrr,
        "mrr_parsed": f"${mrr_value:,}",
        "stage": stage_data["name"],
        "primary_objective": stage_data["objective"],
        "what_to_focus": stage_data["focus"],
        "what_not_to_do": stage_data["avoid"],
        "biggest_mistake_at_stage": stage_data["biggest_mistake"],
        "key_patterns": stage_data["patterns"],
        "metric_to_watch": stage_data["metric"],
        "topic_flags": flags,
    }, indent=2)


def _parse_mrr_string(mrr_str: str) -> int:
    """Convert '$3.5K', '$40,000', 'pre-revenue', '0' to integer."""
    import re
    mrr_str = mrr_str.lower().strip()
    if any(x in mrr_str for x in ["0", "pre", "none", "nothing", "zero"]):
        return 0
    # Remove $ and commas
    cleaned = re.sub(r"[$,]", "", mrr_str)
    # Handle K suffix
    m = re.search(r"([\d.]+)\s*k", cleaned)
    if m:
        return int(float(m.group(1)) * 1000)
    # Handle plain number
    m = re.search(r"([\d,]+)", cleaned)
    if m:
        return int(m.group(1).replace(",", ""))
    return 0


_STAGE_PLAYBOOKS = {
    "pre_revenue": {
        "name": "$0 MRR — Pre-Revenue",
        "objective": "5 paid commitments before writing a single line of production code.",
        "focus": [
            "Customer discovery: 20 conversations with target ICP",
            "Validation: 5 Tier 4+ commitments (LOI or pre-payment)",
            "Manual version first (Levels Test): can this be a spreadsheet/form today?",
            "ChatGPT substitution test: does free AI already do this?",
        ],
        "avoid": [
            "Building anything for >2 weeks without 5 commitments",
            "Brand design, logo, admin dashboard",
            "SEO, content marketing, paid ads",
            "Team building, hiring, VAs",
            "Productizing before validating demand",
        ],
        "biggest_mistake": "Building in stealth for 3+ months without a single customer conversation.",
        "patterns": ["P01 (Levels Test)", "P07 (Narrow ICP)", "P02 (Marc Lou Kill Test)", "P08 (Distribution First)"],
        "metric": "Number of paid pre-commitments (target: 5 before build)",
    },
    "early_traction": {
        "name": "$1–5K MRR — Early Traction",
        "objective": "Find PMF signal: can you retain 40% of customers at Day 30?",
        "focus": [
            "Weekly calls with every paying customer (5 minutes minimum)",
            "D30 retention: if <40%, fix retention before acquiring more",
            "Identify the 1-2 customers who get the most value — serve them exclusively",
            "Direct outreach (DMs, cold email) for acquisition — not channels",
        ],
        "avoid": [
            "Adding new features before understanding why current users churn",
            "Expanding to a second ICP",
            "SEO, content, paid ads",
            "Redesign or rebrand",
            "Optimizing conversion before product retention is proven",
        ],
        "biggest_mistake": "Building new features instead of talking to churned users about why they left.",
        "patterns": ["P07 (Narrow ICP)", "P05 (Pricing Model)", "P11 (Community Distribution)", "P08 (Distribution First)"],
        "metric": "D30 retention rate (target: ≥40%). Monthly churn rate (target: <10%).",
    },
    "pmf_search": {
        "name": "$5–20K MRR — PMF Search",
        "objective": "Make acquisition repeatable: can you do this 10 more times?",
        "focus": [
            "Systematize the sales process that got you here (document every step)",
            "Identify your single strongest acquisition channel (double it)",
            "First hire: customer success or operations (free founder time for revenue)",
            "Begin SEO/content if organic searches already happening",
        ],
        "avoid": [
            "New ICPs or new products",
            "Fundraising (too early for most)",
            "Major product pivots",
            "Enterprise sales without proven sales process",
        ],
        "biggest_mistake": "Thinking $15K MRR = PMF. PMF = 40% 'very disappointed' score on Sean Ellis test.",
        "patterns": ["P06 (Compliance Moat)", "P04 (Viral Output)", "P10 (Pieter Levels Flywheel)"],
        "metric": "Sean Ellis score (target: ≥40% 'very disappointed'). Net Revenue Retention (target: >100%).",
    },
    "scaling": {
        "name": "$20–50K MRR — Scaling",
        "objective": "Systematize operations. Hire to documented processes. One channel at a time.",
        "focus": [
            "First hire: the function consuming most of your time",
            "SOPs for support, onboarding, and sales before hiring",
            "Channel diversification: if 1 channel works, add 1 more (not 3 more)",
            "Pricing optimization: probably undercharging — run price test",
        ],
        "avoid": [
            "Multiple simultaneous channel experiments",
            "International expansion",
            "Adding a second product",
            "Micromanaging new hires",
        ],
        "biggest_mistake": "Hiring without SOPs. Generating chaos instead of leverage.",
        "patterns": ["P06 (Compliance Moat)", "P04 (Viral Output)", "P08 (Distribution)"],
        "metric": "Revenue per employee. Support ticket resolution time. NPS score.",
    },
    "growth": {
        "name": "$50K+ MRR — Growth",
        "objective": "Portfolio management. Systems, team, and channel scaling.",
        "focus": [
            "Team: hire senior people who replace you in key functions",
            "Geographic expansion (now viable)",
            "Enterprise tier if ACV supports sales motion",
            "Build compounding assets: SEO, brand, community",
        ],
        "avoid": [
            "Doing everything yourself (unsustainable past this stage)",
            "Ignoring team retention",
            "Optimizing for vanity metrics vs revenue retention",
        ],
        "biggest_mistake": "Founder still doing everything solo. Leverage requires letting go.",
        "patterns": ["P04 (Viral Output)", "P10 (Levels Flywheel)", "P08 (Distribution)"],
        "metric": "Net Revenue Retention (target: >120%). CAC Payback period (target: <12 months).",
    },
}


# ─────────────────────────────────────────────────────────────
# TOOL 8: session_synthesis
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def session_synthesis(
    decisions_made: list[str],
    open_questions: list[str],
    assumptions_made: list[str],
    next_action: str,
    auto_log_decisions: bool = True,
) -> str:
    """
    Generate a structured SESSION WRAP at the end of a working session.
    Optionally creates founder-log stubs for decisions made (for kill signal tracking).

    Use automatically at end of any session containing strategic decisions,
    experiments, or pivots. This closes the EDE loop.

    Args:
        decisions_made: List of specific decisions made this session (not discussed, MADE)
        open_questions: What still needs answering before next session
        assumptions_made: What was assumed without data confirmation
        next_action: Single most important next step (named, sequenced, specific)
        auto_log_decisions: If True, create FL-XXX stubs for each decision
    """
    today = today_str()

    output = {
        "session_date": today,
        "session_wrap": {
            "decisions": decisions_made,
            "open_questions": open_questions,
            "assumptions_made": assumptions_made,
            "next_action": next_action,
        },
        "logged_entries": [],
        "formatted_output": "",
    }

    # Generate formatted markdown wrap
    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"SESSION WRAP — {today}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "DECISIONS:",
    ]
    for d in decisions_made:
        lines.append(f"  ✓ {d}")

    if open_questions:
        lines.append("")
        lines.append("OPEN QUESTIONS:")
        for q in open_questions:
            lines.append(f"  ? {q}")

    if assumptions_made:
        lines.append("")
        lines.append("ASSUMPTIONS MADE (UNCONFIRMED):")
        for a in assumptions_made:
            lines.append(f"  ⚠️ {a}")

    lines.extend([
        "",
        "NEXT:",
        f"  → {next_action}",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ])

    output["formatted_output"] = "\n".join(lines)

    # Auto-log each decision as a stub
    if auto_log_decisions and decisions_made:
        entries = load_log()
        for decision in decisions_made:
            entry_id = next_log_id(entries)
            stub = FounderLogEntry(
                id=entry_id,
                date=today,
                type="Decision",
                summary=decision,
                context=f"Session on {today}",
                pattern_applied="See session context",
                hypothesis="TBD — add hypothesis to complete this entry",
                kill_signal="TBD — add kill signal before next session",
                kill_signal_due=due_date_str(30),
                outcome="[PENDING OUTCOME]",
                outcome_due=due_date_str(30),
                outcome_status="⏳ Pending",
            )
            append_log_entry(stub)
            entries.append(stub)  # Update local state for next ID
            output["logged_entries"].append({
                "entry_id": entry_id,
                "decision": decision,
                "note": "Kill signal is TBD — update founder-log.md before next session",
            })

    return json.dumps(output, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 9: get_business_context
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_business_context() -> str:
    """
    Read the founder's business-context.md and return structured current state.
    Use at session start to get context before giving advice.

    Returns: MRR, ICP, stage, top channel, biggest challenge, open decisions.
    If no context file exists, returns guidance on running /onboard.
    """
    ctx = read_business_context()
    from .log_manager import BUSINESS_CONTEXT_PATH, FOUNDER_LOG_PATH
    ctx["soloos_version"] = "v3"
    ctx["context_files_checked"] = [str(BUSINESS_CONTEXT_PATH), str(FOUNDER_LOG_PATH)]
    return json.dumps(ctx, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 10: validate_idea_gates
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def validate_idea_gates(
    idea: str,
    category: str = "",
    self_is_customer: bool = False,
    heard_from_customers: int = 0,
    competing_solutions: list[str] | None = None,
    target_price: float = 0,
    problem_monthly_cost: float = 0,
) -> str:
    """
    Run an idea through SoloOS validation gates (Gate 0: ChatGPT Substitution + Gates 1-4).
    Returns structured pass/fail for each gate with specific next actions.

    Use when a founder says "thinking about building X" or "I want to add X".
    This is the /validate skill encoded as a callable tool.

    Args:
        idea: The product idea or feature description
        category: Market category (for Gate 0 and saturation check)
        self_is_customer: True if founder personally experiences this problem
        heard_from_customers: Number of customers who described this pain unprompted
        competing_solutions: List of known paid alternatives
        target_price: Intended price ($/month) — 0 if unknown
        problem_monthly_cost: What does this problem cost the customer per month?
    """
    gates = {}

    # Gate 0: ChatGPT Substitution Test
    ai_keywords = ["ai", "write", "generate", "summarize", "translate", "analyze", "classify", "extract"]
    idea_lower = idea.lower()
    chatgpt_risk = sum(1 for kw in ai_keywords if kw in idea_lower)
    if chatgpt_risk >= 2:
        gates["gate_0_chatgpt"] = {
            "status": "⚠️ HIGH_RISK",
            "finding": "Core function overlaps with free LLM capabilities.",
            "test_required": "Open ChatGPT free tier. Ask it to perform your product's core function right now.",
            "if_passes": "Document the specific gap — that gap IS your product.",
            "if_fails": "Find narrower niche with compliance/integration moat, or find workflow step LLM alone can't complete.",
        }
    else:
        gates["gate_0_chatgpt"] = {
            "status": "✅ LOW_RISK",
            "finding": "Idea doesn't appear to be easily substituted by a free LLM.",
            "note": "Still run the 5-minute test before proceeding.",
        }

    # Arvid Kahl Rule check
    kahl_status = "✅ PASS" if heard_from_customers >= 3 else "⚠️ UNCLEAR"
    gates["kahl_rule"] = {
        "status": kahl_status,
        "heard_from": heard_from_customers,
        "required": 3,
        "finding": (
            "3+ customers described this pain in their own words — origin validated."
            if heard_from_customers >= 3
            else f"Only {heard_from_customers} unprompted customer descriptions. Need 3+ before building."
        ),
        "action": None if heard_from_customers >= 3 else "Spend 2hrs in target community listening before validating idea you invented.",
    }

    # Self-as-customer shortcut
    gates["self_as_customer"] = {
        "applies": self_is_customer,
        "verdict": (
            "SHORTCUT AVAILABLE: You experience this problem. Skip Gates 1-2. "
            "Document your painful workflow first, then validate others will pay (Gate 3)."
            if self_is_customer
            else "Founder is not a direct customer. All 4 gates required."
        ),
    }

    # Gate 1: Problem Existence
    g1_score = min(heard_from_customers * 30, 100)
    if self_is_customer:
        g1_score = max(g1_score, 70)
    gates["gate_1_problem"] = {
        "status": "✅ PASS" if g1_score >= 60 else ("⚠️ UNCLEAR" if g1_score >= 30 else "❌ FAIL"),
        "score": f"{g1_score}%",
        "finding": f"{heard_from_customers} customer pain confirmations" + (" + self-experience" if self_is_customer else ""),
        "gap": "Need 3+ unprompted customer pain descriptions" if g1_score < 60 else None,
    }

    # Gate 2: Market Signal
    has_paid_alternatives = bool(competing_solutions)
    g2_status = "✅ PASS" if has_paid_alternatives else "⚠️ UNCLEAR"
    gates["gate_2_market"] = {
        "status": g2_status,
        "competing_solutions": competing_solutions or [],
        "demand_signal": "Strong — people pay for inadequate alternatives" if has_paid_alternatives else "Unknown — no confirmed paid alternatives",
        "gap": "Research what people currently pay for. If nothing exists, demand may not exist." if not has_paid_alternatives else None,
    }

    # Gate 3: Commitments
    gates["gate_3_commitments"] = {
        "status": "⚠️ PENDING",
        "required": "5 Tier 4+ commitments (LOI or pre-payment)",
        "tiers": {
            "tier_4_loi": "B2B: 'Would you sign a letter of intent to pay $X/month if it does Y?'",
            "tier_5_prepayment": "B2C: 'Founding member price is $X. 50 spots only.'",
        },
        "script": f"'We're building {idea[:60]}. Would you commit to paying ${target_price or 'X'}/month if it does [specific outcome]?'",
        "timeline": "Target: 5 commitments within 14 days from 20 direct outreach attempts",
    }

    # Gate 4: Unit Economics
    if target_price > 0 and problem_monthly_cost > 0:
        price_ratio = target_price / problem_monthly_cost
        if price_ratio < 0.10:
            pricing_verdict = "✅ UNDERCHARGING — Price is <10% of problem cost. Raise it."
            pricing_status = "⚠️ WARNING"
        elif price_ratio > 0.50:
            pricing_verdict = "⚠️ HIGH — Price is >50% of alternatives cost. Need strong ROI justification."
            pricing_status = "⚠️ WARNING"
        else:
            pricing_verdict = "✅ PASS — Price is in the sweet spot (10-50% of problem cost)."
            pricing_status = "✅ PASS"
    elif target_price > 0:
        pricing_status = "⚠️ UNCLEAR"
        pricing_verdict = "Problem monthly cost unknown. Can't validate price-to-value ratio."
    else:
        pricing_status = "❌ FAIL"
        pricing_verdict = "No price set. Pricing paralysis = revenue never starts. Set a price NOW."

    gates["gate_4_unit_economics"] = {
        "status": pricing_status,
        "target_price": f"${target_price}/mo" if target_price else "Not set",
        "problem_cost": f"${problem_monthly_cost}/mo" if problem_monthly_cost else "Unknown",
        "verdict": pricing_verdict,
        "floor": f"${max(target_price * 0.7, 9):.0f}/mo" if target_price else "Unknown",
        "ceiling_test": f"${target_price * 2:.0f}/mo" if target_price else "Unknown",
    }

    # Overall verdict
    fails = [k for k, v in gates.items()
             if isinstance(v, dict) and v.get("status", "").startswith("❌")]
    unclear = [k for k, v in gates.items()
               if isinstance(v, dict) and v.get("status", "").startswith("⚠️")]

    if fails:
        overall = "🔴 DO NOT BUILD"
        next_step = f"Fix failing gate(s): {', '.join(fails)} before building anything."
    elif len(unclear) <= 1:
        overall = "🟢 BUILD"
        next_step = "All gates pass. Build minimum viable version. Ship in ≤2 weeks."
    else:
        overall = "🟡 VALIDATE FIRST"
        next_step = f"Clear these gates before building: {', '.join(unclear[:2])}"

    return json.dumps({
        "idea": idea,
        "overall_verdict": overall,
        "next_step": next_step,
        "gates": gates,
        "time_to_validate": "7-14 days (3hrs/day)" if overall == "🟡 VALIDATE FIRST" else "N/A",
        "minimum_viable_version": f"Manual/concierge version of '{idea[:50]}' first" if overall != "🔴 DO NOT BUILD" else "Do not build until gates pass",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 11: knowledge_base_stats
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def knowledge_base_stats() -> str:
    """
    Return statistics about the loaded SoloOS knowledge base.
    Use to verify the server is connected to the right knowledge base files.
    """
    patterns = get_patterns()
    founders = get_founders()
    markets = get_markets()
    entries = load_log()

    return json.dumps({
        "status": "connected",
        "knowledge_base_root": str(KB_ROOT),
        "patterns_loaded": len(patterns),
        "pattern_categories": list({p.category for p in patterns}),
        "founder_cases_loaded": len(founders),
        "founders_indexed": list({c.founder for c in founders if c.founder != "Unknown"}),
        "market_categories_loaded": len(markets),
        "founder_log_entries": len(entries),
        "pending_outcomes": sum(1 for e in entries if e.outcome_status == "⏳ Pending"),
        "version": "soloos-core v1.0.0",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 12: calculate_unit_economics
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_unit_economics(
    arpu: float,
    monthly_churn_rate: float,
    gross_margin_pct: float = 80.0,
    cac: float = 0.0,
    monthly_expansion_mrr: float = 0.0,
) -> str:
    """
    Calculate the full unit economics stack for a SaaS business.
    Returns LTV (3 methods), LTV:CAC ratio, CAC payback, and health assessment.

    Use when: Any pricing or acquisition decision, fundraising prep, or financial health check.
    The Finance Engine auto-triggers this before any pricing recommendation.

    Args:
        arpu: Average Revenue Per User (monthly, in dollars)
        monthly_churn_rate: Monthly churn as decimal (0.05 = 5%)
        gross_margin_pct: Gross margin percentage (default 80 for SaaS)
        cac: Cost to Acquire one Customer (0 = not provided)
        monthly_expansion_mrr: Monthly expansion revenue per customer (for NRR >100% businesses)
    """
    if monthly_churn_rate <= 0:
        monthly_churn_rate = 0.001  # avoid divide by zero

    gm = gross_margin_pct / 100.0

    # LTV method 1: Simple
    ltv_simple = arpu / monthly_churn_rate

    # LTV method 2: Gross-margin adjusted
    ltv_gm = (arpu * gm) / monthly_churn_rate

    # LTV method 3: With expansion revenue
    ltv_expansion = ((arpu * gm) + monthly_expansion_mrr) / monthly_churn_rate

    # LTV:CAC
    ltv_cac_ratio = None
    cac_payback_months = None
    if cac > 0:
        ltv_cac_ratio = round(ltv_gm / cac, 2)
        cac_payback_months = round(cac / (arpu * gm), 1) if arpu * gm > 0 else None

    # NRR estimate
    nrr = (arpu + monthly_expansion_mrr - (arpu * monthly_churn_rate)) / arpu * 100

    # Health assessment
    health = []
    if ltv_cac_ratio is not None:
        if ltv_cac_ratio < 2:
            health.append("🔴 DANGER: LTV:CAC <2x — acquiring customers is destroying value")
        elif ltv_cac_ratio < 3:
            health.append("🟡 WARNING: LTV:CAC 2-3x — barely viable, tighten CAC or improve LTV")
        elif ltv_cac_ratio < 5:
            health.append("🟢 HEALTHY: LTV:CAC 3-5x — standard SaaS, scale confidently")
        else:
            health.append("🚀 EXCELLENT: LTV:CAC >5x — strong unit economics, accelerate acquisition")

    if monthly_churn_rate > 0.10:
        health.append("🔴 CHURN CRISIS: >10%/mo — fix retention before any acquisition spend")
    elif monthly_churn_rate > 0.05:
        health.append("🟡 CHURN WARNING: 5-10%/mo — investigate top churn reasons immediately")
    elif monthly_churn_rate < 0.02:
        health.append("🟢 EXCELLENT RETENTION: <2%/mo churn — strong foundation")

    if cac_payback_months is not None:
        if cac_payback_months > 18:
            health.append("🔴 CAC PAYBACK >18mo — high risk, reduce acquisition spend")
        elif cac_payback_months > 12:
            health.append("🟡 CAC PAYBACK 12-18mo — monitor closely")
        else:
            health.append("🟢 CAC PAYBACK <12mo — healthy, scale acquisition")

    if nrr > 110:
        health.append("🚀 NRR >110% — customers expand automatically (elite signal)")
    elif nrr > 100:
        health.append("🟢 NRR >100% — net negative churn (strong PMF signal)")
    elif nrr < 90:
        health.append("🔴 NRR <90% — revenue shrinking from existing customers (retention crisis)")

    return json.dumps({
        "inputs": {
            "arpu_monthly": f"${arpu:.2f}",
            "monthly_churn": f"{monthly_churn_rate*100:.1f}%",
            "gross_margin": f"{gross_margin_pct:.0f}%",
            "cac": f"${cac:.2f}" if cac > 0 else "not provided",
            "monthly_expansion": f"${monthly_expansion_mrr:.2f}",
        },
        "ltv_methods": {
            "method_1_simple": f"${ltv_simple:.0f}  (ARPU ÷ churn — use pre-PMF)",
            "method_2_gm_adjusted": f"${ltv_gm:.0f}  (ARPU × GM ÷ churn — use post-PMF)",
            "method_3_with_expansion": f"${ltv_expansion:.0f}  ((ARPU×GM + expansion) ÷ churn — use if NRR>100%)",
        },
        "ratios": {
            "ltv_cac": f"{ltv_cac_ratio}x" if ltv_cac_ratio else "CAC not provided",
            "cac_payback_months": cac_payback_months,
            "nrr_estimate": f"{nrr:.1f}%",
            "annual_churn": f"{(1-(1-monthly_churn_rate)**12)*100:.1f}%",
        },
        "health_assessment": health,
        "break_even_customers": round(cac / (arpu * gm), 1) if cac > 0 and arpu * gm > 0 else None,
        "action": "Fix retention before acquisition" if monthly_churn_rate > 0.05 else "Unit economics healthy — scale acquisition",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 13: calculate_valuation
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_valuation(
    arr: float,
    yoy_growth_rate_pct: float,
    nrr_pct: float = 100.0,
    gross_margin_pct: float = 80.0,
    monthly_churn_rate: float = 3.0,
    is_bootstrapped: bool = True,
    sde_annual: float = 0.0,
) -> str:
    """
    Multi-method company valuation for bootstrapped SaaS / micro-SaaS founders.
    Uses ARR multiple, Acquirer ROI, and SDE multiple methods simultaneously.

    Use when: Considering exit, fundraising, taking on investors, or just knowing your number.
    The Finance Engine auto-triggers this on valuation questions.

    Args:
        arr: Annual Recurring Revenue in dollars
        yoy_growth_rate_pct: Year-over-year growth rate (50 = 50%)
        nrr_pct: Net Revenue Retention percentage (100 = flat, 110 = 10% expansion)
        gross_margin_pct: Gross margin percentage (default 80 for SaaS)
        monthly_churn_rate: Monthly churn rate percentage (3 = 3%)
        is_bootstrapped: True if bootstrapped (clean cap table premium)
        sde_annual: Annual Seller Discretionary Earnings (0 = not calculated)
    """
    mrr = arr / 12

    # Method 1: ARR multiple
    if yoy_growth_rate_pct < 20:
        base_multiple_low, base_multiple_high = 2, 4
    elif yoy_growth_rate_pct < 50:
        base_multiple_low, base_multiple_high = 4, 8
    elif yoy_growth_rate_pct < 100:
        base_multiple_low, base_multiple_high = 8, 12
    else:
        base_multiple_low, base_multiple_high = 12, 20

    # Adjustments
    nrr_adj = 0
    if nrr_pct > 120:
        nrr_adj = 3
    elif nrr_pct > 110:
        nrr_adj = 2
    elif nrr_pct > 100:
        nrr_adj = 1
    elif nrr_pct < 90:
        nrr_adj = -2

    gm_adj = 0
    if gross_margin_pct > 80:
        gm_adj = 1
    elif gross_margin_pct < 60:
        gm_adj = -2

    bootstrap_adj = 0.5 if is_bootstrapped else 0

    adj_multiple_low = base_multiple_low + nrr_adj + gm_adj + bootstrap_adj
    adj_multiple_high = base_multiple_high + nrr_adj + gm_adj + bootstrap_adj
    adj_multiple_low = max(1, adj_multiple_low)

    valuation_arr_low = arr * adj_multiple_low
    valuation_arr_high = arr * adj_multiple_high
    valuation_arr_midpoint = arr * ((adj_multiple_low + adj_multiple_high) / 2)

    # Method 2: Acquirer ROI (strategic buyer)
    acquirer_typical_multiple = 10  # public SaaS trades at ~10x ARR
    strategic_max = arr * acquirer_typical_multiple
    typical_bootstrapped_deal = arr * 4  # typical bootstrapped acquisition price

    # Method 3: SDE multiple (for profitable bootstrapped)
    sde_result = None
    if sde_annual > 0:
        sde_multiple_low, sde_multiple_high = 2.5, 4.0
        sde_result = {
            "sde_annual": f"${sde_annual:,.0f}",
            "sde_multiple_range": f"{sde_multiple_low}x - {sde_multiple_high}x",
            "sde_valuation_low": f"${sde_annual * sde_multiple_low:,.0f}",
            "sde_valuation_high": f"${sde_annual * sde_multiple_high:,.0f}",
        }

    # Biggest value levers
    levers = []
    if nrr_pct < 100:
        levers.append("🔴 NRR <100%: Fix net revenue retention first — this is the #1 multiple driver")
    if nrr_pct >= 100 and nrr_pct < 110:
        levers.append("💡 Increasing NRR from 100% to 110% adds ~2x to your multiple")
    if monthly_churn_rate > 3:
        levers.append("🔴 Reduce monthly churn below 3% — churn directly compresses multiples")
    if gross_margin_pct < 70:
        levers.append("💡 Gross margin below 70% — each point improvement adds ~$X to valuation")
    if yoy_growth_rate_pct < 20:
        levers.append("💡 Sub-20% growth → 2-4x ARR. Accelerating to 50%+ unlocks 4-8x ARR")

    return json.dumps({
        "inputs": {
            "arr": f"${arr:,.0f}",
            "mrr": f"${mrr:,.0f}",
            "yoy_growth": f"{yoy_growth_rate_pct:.0f}%",
            "nrr": f"{nrr_pct:.0f}%",
            "gross_margin": f"{gross_margin_pct:.0f}%",
            "is_bootstrapped": is_bootstrapped,
        },
        "method_1_arr_multiple": {
            "base_multiple": f"{base_multiple_low}x - {base_multiple_high}x (from growth rate)",
            "nrr_adjustment": f"+{nrr_adj}x" if nrr_adj >= 0 else f"{nrr_adj}x",
            "gm_adjustment": f"+{gm_adj}x" if gm_adj >= 0 else f"{gm_adj}x",
            "bootstrap_adjustment": f"+{bootstrap_adj}x (clean cap table)" if is_bootstrapped else "0x",
            "adjusted_multiple": f"{adj_multiple_low:.1f}x - {adj_multiple_high:.1f}x",
            "valuation_range": f"${valuation_arr_low:,.0f} - ${valuation_arr_high:,.0f}",
            "midpoint": f"${valuation_arr_midpoint:,.0f}",
        },
        "method_2_acquirer_roi": {
            "strategic_buyer_max": f"${strategic_max:,.0f} (if acquirer trades at 10x ARR)",
            "typical_bootstrapped_deal": f"${typical_bootstrapped_deal:,.0f} (3-5x ARR for bootstrapped)",
            "note": "Strategic acquirers pay more when you have proprietary data/distribution/ICP they can't build",
        },
        "method_3_sde_multiple": sde_result or "Provide sde_annual for SDE-based valuation",
        "recommendation": f"Use ${valuation_arr_midpoint:,.0f} as your anchor number in conversations",
        "biggest_value_levers": levers,
        "key_insight": "NRR is the single biggest multiple driver. 110% NRR businesses sell at 2-3x higher multiples than 95% NRR businesses at identical ARR.",
        "acquirers_to_target": [
            "Micro-PE: Tiny Capital, Calm Company Fund, Relay Commerce (3-5x ARR)",
            "Marketplaces: Acquire.com, Flippa, Empire Flippers (1-5x ARR)",
            "Strategic: Your largest customers or top 3 competitors (4-10x ARR)",
            "PE: Searchfunder, independent sponsors (>$500K ARR threshold, 3-6x ARR)",
        ],
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 14: score_pmf
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def score_pmf(
    sean_ellis_pct: float = 0.0,
    nrr_pct: float = 0.0,
    l30_retention_pct: float = 0.0,
    referral_pct_of_signups: float = 0.0,
    monthly_churn_pct: float = 0.0,
    weeks_since_launch: int = 0,
    paying_customers: int = 0,
) -> str:
    """
    Score Product-Market Fit across 5 measurement systems. Returns PMF stage,
    what's blocking PMF, and specific actions to accelerate finding PMF.

    Use when: Founder asks "do I have PMF?", "should I scale?", or "is this working?"
    The PMF Engine auto-triggers this before any scaling recommendation.

    Args:
        sean_ellis_pct: % of users who say "Very Disappointed" if product disappeared (target >40%)
        nrr_pct: Net Revenue Retention % (target >100%)
        l30_retention_pct: Day 30 retention % (target varies by product type)
        referral_pct_of_signups: % of new users from referral/WOM (target >20%)
        monthly_churn_pct: Monthly churn % (target <2% for strong PMF)
        weeks_since_launch: How long since launch (context for expectations)
        paying_customers: Number of paying customers (minimum 40 needed for Sean Ellis)
    """
    score = 0
    max_score = 0
    signals = []
    gaps = []

    # Sean Ellis score
    if sean_ellis_pct > 0:
        max_score += 30
        if sean_ellis_pct >= 40:
            score += 30
            signals.append(f"✅ Sean Ellis: {sean_ellis_pct:.0f}% (>40% = PMF confirmed)")
        elif sean_ellis_pct >= 30:
            score += 18
            signals.append(f"🟡 Sean Ellis: {sean_ellis_pct:.0f}% (approaching PMF, need 40%+)")
            gaps.append("Sean Ellis below 40% — interview 'somewhat disappointed' users about their core use case")
        else:
            score += 5
            signals.append(f"🔴 Sean Ellis: {sean_ellis_pct:.0f}% (far from PMF threshold of 40%)")
            gaps.append(f"Sean Ellis at {sean_ellis_pct:.0f}% — major value gap. Find bright spots: who ARE the 'very disappointed'? Build for them exclusively.")

    # NRR
    if nrr_pct > 0:
        max_score += 25
        if nrr_pct >= 110:
            score += 25
            signals.append(f"✅ NRR: {nrr_pct:.0f}% (>110% = customers expand automatically = elite PMF signal)")
        elif nrr_pct >= 100:
            score += 18
            signals.append(f"🟢 NRR: {nrr_pct:.0f}% (>100% = net negative churn = strong PMF signal)")
        elif nrr_pct >= 90:
            score += 10
            signals.append(f"🟡 NRR: {nrr_pct:.0f}% (90-100% = acceptable, not exciting)")
            gaps.append("NRR below 100% — identify expansion opportunities: usage limits, seat expansion, premium features")
        else:
            score += 0
            signals.append(f"🔴 NRR: {nrr_pct:.0f}% (<90% = revenue shrinking from existing base = PMF not found)")
            gaps.append("NRR below 90% — STOP acquisition. Fix why customers are downgrading or churning first.")

    # L30 retention
    if l30_retention_pct > 0:
        max_score += 25
        if l30_retention_pct >= 40:
            score += 25
            signals.append(f"✅ D30 Retention: {l30_retention_pct:.0f}% (>40% = strong habit formation)")
        elif l30_retention_pct >= 25:
            score += 15
            signals.append(f"🟡 D30 Retention: {l30_retention_pct:.0f}% (25-40% = moderate, improve onboarding)")
            gaps.append("D30 retention 25-40% — map the 'boring middle' between signup and first value. What's the Aha moment? Reduce time-to-value.")
        else:
            score += 0
            signals.append(f"🔴 D30 Retention: {l30_retention_pct:.0f}% (<25% = activation failure)")
            gaps.append(f"D30 retention at {l30_retention_pct:.0f}% — critical activation problem. Do 5 user copilot sessions this week. Watch them use the product. You'll find the drop-off point.")

    # Referral %
    if referral_pct_of_signups > 0:
        max_score += 10
        if referral_pct_of_signups >= 20:
            score += 10
            signals.append(f"✅ Referral: {referral_pct_of_signups:.0f}% from WOM (>20% = organic growth loop)")
        elif referral_pct_of_signups >= 10:
            score += 5
            signals.append(f"🟡 Referral: {referral_pct_of_signups:.0f}% from WOM (building referral momentum)")
        else:
            signals.append(f"🔴 Referral: {referral_pct_of_signups:.0f}% from WOM (<10% = people not talking about it)")
            gaps.append("Low WOM — customers aren't motivated to share. Are results transformational? If not, find the bright spots (top 20% power users) and rebuild for them.")

    # Monthly churn
    if monthly_churn_pct > 0:
        max_score += 10
        if monthly_churn_pct < 2:
            score += 10
            signals.append(f"✅ Monthly Churn: {monthly_churn_pct:.1f}% (excellent retention)")
        elif monthly_churn_pct < 5:
            score += 6
            signals.append(f"🟡 Monthly Churn: {monthly_churn_pct:.1f}% (acceptable, optimize)")
        else:
            score += 0
            signals.append(f"🔴 Monthly Churn: {monthly_churn_pct:.1f}% (>5% = leaky bucket)")
            gaps.append(f"Monthly churn at {monthly_churn_pct:.1f}% — exit interviews on every churned customer. The pattern will emerge after 5-10 interviews.")

    # PMF stage verdict
    pmf_score_pct = (score / max_score * 100) if max_score > 0 else 0
    if pmf_score_pct >= 80:
        verdict = "🚀 STRONG PMF — Scale acquisition confidently"
        stage = "PMF_CONFIRMED"
    elif pmf_score_pct >= 60:
        verdict = "🟢 PMF APPROACHING — Fix gaps before scaling"
        stage = "PMF_APPROACHING"
    elif pmf_score_pct >= 40:
        verdict = "🟡 WEAK PMF SIGNAL — Iterate before scaling"
        stage = "PMF_WEAK"
    else:
        verdict = "🔴 NO PMF YET — Do not scale acquisition"
        stage = "NO_PMF"

    # Context-based warnings
    warnings = []
    if paying_customers < 40 and sean_ellis_pct > 0:
        warnings.append(f"⚠️ Sean Ellis requires minimum 40 respondents for statistical validity. You have {paying_customers} customers — survey results may not be reliable.")
    if weeks_since_launch < 8 and stage not in ["PMF_CONFIRMED"]:
        warnings.append(f"📊 Only {weeks_since_launch} weeks since launch — too early for definitive PMF read. Most companies need 12-24 weeks of data.")
    if stage == "NO_PMF" and weeks_since_launch > 24:
        warnings.append("⏰ 24+ weeks without PMF signal — consider ICP pivot or problem pivot. What's the riskiest assumption? Test that first.")

    return json.dumps({
        "pmf_score": f"{pmf_score_pct:.0f}/100",
        "stage": stage,
        "verdict": verdict,
        "signals": signals,
        "gaps_to_close": gaps,
        "warnings": warnings,
        "next_action": gaps[0] if gaps else "Maintain and grow from strong PMF position",
        "scale_gate": "PASS — scale acquisition" if stage == "PMF_CONFIRMED" else f"BLOCK — fix PMF first: {gaps[0] if gaps else 'gather more data'}",
        "benchmarks": {
            "sean_ellis_target": "40%+ Very Disappointed = PMF (Superhuman: 58%, Slack: 51%)",
            "nrr_target": ">100% = net negative churn",
            "d30_retention_target": ">40% for daily tools, >30% for weekly tools",
            "referral_target": ">20% of new users from WOM",
            "monthly_churn_target": "<2% for strong PMF",
        },
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 15: generate_competitor_brief
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
        known_target_icp: Their stated target customer (e.g. "SMB marketing teams")
        known_complaints: List of known complaints (from reviews, Reddit, etc.)
        your_mrr: Your current MRR (for Mandala positioning)
        your_icp: Your target ICP (for displacement opportunity detection)
    """
    if known_complaints is None:
        known_complaints = []

    research_agenda = []
    mandala_position = "Ring 1 (Direct Enemy)" if your_icp and known_target_icp else "Unknown — research needed"

    # Research gaps
    if not known_pricing:
        research_agenda.append("🔍 Pricing: Visit their pricing page. Note plan names, prices, annual discount, free tier limits.")
    if not known_target_icp:
        research_agenda.append("🔍 Real ICP: Search LinkedIn for people who list this tool in their profile. What's their title and company size?")
    if not known_complaints:
        research_agenda.append(f"🔍 Complaints: Search Reddit for 'alternative to {competitor_name}' and 'switched away from {competitor_name}'. Search G2 for 1-3 star reviews.")
    research_agenda.append(f"🔍 Distribution: Check {competitor_name}.com/blog for content strategy. Check SimilarWeb for traffic sources.")
    research_agenda.append(f"🔍 Achilles Heel: Check Glassdoor for company reviews — insider complaints reveal strategic weaknesses.")

    # Displacement opportunity
    displacement_ops = []
    for complaint in known_complaints:
        displacement_ops.append(f"→ Complaint detected: '{complaint}' — this is a displacement opening. If you solve this, target their users with this specific pain.")

    # Upaya recommendation
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
        "next_step": f"Run the live research commands above using Reddit MCP and HN MCP. Then fill in Layers 2-5 with real data.",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 16: calculate_runway
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def calculate_runway(
    cash_balance: float,
    monthly_burn: float,
    current_mrr: float = 0.0,
    monthly_churn_rate: float = 0.05,
    monthly_new_mrr: float = 0.0,
    committed_upcoming_expenses: float = 0.0,
) -> str:
    """
    Calculate true runway accounting for MRR growth, churn, and upcoming lump expenses.
    Returns adjusted runway, break-even MRR, and month-by-month projection.

    Use when: Any mention of runway, cash, burn rate, or "how long do I have?"
    More accurate than simple cash/burn because it accounts for MRR trajectory.

    Args:
        cash_balance: Current cash in bank (dollars)
        monthly_burn: Current monthly operating expenses (dollars)
        current_mrr: Current MRR (0 = pre-revenue)
        monthly_churn_rate: Monthly MRR churn rate (0.05 = 5%)
        monthly_new_mrr: Expected new MRR added per month
        committed_upcoming_expenses: Known future lump sum expenses (annual software, taxes, etc.)
    """
    # Naive runway
    net_burn = monthly_burn - current_mrr
    naive_runway = cash_balance / max(net_burn, 1) if net_burn > 0 else 999

    # True runway (with MRR growth trajectory and buffer)
    real_monthly_burn = monthly_burn * 1.2  # 20% buffer for surprises
    adjusted_cash = cash_balance - committed_upcoming_expenses

    # Month-by-month projection (12 months)
    months = []
    cash = adjusted_cash
    mrr = current_mrr

    for month in range(1, 13):
        mrr = mrr * (1 - monthly_churn_rate) + monthly_new_mrr
        net_cashflow = mrr - real_monthly_burn
        cash += net_cashflow
        months.append({
            "month": month,
            "mrr": round(mrr, 0),
            "net_cashflow": round(net_cashflow, 0),
            "cash_remaining": round(cash, 0),
            "status": "🟢 positive" if cash > 0 else "🔴 BANKRUPT",
        })
        if cash <= 0:
            break

    # Find break-even MRR
    break_even_mrr = real_monthly_burn  # simplified (ignores churn replacement cost)

    # Runway month count
    runway_months = sum(1 for m in months if m["cash_remaining"] > 0)

    # Default alive check
    projected_mrr_12mo = current_mrr * (1 - monthly_churn_rate)**12 + monthly_new_mrr * 12
    default_alive = projected_mrr_12mo > real_monthly_burn

    # Status assessment
    if runway_months >= 18:
        status = "🟢 COMFORTABLE — 18+ months to find next milestone"
    elif runway_months >= 12:
        status = "🟡 ADEQUATE — 12-18mo runway, watch growth rate"
    elif runway_months >= 6:
        status = "🟠 WARNING — 6-12mo runway, fundraise or cut costs now"
    else:
        status = "🔴 CRISIS — <6mo runway. Immediate action required."

    return json.dumps({
        "inputs": {
            "cash_balance": f"${cash_balance:,.0f}",
            "monthly_burn": f"${monthly_burn:,.0f}",
            "current_mrr": f"${current_mrr:,.0f}",
            "adjusted_burn_with_buffer": f"${real_monthly_burn:,.0f} (20% safety buffer applied)",
            "committed_expenses_deducted": f"${committed_upcoming_expenses:,.0f}",
        },
        "naive_runway": f"{naive_runway:.1f} months (cash ÷ current net burn — optimistic)",
        "true_runway_months": runway_months,
        "status": status,
        "default_alive": default_alive,
        "default_alive_explanation": "Will you reach profitability before cash out if growth continues at current rate?",
        "break_even_mrr": f"${break_even_mrr:,.0f}/mo needed to stop burning cash",
        "mrr_gap_to_break_even": f"${max(0, break_even_mrr - current_mrr):,.0f}/mo more MRR needed",
        "month_by_month": months,
        "action": (
            "CRISIS PROTOCOL: Cut all non-essential spend + ramp direct sales daily" if runway_months < 6
            else "Fundraise mode ON" if runway_months < 12
            else "Monitor monthly — stay above 12 months at all times"
        ),
        "sequoia_rule": "Maintain 18+ months runway or be actively fundraising. <6mo = emergency mode.",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool 17: monitor_competitor — Weekly competitive intelligence brief
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
    Includes specific MCP commands to run for live data collection.

    Args:
        competitor_name: Name of the competitor to monitor
        competitor_url: Their website URL (optional but improves output)
        your_mrr: Your current MRR for stage-calibrated framing
        your_icp: Your ideal customer profile
        known_recent_changes: Any changes you already know about (pricing, features, etc.)
        category: Market category (e.g., "AI email tools", "project management for designers")
    """
    import json as _json

    founder_mrr_val = _parse_mrr_string(your_mrr)

    # Stage-calibrated monitoring intensity
    if founder_mrr_val < 5000:
        monitoring_intensity = "LIGHT — check monthly, focus on pricing/positioning only"
        threat_level_context = "At your stage, competitor moves matter less than getting first customers."
    elif founder_mrr_val < 20000:
        monitoring_intensity = "MODERATE — check bi-weekly, track pricing + new features + customer complaints"
        threat_level_context = "At your stage, competitor weaknesses = your acquisition opportunities."
    else:
        monitoring_intensity = "ACTIVE — weekly monitoring, full signal tracking"
        threat_level_context = "At your stage, competitor intelligence directly informs positioning and roadmap."

    # Layer 1: Offer analysis
    offer_signals = [
        f"Pricing page changes (scrape {competitor_url}/pricing if available)",
        "Free tier limits and paid tier feature gates",
        "New product lines or feature announcements",
        "Trial length and onboarding flow changes",
        "Integration additions (their API/integrations page)",
    ]

    # Layer 2: ICP signals
    icp_signals = [
        f"Who is upvoting their ProductHunt page (job titles, company sizes)",
        f"Case studies and testimonials (which company types they highlight)",
        f"Job postings (what roles they're hiring = what segments they're going after)",
        "LinkedIn page followers — company size and industry breakdown",
        "Content topics (what customer segments their blog/content targets)",
    ]

    # Layer 3: Customer sentiment
    sentiment_sources = [
        f"Reddit: search '{competitor_name} review', '{competitor_name} alternative', '{competitor_name} problems'",
        f"HackerNews: search '{competitor_name}' in comments (hn.algolia.com)",
        f"G2 / Capterra: most recent 1-star and 2-star reviews (what specifically they complain about)",
        f"Twitter/X: '{competitor_name} -filter:retweets' sorted by Latest",
        f"Indie Hackers: search their name in community posts",
    ]

    # Layer 4: Distribution channels
    distribution_signals = [
        "Content publishing frequency and topics (Similarweb/Semrush for free estimate)",
        "Backlink profile changes (new partnerships indicated by referring domains)",
        "Social media posting cadence and engagement",
        "Podcast / conference appearances (Google: 'site:buzzsprout.com OR site:transistor.fm [competitor]')",
        "Affiliate / partner program activity",
    ]

    # Layer 5: Achilles heel — the systematic weakness
    achilles_patterns = {
        "complexity": "Complex product targeting power users → opportunity: simpler tool for same outcome",
        "price": "High price point → opportunity: lower entry price for specific segment",
        "support": "Poor support reviews → opportunity: obsessive customer success as differentiator",
        "niche": "Broad generalist product → opportunity: deep specialization for one vertical",
        "legacy": "Legacy tech/UX → opportunity: modern stack, better developer experience",
        "size": "Large company, slow roadmap → opportunity: faster shipping, founder relationship with customers",
    }

    # Build research agenda with MCP commands
    mcp_commands = [
        f"mcp__reddit__reddit_search_reddit(query='{competitor_name} problems OR sucks OR alternative OR switch', limit=25)",
        f"mcp__reddit__reddit_search_reddit(query='{competitor_name} review', subreddit='SaaS', limit=10)",
        f"mcp__hackernews__getItem (search HN Algolia for '{competitor_name}')",
    ]
    if competitor_url:
        mcp_commands.append(f"mcp__jina__jina_reader(url='{competitor_url}/pricing') — extract current pricing")
        mcp_commands.append(f"mcp__jina__jina_reader(url='{competitor_url}/blog') — track content topics")

    # Signal classification
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

    output = {
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
    }

    return _json.dumps(output, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool 18: enrich_prospect — 90-second prospect research brief
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
    Includes specific MCP/search commands to execute for live data enrichment.

    Args:
        company_name: Target company name
        contact_name: Decision-maker name (optional)
        contact_role: Their role/title (optional, helps personalize outreach)
        your_icp: Your ideal customer profile description
        your_product: What your product does (1 sentence)
        your_mrr: Your current MRR (for ACV routing)
    """
    import json as _json

    founder_mrr_val = _parse_mrr_string(your_mrr)

    # ACV-based outreach motion
    if founder_mrr_val < 10000:
        outreach_motion = "HIGH-TOUCH: Personal DM → short value observation → ask for 20-min call"
        follow_up_sequence = "Day 0: initial DM/email | Day 3: value-add resource | Day 7: ask | Day 14: final"
    elif founder_mrr_val < 50000:
        outreach_motion = "STRUCTURED: Cold email sequence + LinkedIn connection + call offer"
        follow_up_sequence = "Day 0: email | Day 2: LinkedIn connect | Day 5: email 2 (case study) | Day 10: final ask"
    else:
        outreach_motion = "SALES-LED: Full SDR sequence, discovery call targeting, demo offer"
        follow_up_sequence = "Day 0: research + personalized email | Day 3: LinkedIn | Day 7: phone | Day 14: email | Day 21: final"

    # Research agenda — what to look up
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

    # Pain hypothesis framework
    pain_hypothesis = {
        "template": f"If {company_name} is a [size] company doing [activity], their biggest pain in [your product category] is probably: [specific problem].",
        "validation_question": f"'I've been talking to {contact_role or 'founders'} at similar companies and the most common challenge I hear is [X]. Is that something you deal with, or is it different for you?'",
        "note": "Never assume the pain — use this as a hypothesis to validate in the opening question, not as a claim.",
    }

    # The 3 outreach variants
    outreach_variants = {
        "variant_1_insight": {
            "approach": "Lead with a relevant insight specific to their company/role",
            "template": f"Hi {contact_name or '[Name]'},\n\nI noticed [company_specific_observation — from hiring/news/product/content].\n\nMost {contact_role or 'teams'} I talk to at [similar company type] are dealing with [specific pain] because of this.\n\nIs that relevant for you, or are you in a different place?\n\n[Your name]",
            "best_for": "Cold email, LinkedIn DM to someone who posts actively",
        },
        "variant_2_case_study": {
            "approach": "Lead with a relevant outcome from a similar company",
            "template": f"Hi {contact_name or '[Name]'},\n\nI helped [similar company type] [specific outcome — e.g., 'reduce manual reporting time from 4hrs/week to 20min'] using [your product].\n\nGiven what [company_name] is building, it might apply.\n\nWorth a 15-minute call to see if the situation is similar?\n\n[Your name]",
            "best_for": "Cold email when you have a relevant case study",
        },
        "variant_3_resource": {
            "approach": "Lead with pure value — no ask",
            "template": f"Hi {contact_name or '[Name]'},\n\nI've been researching [their industry/problem space] and wrote up [relevant resource — framework, analysis, tool]. Thought it might be useful given what [company_name] is working on.\n\n[Link or attach]\n\nNo ask — just hope it's useful. [Your name]",
            "best_for": "First touch when you want to start a relationship without a pitch",
        },
    }

    # Conversation starters for discovery
    discovery_openers = [
        f"'What's the most painful part of [relevant workflow] for your team right now?'",
        f"'I saw you're hiring for [role from job board] — what's driving that decision?'",
        f"'I noticed {company_name} recently [news/product/hiring signal] — is [related challenge] something you're focused on?'",
        f"'What does your current workflow for [relevant activity] look like today?'",
    ]

    return _json.dumps({
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
            "authority_signal": f"Is {contact_name or 'the contact'} a decision maker or influencer? (Title + LinkedIn connections)",
            "need_signal": "Do their hiring signals or content indicate the pain your product solves?",
            "timing_signal": "Are there triggers suggesting NOW is the right time? (new hire, new initiative, funding, competitor problem)",
        },
        "kill_signal": (
            "If after 2 full outreach sequences (14 touchpoints) there is zero response: "
            "either wrong ICP, wrong channel, or wrong pain hypothesis. Do not increase volume — improve targeting."
        ),
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 17: update_context
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def update_context(
    file: str,
    content: str,
    mode: str = "overwrite",
) -> str:
    """
    Write or append to a SoloOS context file. Activates cross-session memory.

    Use during onboarding, assumption drift corrections, or whenever the founder
    updates their ICP, stage, metrics, or experiments.

    Args:
        file: Which context file to update. One of:
              "business-context" | "experiment-log" | "decision-log" |
              "customer-voice" | "mission"
        content: The markdown content to write (full replacement) or append.
        mode: "overwrite" (replace entire file) or "append" (add to end).
              Default: "overwrite". Use "append" for adding new entries to logs.

    Returns: Confirmation with file path and byte count written.
    """
    from .log_manager import (
        BUSINESS_CONTEXT_PATH,
        EXPERIMENT_LOG_PATH,
        DECISION_LOG_PATH,
        CUSTOMER_VOICE_PATH,
        CONTEXT_ROOT,
    )

    file_map = {
        "business-context": BUSINESS_CONTEXT_PATH,
        "experiment-log": EXPERIMENT_LOG_PATH,
        "decision-log": DECISION_LOG_PATH,
        "customer-voice": CUSTOMER_VOICE_PATH,
        "mission": CONTEXT_ROOT / "mission.md",
    }

    if file not in file_map:
        return json.dumps({
            "status": "error",
            "message": f"Unknown file '{file}'. Valid options: {list(file_map.keys())}",
        })

    target = file_map[file]
    target.parent.mkdir(parents=True, exist_ok=True)

    if mode == "append":
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        new_content = existing.rstrip() + "\n\n" + content
    else:
        new_content = content

    target.write_text(new_content, encoding="utf-8")

    return json.dumps({
        "status": "success",
        "file": str(target),
        "mode": mode,
        "bytes_written": len(new_content.encode("utf-8")),
        "message": f"Context file '{file}' updated. Cross-session memory is now active for this field.",
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 18: get_system_state
# ─────────────────────────────────────────────────────────────

# Causal chain map: decision_type → downstream variables that shift
_CAUSAL_CHAINS: dict[str, list[dict]] = {
    "pricing_increase": [
        {"variable": "CAC", "direction": "↑", "reason": "harder to close, fewer impulse buys"},
        {"variable": "LTV", "direction": "↑", "reason": "higher revenue per customer"},
        {"variable": "Churn risk", "direction": "↑", "reason": "existing customers may leave"},
        {"variable": "Support load", "direction": "↓", "reason": "fewer low-value customers"},
        {"variable": "Runway", "direction": "↑", "reason": "higher margin per sale"},
    ],
    "pricing_decrease": [
        {"variable": "CAC", "direction": "↓", "reason": "easier to close, lower barrier"},
        {"variable": "LTV", "direction": "↓", "reason": "less revenue per customer"},
        {"variable": "Volume", "direction": "↑ (uncertain)", "reason": "price-sensitive segment unlocked"},
        {"variable": "Support load", "direction": "↑", "reason": "more low-value customers"},
        {"variable": "Margin", "direction": "↓", "reason": "direct unit economics hit"},
    ],
    "hire_first_employee": [
        {"variable": "Runway", "direction": "↓↓", "reason": "salary is fixed burn"},
        {"variable": "Capacity", "direction": "↑", "reason": "more hours in the system"},
        {"variable": "Complexity", "direction": "↑", "reason": "coordination overhead begins"},
        {"variable": "Founder bandwidth", "direction": "↑", "reason": "delegation frees focus"},
        {"variable": "Reversibility", "direction": "2/10", "reason": "letting someone go is costly and slow"},
    ],
    "launch_new_feature": [
        {"variable": "Dev time", "direction": "↓", "reason": "time spent on unvalidated surface area"},
        {"variable": "Retention", "direction": "↑ (if validated)", "reason": "solves real user pain"},
        {"variable": "Support load", "direction": "↑", "reason": "new surface = new failure modes"},
        {"variable": "Focus", "direction": "↓", "reason": "breadth vs depth tradeoff"},
        {"variable": "ICP clarity", "direction": "↓ risk", "reason": "may attract wrong segment"},
    ],
    "pivot": [
        {"variable": "Existing traction", "direction": "↓ or reset", "reason": "current users may not follow"},
        {"variable": "Stage clock", "direction": "reset", "reason": "back to $0 MRR validation phase"},
        {"variable": "Morale", "direction": "↓ short-term", "reason": "sunk cost psychology"},
        {"variable": "Optionality", "direction": "↑", "reason": "new hypothesis, new surface area"},
        {"variable": "Reversibility", "direction": "3/10", "reason": "hard to un-pivot once announced"},
    ],
    "raise_funding": [
        {"variable": "Runway", "direction": "↑↑", "reason": "direct cash injection"},
        {"variable": "Dilution", "direction": "↑", "reason": "equity given in exchange"},
        {"variable": "Growth pressure", "direction": "↑↑", "reason": "investors expect return timeline"},
        {"variable": "Optionality", "direction": "↓", "reason": "harder to lifestyle/exit cheaply"},
        {"variable": "Reversibility", "direction": "2/10", "reason": "dilution is permanent"},
    ],
    "enter_new_market": [
        {"variable": "CAC", "direction": "↑", "reason": "unknown distribution in new market"},
        {"variable": "ICP clarity", "direction": "↓", "reason": "splits focus between segments"},
        {"variable": "Complexity", "direction": "↑↑", "reason": "new language, regulation, channels"},
        {"variable": "Upside", "direction": "↑ (long-term)", "reason": "TAM expansion"},
        {"variable": "Reversibility", "direction": "4/10", "reason": "brand confusion is slow to fix"},
    ],
    "default": [
        {"variable": "Focus", "direction": "?", "reason": "any decision reallocates attention"},
        {"variable": "Runway", "direction": "?", "reason": "cost or revenue impact unknown"},
        {"variable": "Reversibility", "direction": "assess", "reason": "score before committing"},
    ],
}

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


@mcp.tool()
def get_system_state(
    decision: str,
    stage_mrr: str = "",
    show_causal_chain: bool = True,
) -> str:
    """
    Cross-domain system state snapshot BEFORE a significant decision.

    This is the Systems Intelligence Layer — it pulls business context,
    kill signal status, relevant patterns, and causal chain for the decision
    in ONE call instead of requiring 4-5 separate tool calls.

    Use BEFORE any reversibility ≤5/10 decision. Replaces the need to
    manually chain: get_business_context + check_kill_signals_tool +
    match_pattern + score_pmf separately.

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

    # ── 1. Business state ──────────────────────────────────────
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

    # ── 2. Kill signal health ──────────────────────────────────
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

    # ── 3. Pattern matches ────────────────────────────────────
    patterns = get_patterns()
    matched = search_patterns(decision, patterns, top_n=2) if patterns else []
    result["relevant_patterns"] = [
        {"id": p.id, "name": p.name, "situation": p.situation[:200],
         "kill_signal": p.kill_signal if hasattr(p, "kill_signal") else ""}
        for p in matched
    ] if matched else [{"note": "No strong pattern match in PATTERN_LIBRARY.md"}]

    # ── 4. Causal chain ───────────────────────────────────────
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

    # ── 5. System health score ────────────────────────────────
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
# SWARM HELPERS — parallel analysis threads
# ─────────────────────────────────────────────────────────────

def _swarm_pattern_analysis(decision: str) -> dict:
    """Thread: BM25 pattern match from PATTERN_LIBRARY."""
    patterns = get_patterns()
    matched = search_patterns(decision, patterns, top_n=3) if patterns else []
    return {
        "domain": "pattern_match",
        "matches": [
            {"id": p.id, "name": p.name,
             "situation": p.situation[:180],
             "kill_signal": getattr(p, "kill_signal", "")}
            for p in matched
        ] if matched else [],
        "note": f"{len(matched)} pattern(s) matched via BM25" if matched else "No pattern match — novel situation",
    }


def _swarm_founder_cases(decision: str) -> dict:
    """Thread: Analogous founder case search."""
    founders = get_founders()
    matched = search_founders(decision, founders, top_n=3) if founders else []
    return {
        "domain": "analogous_founders",
        "cases": [
            {"founder": c.founder, "product": c.product,
             "decision": c.decision[:160], "outcome": c.outcome[:160],
             "tags": c.tags[:4]}
            for c in matched
        ] if matched else [],
        "note": f"{len(matched)} analogous case(s) found" if matched else "No direct analogues — check FOUNDER_INTELLIGENCE.md",
    }


def _swarm_kill_signal_check() -> dict:
    """Thread: Current kill signal health."""
    entries = load_log()
    alerts = check_kill_signals(entries)
    overdue = [a for a in alerts if a.urgency == "OVERDUE"]
    urgent  = [a for a in alerts if a.urgency == "URGENT"]
    warning = [a for a in alerts if a.urgency == "WARNING"]
    return {
        "domain": "kill_signal_health",
        "overdue": len(overdue),
        "urgent": len(urgent),
        "warning": len(warning),
        "blocker": len(overdue) > 0,
        "alerts": [{"id": a.entry_id, "urgency": a.urgency,
                    "summary": a.summary[:120], "days_remaining": a.days_remaining}
                   for a in alerts[:5]],
        "note": (f"🚨 {len(overdue)} OVERDUE — resolve before new decisions"
                 if overdue else
                 f"🟡 {len(urgent)} urgent within 7 days"
                 if urgent else "✅ Kill signals healthy"),
    }


def _swarm_causal_impact(decision: str, stage_mrr: str) -> dict:
    """Thread: Causal chain + system state snapshot."""
    ctx = read_business_context()
    mrr = stage_mrr or ctx.get("mrr", "unknown")
    dtype = _detect_decision_type(decision)
    chain = _CAUSAL_CHAINS.get(dtype, _CAUSAL_CHAINS["default"])

    # Stage-specific risk amplifiers
    risk_notes = []
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0
    if dtype == "hire_first_employee" and mrr_int < 5000:
        risk_notes.append("⚠️ Hiring before $5K MRR — Tringas Rule violation")
    if dtype == "raise_funding" and mrr_int < 50000:
        risk_notes.append("⚠️ Fundraising below $50K MRR — model bootstrapped path first")
    if dtype == "enter_new_market" and mrr_int < 50000:
        risk_notes.append("⚠️ International expansion before $50K MRR — fix home-market churn first")

    return {
        "domain": "causal_impact",
        "decision_type": dtype,
        "stage_mrr": mrr,
        "downstream_effects": chain,
        "stage_risk_flags": risk_notes,
        "icp": ctx.get("icp", "not set"),
        "biggest_challenge": ctx.get("biggest_challenge", "not set"),
    }


def _swarm_market_signals(decision: str) -> dict:
    """Thread: Market intelligence queries to run (instructions for live MCPs)."""
    keywords = " ".join(decision.lower().split()[:6])
    return {
        "domain": "market_signals",
        "status": "query_ready",
        "note": "Run these live queries for real-time signals:",
        "reddit_query": {
            "tool": "mcp__reddit__reddit_search_reddit",
            "params": {"query": keywords, "limit": 10},
            "subreddits_to_check": ["entrepreneur", "startups", "SaaS", "indiehackers"],
        },
        "hackernews_query": {
            "tool": "mcp__hackernews__getTopStories",
            "note": f"Filter for: {keywords}",
        },
        "competitor_query": {
            "tool": "mcp__soloos-core__generate_competitor_brief",
            "trigger": "if competitor name mentioned in decision",
        },
        "jina_scrape": {
            "tool": "mcp__jina__jina_reader",
            "note": "Scrape competitor pricing/feature pages if relevant",
        },
    }


# ─────────────────────────────────────────────────────────────
# TOOL 19: get_decision_intelligence_brief
# ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_decision_intelligence_brief(
    decision: str,
    stage_mrr: str = "",
    include_market_signals: bool = True,
) -> str:
    """
    SWARM INTELLIGENCE BRIEF — parallel multi-domain analysis of a decision.

    Runs 4 analysis threads simultaneously (patterns, founders, kill signals,
    causal impact) and synthesizes into a single Decision Intelligence Brief.
    Replaces manually calling 5+ separate tools.

    This is the Systems Intelligence Layer upgrade: not just "what does the
    framework say?" but "what do ALL domains say simultaneously?"

    Args:
        decision: What the founder is considering
        stage_mrr: Current MRR for stage-calibrated analysis
        include_market_signals: Include live query instructions for Reddit/HN (default True)

    Returns:
        Unified JSON: 4 parallel analyses + synthesis + recommended action + kill signal
    """
    brief: dict = {
        "decision": decision,
        "timestamp": today_str(),
        "stage_mrr": stage_mrr or "unknown",
        "swarm_domains": [],
    }

    # ── Parallel execution ───────────────────────────────────
    futures_map = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures_map[ex.submit(_swarm_pattern_analysis, decision)]   = "patterns"
        futures_map[ex.submit(_swarm_founder_cases, decision)]       = "founders"
        futures_map[ex.submit(_swarm_kill_signal_check)]             = "kill_signals"
        futures_map[ex.submit(_swarm_causal_impact, decision, stage_mrr)] = "causal"
        if include_market_signals:
            futures_map[ex.submit(_swarm_market_signals, decision)]  = "market"

        domain_results: dict[str, dict] = {}
        for future in as_completed(futures_map):
            key = futures_map[future]
            try:
                domain_results[key] = future.result()
            except Exception as e:
                domain_results[key] = {"domain": key, "error": str(e)}

    brief["swarm_domains"] = list(domain_results.values())

    # ── Synthesis ────────────────────────────────────────────
    kill = domain_results.get("kill_signals", {})
    causal = domain_results.get("causal", {})
    patterns = domain_results.get("patterns", {})
    founders = domain_results.get("founders", {})

    blocker = kill.get("blocker", False)
    risk_flags = causal.get("stage_risk_flags", [])
    dtype = causal.get("decision_type", "unknown")
    effects = causal.get("downstream_effects", [])

    # Reversibility from causal chain
    rev_effect = next((e for e in effects if "Reversibility" in e.get("variable", "")), None)
    reversibility = rev_effect["direction"] if rev_effect else "assess"

    # Top pattern
    top_pattern = patterns.get("matches", [{}])[0] if patterns.get("matches") else None
    top_case = founders.get("cases", [{}])[0] if founders.get("cases") else None

    synthesis = {
        "decision_type": dtype,
        "reversibility": reversibility,
        "blocker": ("🚨 RESOLVE OVERDUE KILL SIGNALS FIRST" if blocker
                    else "No blockers — proceed with analysis"),
        "stage_flags": risk_flags,
        "top_pattern": top_pattern["name"] if top_pattern else "none",
        "top_analogue": f"{top_case['founder']} ({top_case['product']})" if top_case else "none",
        "key_effects": [f"{e['variable']} {e['direction']}" for e in effects[:3]],
        "recommended_action": (
            "STOP: resolve overdue kill signals before this decision compounds risk"
            if blocker else
            f"PROCEED with caution — reversibility {reversibility}. "
            f"Run live market scan (Reddit + HN) before committing."
            if reversibility in ("2/10", "3/10") else
            "PROCEED — collect 3 data points this week to validate, then commit"
        ),
        "kill_signal_template": (
            f"If [{decision[:50]}...] does not show [measurable signal] "
            f"within 30 days, this approach is wrong. Pivot or stop."
        ),
    }

    brief["synthesis"] = synthesis
    brief["next_live_queries"] = domain_results.get("market", {})

    return json.dumps(brief, indent=2)


# ─────────────────────────────────────────────────────────────
# TOOL 20: run_morning_brief
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

    # Active experiments
    pending = [e for e in entries if e.outcome_status == "⏳ Pending"]
    overdue_alerts = [a for a in alerts if a.urgency == "OVERDUE"]
    urgent_alerts  = [a for a in alerts if a.urgency == "URGENT"]
    warning_alerts = [a for a in alerts if a.urgency == "WARNING"]

    mrr = ctx.get("mrr", "unknown")
    stage = ctx.get("stage", "unknown")
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0

    # Stage-gated focus recommendation
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
# TOOL 21: score_opportunity
# ─────────────────────────────────────────────────────────────

# Paid API recommendations by goal + stage
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

_OPPORTUNITY_DIMENSIONS = [
    "market_size",      # TAM evidence
    "founder_fit",      # does the founder have edge here?
    "timing",           # is the market opening or closing?
    "competition",      # how differentiated is the position?
    "monetization",     # can this charge enough to be a business?
]

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

    Returns:
        Opportunity score + dimension breakdown + API stack recommendations
    """
    ctx = read_business_context()
    mrr = stage_mrr or ctx.get("mrr", "unknown")
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0

    scores: dict[str, dict] = {}

    # ── Market Size ───────────────────────────────────────────
    ms_score = 5  # neutral default
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

    # ── Founder Fit ───────────────────────────────────────────
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

    # ── Timing ───────────────────────────────────────────────
    # Heuristic: if market is young (no SaaS leader) timing is open
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

    # ── Competition ───────────────────────────────────────────
    comp_score = max(0, 10 - (competitor_count if competitor_count >= 0 else 5))
    comp_note = (f"{competitor_count} known competitors" if competitor_count >= 0
                 else "Competitor count unknown — run generate_competitor_brief")
    scores["competition"] = {"score": min(comp_score, 10), "max": 10, "note": comp_note}

    # ── Monetization ──────────────────────────────────────────
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

    # ── Overall Score ─────────────────────────────────────────
    total = sum(v["score"] for v in scores.values())
    max_total = sum(v["max"] for v in scores.values())
    overall_pct = round((total / max_total) * 100)
    verdict = (
        "🟢 HIGH conviction — pursue aggressively, set 30-day kill signal" if overall_pct >= 70 else
        "🟡 MEDIUM conviction — validate 2 weak dimensions before building" if overall_pct >= 50 else
        "🔴 LOW conviction — too many unknowns. Validate before committing any weeks"
    )

    # ── API recommendations by goal ───────────────────────────
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
    # Always recommend analytics + banking from day 0
    recommended_apis.extend(_API_RECOMMENDATIONS.get("customer_analytics", [{}])[:1])
    recommended_apis.extend(_API_RECOMMENDATIONS.get("financial_ops", [{}])[:1])

    # Deduplicate
    seen, unique_apis = set(), []
    for api in recommended_apis:
        if api.get("name") and api["name"] not in seen:
            seen.add(api["name"])
            # Filter by stage
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
# Entry point
# ─────────────────────────────────────────────────────────────

def main():
    mcp.run()


if __name__ == "__main__":
    main()
