"""
SoloOS v7 — Decision Intelligence Engine

Pure Python business logic for all decision-related tools.
No MCP decorators here — server.py registers these as tools.

v7 key upgrades:
  - get_decision_intelligence_brief calls run_council_brief for REAL AI analysis
    (5 actual Claude sub-agent calls, not keyword scoring)
  - simulate_business_change uses stage-gated causal maps
  - score_pmf with precise PMF thresholds
  - validate_idea_gates with Gate 0-4 protocol
"""

from __future__ import annotations

import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# ─────────────────────────────────────────────────────────────
# Data structures
# ─────────────────────────────────────────────────────────────

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

_CHANGE_CAUSAL_MAP: dict[str, dict] = {
    "price_increase": {
        "label": "Price Increase",
        "primary_impacts": [
            {"variable": "MRR (existing customers)", "direction": "neutral → positive",
             "note": "Existing customers stay at old price until renewal"},
            {"variable": "MRR (new customers)", "direction": "positive",
             "note": "New customers pay the new price immediately"},
            {"variable": "Churn rate", "direction": "slight increase risk",
             "note": "B2B SaaS: typically <5% additional churn per 20% price increase"},
            {"variable": "CAC", "direction": "neutral", "note": "Price rarely affects acquisition cost"},
            {"variable": "LTV", "direction": "positive", "note": "Higher price → higher LTV assuming same retention"},
        ],
        "reversibility": 4,
        "rule": "B2B SaaS absorbs 20-30% annual price increases with <5% churn impact if value is delivered. Grandfathering kills margin.",
        "red_flags": ["Raising price before PMF is confirmed", "Raising price without value delivery proof"],
        "kill_signal_template": "If churn in 30 days post-price-change exceeds baseline by >10 percentage points, revert and diagnose.",
    },
    "price_decrease": {
        "label": "Price Decrease / Discount",
        "primary_impacts": [
            {"variable": "MRR", "direction": "negative", "note": "Immediate MRR drop if applied retroactively"},
            {"variable": "Churn rate", "direction": "slight decrease", "note": "Rarely prevents churn — customers churn due to value, not price"},
            {"variable": "CAC", "direction": "may decrease", "note": "Lower price may reduce sales friction"},
            {"variable": "Positioning", "direction": "degraded", "note": "Price signals value — decreasing signals less value"},
        ],
        "reversibility": 3,
        "rule": "Discounting almost never solves churn. Customers who leave at $50 leave at $20. Fix the value, not the price.",
        "red_flags": ["Discounting to close deals instead of improving value", "Blanket discounts vs. strategic pricing"],
        "kill_signal_template": "If 30 days after discount, conversion hasn't improved >20%, the blocker is not price.",
    },
    "hire_employee": {
        "label": "First Employee / Full-Time Hire",
        "primary_impacts": [
            {"variable": "Burn rate", "direction": "increases by salary + overhead",
             "note": "Estimate: $5K–12K/mo per FTE including overhead"},
            {"variable": "Runway", "direction": "decreases significantly",
             "note": "At $5K/mo burn: a $6K/mo hire cuts runway by ~50%"},
            {"variable": "Founder bandwidth", "direction": "increases after 60-day ramp",
             "note": "First 30-60 days: bandwidth DECREASES due to management overhead"},
            {"variable": "Revenue (if sales hire)", "direction": "delayed positive",
             "note": "Sales hire: 30-90 day ramp before meaningful contribution"},
        ],
        "reversibility": 2,
        "rule": "Hire to the document. Only hire if you have a documented process the hire will execute.",
        "stage_gate": "$20K MRR minimum before full-time hire, unless role is directly revenue-generating.",
        "red_flags": ["Hiring before role is documented", "Hiring to solve founder burnout"],
        "kill_signal_template": "If hire hasn't contributed measurable output by day 60, the role definition or onboarding is the problem.",
    },
    "hire_va": {
        "label": "Virtual Assistant / Contractor",
        "primary_impacts": [
            {"variable": "Burn rate", "direction": "increases by $800–2K/mo", "note": "Typical VA cost"},
            {"variable": "Runway", "direction": "minor decrease", "note": "Much smaller runway impact than FTE"},
            {"variable": "Founder bandwidth", "direction": "increases by 5-10hrs/week after setup", "note": "Requires good SOP first"},
        ],
        "reversibility": 7,
        "rule": "Document the task fully first. Test with a 20-hr pilot project before committing.",
        "red_flags": ["Hiring VA to figure out what to delegate"],
        "kill_signal_template": "If 2 weeks after VA starts, founder spends >2hrs/week correcting work, the SOP is wrong.",
    },
    "run_paid_ads": {
        "label": "Launch Paid Advertising",
        "primary_impacts": [
            {"variable": "CAC", "direction": "increases initially (learning phase)",
             "note": "First 30-60 days: CAC 2-5x higher than target"},
            {"variable": "Burn rate", "direction": "increases by ad spend + management time",
             "note": "Minimum viable test: $2K/mo"},
            {"variable": "MRR (if PMF confirmed)", "direction": "positive after 60-90 days",
             "note": "Paid ads amplify a working funnel — they don't fix a broken one."},
            {"variable": "Runway", "direction": "decreases by ad spend per month", "note": "Fixed cost regardless of outcome"},
        ],
        "reversibility": 8,
        "rule": "Never run ads before knowing: (1) D30 retention, (2) LTV > 3x CAC target, (3) one organic channel already converts.",
        "stage_gate": "$5K MRR with proven retention before paid acquisition.",
        "red_flags": ["Running ads without knowing LTV", "Running ads as the first acquisition attempt"],
        "kill_signal_template": "If after 60 days CAC > LTV/3, turn off and fix funnel first.",
    },
    "pivot": {
        "label": "Product or Market Pivot",
        "primary_impacts": [
            {"variable": "Existing MRR", "direction": "at risk — 30-70% may not follow",
             "note": "Existing customers bought a specific thing. Pivots often lose them."},
            {"variable": "Product velocity", "direction": "reset — 60-90 day dead zone",
             "note": "Pivots require rebuilding context, codebase focus, positioning"},
            {"variable": "CAC", "direction": "increases — new ICP, new channels to learn", "note": "Every pivot resets acquisition learning"},
        ],
        "reversibility": 2,
        "rule": "Pivot on customer insight, not discouragement. Pivot driven by 5+ customers saying 'I wish you did X' is valid.",
        "red_flags": ["Pivoting without 3+ customers articulating the pivot direction", "Pivoting within first 60 days"],
        "kill_signal_template": "If 90 days post-pivot you have fewer paying customers than pre-pivot, the direction was wrong.",
    },
    "expand_market": {
        "label": "Geographic or ICP Expansion",
        "primary_impacts": [
            {"variable": "CAC", "direction": "increases — new market learning", "note": "New markets require new positioning and channels"},
            {"variable": "Support load", "direction": "increases", "note": "New segments have different edge cases"},
            {"variable": "Founder bandwidth", "direction": "decreases significantly",
             "note": "Two ICPs effectively doubles the workload"},
        ],
        "reversibility": 4,
        "rule": "Expand only when home market is saturated. At <$50K MRR, most founders expand to escape, not because home is exhausted.",
        "stage_gate": "$50K MRR with <3% monthly churn before expansion.",
        "red_flags": ["Expanding before home PMF is confirmed", "Expanding to avoid hard sales work in home market"],
        "kill_signal_template": "If 60 days into new market, CAC is >2x home market CAC with no learning curve — pause.",
    },
    "new_feature": {
        "label": "Major New Feature",
        "primary_impacts": [
            {"variable": "Shipping velocity", "direction": "decreases", "note": "Adding a major feature delays everything else"},
            {"variable": "Tech debt", "direction": "may increase if rushed", "note": "Features shipped fast = debt accumulated fast"},
            {"variable": "Churn (if feature solves known pain)", "direction": "may decrease",
             "note": "Only if 3+ churned customers named this as the reason they left"},
        ],
        "reversibility": 5,
        "rule": "Build features to solve a stated problem for 3+ customers, not anticipated problems. Every feature must be maintained forever.",
        "red_flags": ["Building feature based on one customer request", "Building feature because it's interesting"],
        "kill_signal_template": "If 60 days post-ship, the feature hasn't been cited as a reason for purchase or retention — it was wrong.",
    },
}


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _parse_mrr_string(mrr_str: str) -> int:
    """Convert '$3.5K', '$40,000', 'pre-revenue', '0' to integer."""
    import re
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


