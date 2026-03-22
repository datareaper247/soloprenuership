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
# Entry point
# ─────────────────────────────────────────────────────────────

def main():
    mcp.run()


if __name__ == "__main__":
    main()