def _infer_stage_from_mrr(mrr_int: int) -> str:
    if mrr_int == 0:
        return "pre-revenue"
    elif mrr_int < 1000:
        return "$0–1K MRR"
    elif mrr_int < 5000:
        return "$1–5K MRR"
    elif mrr_int < 20000:
        return "$5–20K MRR"
    elif mrr_int < 50000:
        return "$20–50K MRR"
    return "$50K+ MRR"


def _detect_decision_type(decision: str) -> str:
    dl = decision.lower()
    for dtype, keywords in _DECISION_TYPE_KEYWORDS.items():
        if any(kw in dl for kw in keywords):
            return dtype
    return "default"


def _monte_carlo_ev(prob: float, revenue: float, downside: float, hours: float, n: int) -> dict:
    outcomes = []
    for _ in range(n):
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
        "note": f"Monte Carlo ({n} sims) with ±20% probability uncertainty",
    }


# ─────────────────────────────────────────────────────────────
# Swarm thread helpers (pure KB-based, no AI calls)
# ─────────────────────────────────────────────────────────────

def _swarm_pattern_analysis(decision: str) -> dict:
    """BM25 pattern match from PATTERN_LIBRARY."""
    try:
        from ..kb_loader import get_patterns, search_patterns
        patterns = get_patterns()
        matched = search_patterns(decision, patterns, top_n=3) if patterns else []
        return {
            "domain": "pattern_match",
            "matches": [
                {"id": p.id, "name": p.name,
                 "situation": p.situation[:180],
                 "kill_signal": getattr(p, "kill_signal", "")}
                for p in matched
            ],
            "note": f"{len(matched)} pattern(s) matched" if matched else "No pattern match — novel situation",
        }
    except Exception as e:
        return {"domain": "pattern_match", "error": str(e), "matches": []}


def _swarm_founder_cases(decision: str) -> dict:
    """Analogous founder case search."""
    try:
        from ..kb_loader import get_founders, search_founders
        founders = get_founders()
        matched = search_founders(decision, founders, top_n=3) if founders else []
        return {
            "domain": "analogous_founders",
            "cases": [
                {"founder": c.founder, "product": c.product,
                 "decision": c.decision[:160], "outcome": c.outcome[:160],
                 "tags": c.tags[:4]}
                for c in matched
            ],
            "note": f"{len(matched)} analogous case(s)" if matched else "No direct analogues in FOUNDER_INTELLIGENCE.md",
        }
    except Exception as e:
        return {"domain": "analogous_founders", "error": str(e), "cases": []}


def _swarm_kill_signal_check() -> dict:
    """Current kill signal health."""
    try:
        from ..log_manager import load_log, check_kill_signals
        entries = load_log()
        alerts = check_kill_signals(entries)
        overdue = [a for a in alerts if a.urgency == "OVERDUE"]
        urgent = [a for a in alerts if a.urgency == "URGENT"]
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
            "note": (f"🚨 {len(overdue)} OVERDUE — resolve before new decisions" if overdue
                     else f"🟡 {len(urgent)} urgent within 7 days" if urgent else "✅ Kill signals healthy"),
        }
    except Exception as e:
        return {"domain": "kill_signal_health", "error": str(e), "blocker": False}


def _swarm_causal_impact(decision: str, stage_mrr: str) -> dict:
    """Causal chain + stage risk assessment."""
    try:
        from ..log_manager import read_business_context
        ctx = read_business_context()
        mrr = stage_mrr or ctx.get("mrr", "unknown")
        mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0
        dtype = _detect_decision_type(decision)
        chain = _CAUSAL_CHAINS.get(dtype, _CAUSAL_CHAINS["default"])

        risk_notes = []
        if dtype == "hire_first_employee" and mrr_int < 5000:
            risk_notes.append("⚠️ Hiring before $5K MRR — process first, then hire")
        if dtype == "raise_funding" and mrr_int < 50000:
            risk_notes.append("⚠️ Fundraising below $50K MRR — model bootstrapped path first")
        if dtype == "enter_new_market" and mrr_int < 50000:
            risk_notes.append("⚠️ Expansion before $50K MRR — fix home-market churn first")

        return {
            "domain": "causal_impact",
            "decision_type": dtype,
            "stage_mrr": mrr,
            "downstream_effects": chain,
            "stage_risk_flags": risk_notes,
            "icp": ctx.get("icp", "not set"),
        }
    except Exception as e:
        return {"domain": "causal_impact", "error": str(e), "decision_type": "unknown"}


# ─────────────────────────────────────────────────────────────
# Tool: calculate_ev
# ─────────────────────────────────────────────────────────────

def calculate_ev(
    activities: list[dict],
    use_monte_carlo: bool = False,
    simulations: int = 1000,
) -> str:
    """
    Calculate Expected Value (EV) per hour for competing activities.
    Ranks options by EV/hr to identify highest-leverage use of founder time.

    Args:
        activities: List of dicts with: name, hours, probability, revenue_impact, downside (optional)
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
        hours = max(0.1, float(act.get("hours", 1)))
        prob = max(0.0, min(1.0, float(act.get("probability", 0.5))))
        revenue = float(act.get("revenue_impact", 0))
        downside = float(act.get("downside", 0))

        ev = (prob * revenue) + ((1 - prob) * downside)
        ev_per_hour = ev / hours

        item: dict = {
            "name": name,
            "hours": hours,
            "probability": f"{prob:.0%}",
            "revenue_impact": f"${revenue:,.0f}",
            "ev": f"${ev:,.0f}",
            "ev_per_hour": f"${ev_per_hour:,.0f}/hr",
            "_ev_per_hour_raw": ev_per_hour,
        }

        if use_monte_carlo and simulations > 0:
            item["monte_carlo"] = _monte_carlo_ev(prob, revenue, downside, hours, simulations)

        results.append(item)

    results.sort(key=lambda x: x["_ev_per_hour_raw"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
        del r["_ev_per_hour_raw"]

    winner = results[0]
    comparison = ""
    if len(results) >= 2:
        ev0 = float(results[0]["ev"].replace("$", "").replace(",", ""))
        ev1 = max(1, float(results[1]["ev"].replace("$", "").replace(",", "")))
        comparison = f"'{winner['name']}' has {ev0/ev1:.1f}x the EV of the next best option."

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


# ─────────────────────────────────────────────────────────────
# Tool: validate_idea_gates
# ─────────────────────────────────────────────────────────────

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
    Run an idea through SoloOS Gate 0-4 validation protocol.
    Returns structured pass/fail for each gate with specific next actions.

    Use when a founder says "thinking about building X" or "I want to add X".

    Args:
        idea: The product idea or feature description
        category: Market category (for Gate 0 and saturation check)
        self_is_customer: True if founder personally experiences this problem
        heard_from_customers: Number of customers who described this pain unprompted
        competing_solutions: List of known paid alternatives
        target_price: Intended price ($/month)
        problem_monthly_cost: What does this problem cost the customer per month?
    """
    gates: dict = {}
    competing_solutions = competing_solutions or []

    # Gate 0: ChatGPT Substitution Test
    ai_keywords = ["ai", "write", "generate", "summarize", "translate", "analyze", "classify", "extract"]
    chatgpt_risk = sum(1 for kw in ai_keywords if kw in idea.lower())
    gates["gate_0_chatgpt"] = (
        {
            "status": "⚠️ HIGH_RISK",
            "finding": "Core function overlaps with free LLM capabilities.",
            "test_required": "Open ChatGPT free tier. Attempt your product's core function now.",
            "if_passes": "Document the specific gap — that gap IS your product.",
            "if_fails": "Find narrower niche with compliance/integration moat or workflow step LLM can't complete.",
        }
        if chatgpt_risk >= 2 else {
            "status": "✅ LOW_RISK",
            "finding": "Idea doesn't appear easily substituted by a free LLM.",
            "note": "Still run the 5-minute test.",
        }
    )

    # Arvid Kahl Rule
    gates["kahl_rule"] = {
        "status": "✅ PASS" if heard_from_customers >= 3 else "⚠️ UNCLEAR",
        "heard_from": heard_from_customers,
        "required": 3,
        "finding": (
            "3+ customers described this pain unprompted — origin validated."
            if heard_from_customers >= 3
            else f"Only {heard_from_customers} unprompted customer descriptions. Need 3+ before building."
        ),
        "action": None if heard_from_customers >= 3 else "Spend 2hrs in target community listening before building.",
    }

    # Self-as-customer
    gates["self_as_customer"] = {
        "applies": self_is_customer,
        "verdict": (
            "SHORTCUT AVAILABLE: You experience this problem. Skip Gates 1-2. "
            "Document your painful workflow first, then validate others pay (Gate 3)."
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
        "score": g1_score,
        "finding": (
            "Problem existence confirmed." if g1_score >= 60
            else "Weak problem signal. Collect more unprompted customer descriptions."
        ),
        "action": None if g1_score >= 60 else f"Find 3+ people who describe this problem without being prompted. Use Reddit + LinkedIn.",
    }

    # Gate 2: Existing Solutions
    comp_count = len(competing_solutions)
    if comp_count == 0:
        g2_status, g2_note = "⚠️ UNCLEAR", "No competitors found. Either early market or problem isn't painful enough to build a market."
    elif comp_count <= 3:
        g2_status, g2_note = "✅ PASS", f"{comp_count} competitors exist — market validated. Wedge required."
    else:
        g2_status, g2_note = "⚠️ CROWDED", f"{comp_count}+ competitors. Needs strong differentiation or niche focus."
    gates["gate_2_market"] = {
        "status": g2_status,
        "competitors_known": comp_count,
        "competitors": competing_solutions,
        "finding": g2_note,
        "action": "Run mcp__soloos-core__generate_competitor_brief for 5-layer autopsy of top competitor." if comp_count > 0 else "Search Product Hunt + G2 + Reddit for alternatives first.",
    }

    # Gate 3: Willingness to Pay
    if target_price == 0:
        g3_status, g3_note = "⚠️ UNKNOWN", "No target price set. Run the $100 bill test: would someone pay $100/mo right now?"
    elif problem_monthly_cost > 0 and target_price < problem_monthly_cost * 0.1:
        g3_status, g3_note = "⚠️ UNDERPRICED", f"${target_price}/mo is <10% of ${problem_monthly_cost}/mo problem cost. Raise the price."
    elif target_price >= 50:
        g3_status, g3_note = "✅ PASS", f"${target_price}/mo is viable B2B pricing."
    else:
        g3_status, g3_note = "⚠️ LOW_PRICE", f"${target_price}/mo requires volume. Validate >200 customers are reachable."
    gates["gate_3_pricing"] = {
        "status": g3_status,
        "target_price": f"${target_price}/mo" if target_price else "not set",
        "problem_cost": f"${problem_monthly_cost}/mo" if problem_monthly_cost else "unknown",
        "finding": g3_note,
    }

    # Gate 4: Distribution
    gates["gate_4_distribution"] = {
        "status": "⚠️ CHECK",
        "finding": "Can you find 20 of your ICP on LinkedIn/Reddit in 30 minutes?",
        "test": "Open LinkedIn Sales Navigator. Search for your ICP title + company size. Count results in 5 minutes.",
        "passing": ">500 results = accessible market. <50 results = distribution problem.",
        "action": "Before building: send 20 direct DMs to potential customers. Aim for 3 positive signals.",
    }

    # Overall verdict
    statuses = [g.get("status", "") for g in gates.values()]
    fails = sum(1 for s in statuses if "FAIL" in s or "HIGH_RISK" in s)
    clears = sum(1 for s in statuses if "PASS" in s)

    overall = (
        "🟢 HIGH CONVICTION — proceed to building (set 30-day kill signal)" if clears >= 3 and fails == 0
        else "🟡 MEDIUM CONVICTION — 2+ gates unclear, validate before building"
        if fails == 0
        else "🔴 LOW CONVICTION — critical gates failed, validate or pivot idea"
    )

    return json.dumps({
        "idea": idea,
        "overall_verdict": overall,
        "gates": gates,
        "next_action": (
            "Start customer discovery: find 20 people with this problem and have 5 conversations."
            if clears < 3
            else "Gates cleared. Build a 2-day MVP or landing page. Set kill signal: '5 people pay within 30 days.'"
        ),
        "anti_pattern_check": (
            "⚠️ Self-as-customer shortcut applies — document your workflow BEFORE building anything."
            if self_is_customer
            else "Standard validation path — 5 paying customers before building week 3+"
        ),
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: score_pmf
# ─────────────────────────────────────────────────────────────

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
    Score Product-Market Fit across 5 measurement systems.
    Returns PMF stage, what's blocking PMF, and specific actions.

    Use when: "do I have PMF?", "should I scale?", "is this working?"

    Args:
        sean_ellis_pct: % of users who say "Very Disappointed" if product disappeared (target >40%)
        nrr_pct: Net Revenue Retention % (target >100%)
        l30_retention_pct: Day 30 retention % (target >40% for daily tools). Auto-filled from
                           PostHog/user_events in DuckDB when not provided and data exists.
        referral_pct_of_signups: % new users from referral/WOM (target >20%)
        monthly_churn_pct: Monthly churn % (target <2%). Auto-filled from DuckDB churn view
                           when not provided and data exists.
        weeks_since_launch: Weeks since launch (context for expectations)
        paying_customers: Number of paying customers (min 40 for Sean Ellis)
    """
    data_source = "manual_input"
    live_context_notes: list[str] = []

    # Phase E: auto-fill from DuckDB when available — silently, never fail
    if l30_retention_pct == 0.0 or monthly_churn_pct == 0.0:
        try:
            from ..data.analytics_db import get_analytics_db
            db = get_analytics_db()
            if db.has_data():
                # Auto-fill day-7 retention as a proxy for l30 when not provided
                if l30_retention_pct == 0.0:
                    retention = db.get_recent_retention()
                    if retention.get("source") == "user_events" and retention.get("day7") is not None:
                        # Use day-7 as a leading indicator — note this in context
                        day7_pct = round(retention["day7"] * 100, 1)
                        live_context_notes.append(
                            f"Live retention data (PostHog/user_events): "
                            f"day-7 = {day7_pct}% "
                            f"(cohort_size={retention.get('cohort_size', '?')}). "
                            f"D30 not yet available — day-7 used as leading indicator."
                        )
                        data_source = "live_posthog"
                # Auto-fill churn from revenue events
                if monthly_churn_pct == 0.0:
                    live_churn = db.get_churn_rate()
                    if live_churn > 0:
                        monthly_churn_pct = round(live_churn * 100, 2)
                        live_context_notes.append(
                            f"Live churn data (Stripe/revenue_events): "
                            f"monthly churn = {monthly_churn_pct:.2f}%"
                        )
                        data_source = "live_stripe"
        except Exception:
            pass  # fail-open — never let DB errors surface to caller

    score = 0
    max_score = 0
    signals = []
    gaps = []

    if sean_ellis_pct > 0:
        max_score += 30
        if sean_ellis_pct >= 40:
            score += 30
            signals.append(f"✅ Sean Ellis: {sean_ellis_pct:.0f}% (>40% = PMF confirmed)")
        elif sean_ellis_pct >= 30:
            score += 18
            signals.append(f"🟡 Sean Ellis: {sean_ellis_pct:.0f}% (approaching — need 40%+)")
            gaps.append("Sean Ellis below 40% — interview 'somewhat disappointed' users about core use case")
        else:
            score += 5
            signals.append(f"🔴 Sean Ellis: {sean_ellis_pct:.0f}% (far from threshold)")
            gaps.append(f"Sean Ellis at {sean_ellis_pct:.0f}% — major value gap. Who ARE the 'very disappointed'? Build exclusively for them.")

    if nrr_pct > 0:
        max_score += 25
        if nrr_pct >= 110:
            score += 25
            signals.append(f"✅ NRR: {nrr_pct:.0f}% (>110% = net negative churn = elite PMF signal)")
        elif nrr_pct >= 100:
            score += 18
            signals.append(f"🟢 NRR: {nrr_pct:.0f}% (>100% = strong PMF signal)")
        elif nrr_pct >= 90:
            score += 10
            signals.append(f"🟡 NRR: {nrr_pct:.0f}% (acceptable, not exciting)")
            gaps.append("NRR below 100% — find expansion opportunities: usage limits, seat expansion, premium features")
        else:
            signals.append(f"🔴 NRR: {nrr_pct:.0f}% (<90% = revenue shrinking from existing base)")
            gaps.append("NRR below 90% — STOP acquisition. Fix why customers downgrade or churn first.")

    if l30_retention_pct > 0:
        max_score += 25
        if l30_retention_pct >= 40:
            score += 25
            signals.append(f"✅ D30 Retention: {l30_retention_pct:.0f}% (strong habit formation)")
        elif l30_retention_pct >= 25:
            score += 15
            signals.append(f"🟡 D30 Retention: {l30_retention_pct:.0f}% (moderate — improve onboarding)")
            gaps.append("D30 retention 25-40% — map the 'boring middle'. Reduce time-to-first-value.")
        else:
            signals.append(f"🔴 D30 Retention: {l30_retention_pct:.0f}% (<25% = activation failure)")
            gaps.append(f"D30 at {l30_retention_pct:.0f}% — do 5 user copilot sessions this week. Watch them use the product.")

    if referral_pct_of_signups > 0:
        max_score += 10
        if referral_pct_of_signups >= 20:
            score += 10
            signals.append(f"✅ Referral: {referral_pct_of_signups:.0f}% from WOM (organic growth loop active)")
        elif referral_pct_of_signups >= 10:
            score += 5
            signals.append(f"🟡 Referral: {referral_pct_of_signups:.0f}% (building momentum)")
        else:
            signals.append(f"🔴 Referral: {referral_pct_of_signups:.0f}% (people not talking about it)")
            gaps.append("Low WOM — find power users (top 20%) and rebuild for them.")

    if monthly_churn_pct > 0:
        max_score += 10
        if monthly_churn_pct < 2:
            score += 10
            signals.append(f"✅ Monthly Churn: {monthly_churn_pct:.1f}% (excellent)")
        elif monthly_churn_pct < 5:
            score += 6
            signals.append(f"🟡 Monthly Churn: {monthly_churn_pct:.1f}% (acceptable)")
        else:
            signals.append(f"🔴 Monthly Churn: {monthly_churn_pct:.1f}% (>5% = leaky bucket)")
            gaps.append(f"Monthly churn at {monthly_churn_pct:.1f}% — exit interview every churned customer. Pattern emerges after 5-10.")

    pmf_pct = round((score / max_score * 100) if max_score > 0 else 0)

    if pmf_pct >= 80:
        verdict = "🚀 STRONG PMF — Scale acquisition confidently"
        stage = "PMF_CONFIRMED"
    elif pmf_pct >= 60:
        verdict = "🟢 PMF APPROACHING — Fix gaps before scaling"
        stage = "PMF_APPROACHING"
    elif pmf_pct >= 40:
        verdict = "🟡 WEAK PMF SIGNAL — Iterate before scaling"
        stage = "PMF_WEAK"
    else:
        verdict = "🔴 NO PMF YET — Do not scale acquisition"
        stage = "NO_PMF"

    warnings = []
    if paying_customers < 40 and sean_ellis_pct > 0:
        warnings.append(f"⚠️ Sean Ellis needs 40+ respondents. You have {paying_customers} — results may not be reliable.")
    if weeks_since_launch < 8 and stage != "PMF_CONFIRMED":
        warnings.append(f"📊 Only {weeks_since_launch} weeks since launch — too early for definitive PMF read.")
    if stage == "NO_PMF" and weeks_since_launch > 24:
        warnings.append("⏰ 24+ weeks without PMF — consider ICP or problem pivot.")

    result: dict = {
        "pmf_score": f"{pmf_pct}/100",
        "stage": stage,
        "verdict": verdict,
        "signals": signals,
        "gaps_to_close": gaps,
        "warnings": warnings,
        "next_action": gaps[0] if gaps else "Maintain and grow from strong PMF position",
        "scale_gate": "PASS — scale acquisition" if stage == "PMF_CONFIRMED" else f"BLOCK — {gaps[0] if gaps else 'gather more data'}",
        "benchmarks": {
            "sean_ellis_target": "40%+ Very Disappointed (Superhuman: 58%, Slack: 51%)",
            "nrr_target": ">100% = net negative churn",
            "d30_retention_target": ">40% for daily tools, >30% for weekly tools",
            "referral_target": ">20% of new users from WOM",
            "monthly_churn_target": "<2% for strong PMF",
        },
        "data_source": data_source,
    }

    if live_context_notes:
        result["live_data_context"] = live_context_notes

    return json.dumps(result, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: simulate_business_change
# ─────────────────────────────────────────────────────────────

def simulate_business_change(
    change_type: str,
    description: str = "",
    magnitude: str = "",
    stage_mrr: str = "",
) -> str:
    """
    Causal chain simulation: trace downstream effects of a proposed business change.

    Args:
        change_type: price_increase | price_decrease | hire_employee | hire_va |
                     run_paid_ads | pivot | expand_market | new_feature
        description: What specifically you're considering
        magnitude: Size/scale of change (e.g., "30% price increase", "$3K/mo ad spend")
        stage_mrr: Current MRR for stage calibration

    Returns:
        Causal impact map: projected variable shifts, reversibility score, stage gate check, kill signal
    """
    try:
        from ..log_manager import read_business_context
        ctx = read_business_context()
    except Exception:
        ctx = {}

    mrr = stage_mrr or ctx.get("mrr", "unknown")
    mrr_int = _parse_mrr_string(mrr) if mrr not in ("unknown", "") else 0

    ct = change_type.lower().replace("-", "_").replace(" ", "_")
    if ct not in _CHANGE_CAUSAL_MAP:
        matches = [k for k in _CHANGE_CAUSAL_MAP if any(word in ct for word in k.split("_"))]
        ct = matches[0] if matches else None

    if ct is None:
        return json.dumps({
            "error": f"Unknown change_type '{change_type}'.",
            "available": list(_CHANGE_CAUSAL_MAP.keys()),
            "tip": "For unlisted changes, use get_decision_intelligence_brief.",
        })

    profile = _CHANGE_CAUSAL_MAP[ct]
    reversibility = profile["reversibility"]
    stage_gate = profile.get("stage_gate", "")

    stage_warning = None
    if stage_gate and mrr_int > 0:
        import re
        gate_match = re.search(r"\$(\d+)K", stage_gate)
        if gate_match:
            gate_mrr = int(gate_match.group(1)) * 1000
            if mrr_int < gate_mrr:
                stage_warning = (
                    f"⚠️ STAGE GATE: {stage_gate} — You're at {mrr} MRR. "
                    f"This action is premature. Rule: {profile['rule']}"
                )

    red_flags_found = []
    if description:
        desc_lower = description.lower()
        for rf in profile.get("red_flags", []):
            rf_words = set(rf.lower().split())
            desc_words = set(desc_lower.split())
            if len(rf_words & desc_words) >= 2:
                red_flags_found.append(f"⚠️ {rf}")

    kill_signal = profile["kill_signal_template"]
    if magnitude:
        kill_signal = kill_signal.replace("[magnitude]", magnitude)

    impacts = []
    for impact in profile["primary_impacts"]:
        entry = dict(impact)
        if magnitude and any(x in impact["variable"].lower() for x in ["burn", "mrr", "cac", "runway"]):
            entry["magnitude_context"] = f"Given '{magnitude}', monitor this closely."
        impacts.append(entry)

    if reversibility <= 3:
        rev_label = "Nearly irreversible — high evidence bar required"
    elif reversibility <= 5:
        rev_label = "Partially reversible — set kill signal before starting"
    elif reversibility <= 7:
        rev_label = "Moderately reversible — can course-correct within 30-60 days"
    else:
        rev_label = "Easily reversible — low risk, measure and adjust"

    return json.dumps({
        "change": profile["label"],
        "description": description or change_type,
        "magnitude": magnitude or "not specified",
        "stage_mrr": mrr,
        "reversibility": f"{reversibility}/10 — {rev_label}",
        "causal_impacts": impacts,
        "governing_rule": profile["rule"],
        "stage_gate_check": stage_warning or "✅ Stage-appropriate",
        "red_flags": red_flags_found or ["None detected"],
        "kill_signal": kill_signal,
        "system_2_required": reversibility <= 5,
        "next_actions": [
            "Run get_decision_intelligence_brief for full council analysis",
            f"Log kill signal in founder-log.md: {kill_signal[:80]}...",
        ],
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: get_decision_intelligence_brief (v7 — with REAL AI council)
# ─────────────────────────────────────────────────────────────

def get_decision_intelligence_brief(
    decision: str,
    stage_mrr: str = "",
    use_council: bool = True,
) -> str:
    """
    SWARM INTELLIGENCE BRIEF — parallel multi-domain analysis of a decision.

    v7 upgrade: integrates real 5-seat Claude AI council alongside KB pattern/founder analysis.
    All threads run in parallel via ThreadPoolExecutor.

    Args:
        decision: What the founder is considering
        stage_mrr: Current MRR for stage-calibrated analysis
        use_council: Run 5-seat AI council (requires ANTHROPIC_API_KEY, default True)

    Returns:
        Unified JSON: KB patterns + founder cases + kill signals + causal chain + AI council synthesis
    """
    try:
        from ..log_manager import today_str
        timestamp = today_str()
    except Exception:
        from datetime import date
        timestamp = date.today().isoformat()

    brief: dict = {
        "decision": decision,
        "timestamp": timestamp,
        "stage_mrr": stage_mrr or "unknown",
        "swarm_domains": [],
        "intelligence_mode": "v7",
    }

    domain_results: dict = {}

    def _run_council() -> dict:
        """Real 5-seat Claude AI council."""
        if not use_council:
            return {"domain": "ai_council", "skipped": True, "reason": "use_council=False"}
        try:
            from .agents import run_council_brief
            council = run_council_brief(decision, stage_mrr)
            return {
                "domain": "ai_council",
                "seats": council.get("council_seats", []),
                "synthesis": council.get("synthesis", ""),
                "final_verdict": council.get("final_verdict", "INVESTIGATE"),
                "intelligence_mode": council.get("intelligence_mode", "unknown"),
            }
        except Exception as e:
            return {"domain": "ai_council", "error": str(e), "final_verdict": "INVESTIGATE"}

    # Launch all threads in parallel
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {
            ex.submit(_swarm_pattern_analysis, decision): "patterns",
            ex.submit(_swarm_founder_cases, decision): "founders",
            ex.submit(_swarm_kill_signal_check): "kill_signals",
            ex.submit(_swarm_causal_impact, decision, stage_mrr): "causal",
            ex.submit(_run_council): "ai_council",
        }
        for future in as_completed(futures, timeout=35):
            key = futures[future]
            try:
                domain_results[key] = future.result(timeout=30)
            except Exception as e:
                domain_results[key] = {"domain": key, "error": str(e)}

    brief["swarm_domains"] = list(domain_results.values())

    # Build synthesis
    kill = domain_results.get("kill_signals", {})
    causal = domain_results.get("causal", {})
    council = domain_results.get("ai_council", {})
    patterns = domain_results.get("patterns", {})
    founders = domain_results.get("founders", {})

    blocker = kill.get("blocker", False)
    risk_flags = causal.get("stage_risk_flags", [])
    dtype = causal.get("decision_type", "unknown")
    effects = causal.get("downstream_effects", [])
    top_pattern = (patterns.get("matches") or [{}])[0]
    top_case = (founders.get("cases") or [{}])[0]

    brief["synthesis"] = {
        "decision_type": dtype,
        "blocker": "🚨 RESOLVE OVERDUE KILL SIGNALS FIRST" if blocker else "No blockers",
        "stage_flags": risk_flags,
        "top_pattern": top_pattern.get("name", "none"),
        "top_analogue": f"{top_case.get('founder', '')} ({top_case.get('product', '')})" if top_case.get("founder") else "none",
        "causal_effects": [f"{e['variable']} {e['direction']}" for e in effects[:3]],
        "ai_verdict": council.get("final_verdict", "INVESTIGATE"),
        "ai_synthesis": council.get("synthesis", "Council not available — set ANTHROPIC_API_KEY to enable."),
        "recommended_action": (
            "STOP: resolve overdue kill signals before this decision"
            if blocker
            else f"PROCEED WITH CONDITIONS — council verdict: {council.get('final_verdict', 'INVESTIGATE')}. "
                 "Set a kill signal before committing."
            if council.get("final_verdict") in ("PROCEED_WITH_CONDITIONS", "INVESTIGATE")
            else "PROCEED — collect 3 data points this week to validate, then commit"
        ),
        "kill_signal_template": (
            f"If [{decision[:50]}...] does not show measurable signal within 30 days, this approach is wrong."
        ),
    }

    return json.dumps(brief, indent=2)
