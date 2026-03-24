"""
SoloOS v7 — Memory & Context Layer

Pure Python business logic for context management, session synthesis,
stage advice, and knowledge base tools. No MCP decorators.

Handles the EKG (Emergent Knowledge Graph) linking and founder log management.
"""

from __future__ import annotations

import json
import re
from typing import Optional

# ─────────────────────────────────────────────────────────────
# Stage playbooks (single source of truth)
# ─────────────────────────────────────────────────────────────

_STAGE_PLAYBOOKS: dict[str, dict] = {
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
        ],
        "biggest_mistake": "Building in stealth for 3+ months without a single customer conversation.",
        "patterns": ["P01 (Levels Test)", "P07 (Narrow ICP)", "P02 (Marc Lou Kill Test)", "P08 (Distribution First)"],
        "metric": "Number of paid pre-commitments (target: 5 before build)",
    },
    "early_traction": {
        "name": "$1–5K MRR — Early Traction",
        "objective": "PMF signal: retain 40% of customers at Day 30?",
        "focus": [
            "Weekly calls with every paying customer (5 minutes minimum)",
            "D30 retention: if <40%, fix retention before acquiring more",
            "Identify 1-2 customers who get most value — serve them exclusively",
            "Direct outreach (DMs, cold email) for acquisition — not channels",
        ],
        "avoid": [
            "Adding new features before understanding why current users churn",
            "Expanding to a second ICP",
            "SEO, content, paid ads",
            "Redesign or rebrand",
        ],
        "biggest_mistake": "Building new features instead of talking to churned users about why they left.",
        "patterns": ["P07 (Narrow ICP)", "P05 (Pricing Model)", "P11 (Community Distribution)"],
        "metric": "D30 retention rate (target: ≥40%). Monthly churn rate (target: <10%).",
    },
    "pmf_search": {
        "name": "$5–20K MRR — PMF Search",
        "objective": "Make acquisition repeatable: can you do this 10 more times?",
        "focus": [
            "Systematize the sales process that got you here",
            "Identify your single strongest acquisition channel (double it)",
            "First hire: customer success or operations (free founder for revenue)",
            "Begin SEO/content if organic searches already happening",
        ],
        "avoid": [
            "New ICPs or new products",
            "Fundraising (too early for most)",
            "Major product pivots",
            "Enterprise sales without proven process",
        ],
        "biggest_mistake": "Thinking $15K MRR = PMF. PMF = 40% 'very disappointed' on Sean Ellis test.",
        "patterns": ["P06 (Compliance Moat)", "P04 (Viral Output)", "P10 (Pieter Levels Flywheel)"],
        "metric": "Sean Ellis score (target: ≥40%). Net Revenue Retention (target: >100%).",
    },
    "scaling": {
        "name": "$20–50K MRR — Scaling",
        "objective": "Systematize operations. Hire to documented processes. One channel at a time.",
        "focus": [
            "First hire: the function consuming most of your time",
            "SOPs for support, onboarding, and sales before hiring",
            "Channel diversification: if 1 channel works, add 1 more (not 3)",
            "Pricing optimization: probably undercharging — run price test",
        ],
        "avoid": [
            "Multiple simultaneous channel experiments",
            "International expansion",
            "Adding a second product",
        ],
        "biggest_mistake": "Hiring without SOPs. Generating chaos instead of leverage.",
        "patterns": ["P06 (Compliance Moat)", "P04 (Viral Output)", "P08 (Distribution)"],
        "metric": "Revenue per employee. NPS score. Monthly churn rate.",
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


def _parse_mrr_string(mrr_str: str) -> int:
    """Convert '$3.5K', '$40,000', 'pre-revenue' to integer."""
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


# ─────────────────────────────────────────────────────────────
# Tool: get_stage_advice
# ─────────────────────────────────────────────────────────────

def get_stage_advice(
    mrr: str,
    question_topic: str = "",
) -> str:
    """
    Get stage-calibrated advice based on current MRR.
    Returns what to focus on, what NOT to do, key patterns, and biggest mistake at this stage.

    Use when inferring a founder's stage from conversation clues or when they state MRR.

    Args:
        mrr: Current MRR as string — "$0", "$3K", "$15K", "$40K", "pre-revenue", etc.
        question_topic: What they're asking about (for context-specific flags)
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

    data = _STAGE_PLAYBOOKS[stage]

    flags = []
    topic = question_topic.lower()
    if mrr_value < 5000 and any(k in topic for k in ["seo", "content", "blog", "backlink"]):
        flags.append("⚠️ STAGE MISMATCH: SEO requires 6-12 months. At <$5K MRR, direct outreach generates faster ROI.")
    if mrr_value < 20000 and any(k in topic for k in ["hire", "va", "team", "employee"]):
        flags.append("⚠️ PROCESS FIRST: Document the process before hiring. Hiring before documentation = chaos.")
    if mrr_value < 50000 and any(k in topic for k in ["international", "expand", "global"]):
        flags.append("⚠️ PREMATURE: Fix home-market churn first. International expansion at $50K+ MRR.")
    if mrr_value < 10000 and any(k in topic for k in ["paid ads", "facebook ads", "google ads", "ppc"]):
        flags.append("⚠️ UNIT ECONOMICS FIRST: Need LTV data before paid ads. What's your D30 retention?")
    if mrr_value < 50000 and any(k in topic for k in ["fundrais", "investor", "raise", "seed", "vc"]):
        flags.append("⚠️ STAGE CHECK: Fundraising below $50K MRR — model bootstrapped path first.")

    return json.dumps({
        "mrr_input": mrr,
        "mrr_parsed": f"${mrr_value:,}",
        "stage": data["name"],
        "primary_objective": data["objective"],
        "what_to_focus": data["focus"],
        "what_not_to_do": data["avoid"],
        "biggest_mistake_at_stage": data["biggest_mistake"],
        "key_patterns": data["patterns"],
        "metric_to_watch": data["metric"],
        "stage_flags": flags,
    }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: session_synthesis
# ─────────────────────────────────────────────────────────────

def session_synthesis(
    decisions_made: list[str],
    open_questions: list[str],
    assumptions_made: list[str],
    next_action: str,
    auto_log_decisions: bool = True,
) -> str:
    """
    Generate a structured SESSION WRAP at the end of a working session.
    Optionally creates founder-log stubs for kill signal tracking.

    Use at end of any session containing strategic decisions, experiments, or pivots.

    Args:
        decisions_made: Specific decisions made this session (not discussed, MADE)
        open_questions: What still needs answering before next session
        assumptions_made: What was assumed without data confirmation
        next_action: Single most important next step (named, specific)
        auto_log_decisions: If True, create FL-XXX stubs for each decision
    """
    try:
        from ..log_manager import (
            today_str, load_log, next_log_id, append_log_entry,
            due_date_str, FounderLogEntry,
        )
        today = today_str()
    except Exception:
        from datetime import date
        today = date.today().isoformat()
        load_log = lambda: []  # noqa: E731
        next_log_id = lambda _: "FL-000"  # noqa: E731
        append_log_entry = lambda _: None  # noqa: E731
        due_date_str = lambda n: "30 days from today"  # noqa: E731
        FounderLogEntry = None
        auto_log_decisions = False

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
        lines += ["", "OPEN QUESTIONS:"] + [f"  ? {q}" for q in open_questions]

    if assumptions_made:
        lines += ["", "ASSUMPTIONS MADE (UNCONFIRMED):"] + [f"  ⚠️ {a}" for a in assumptions_made]

    lines += ["", "NEXT:", f"  → {next_action}", "", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
    output["formatted_output"] = "\n".join(lines)

    if auto_log_decisions and decisions_made and FounderLogEntry is not None:
        try:
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
                entries.append(stub)
                output["logged_entries"].append({
                    "entry_id": entry_id,
                    "decision": decision,
                    "note": "Kill signal is TBD — update founder-log.md before next session",
                })
        except Exception as e:
            output["log_error"] = str(e)

    return json.dumps(output, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: get_business_context
# ─────────────────────────────────────────────────────────────

def get_business_context() -> str:
    """
    Read the founder's business-context.md and return structured current state.
    Use at session start to get context before giving advice.

    Returns: MRR, ICP, stage, top channel, biggest challenge, open decisions.
    """
    try:
        from ..log_manager import read_business_context, BUSINESS_CONTEXT_PATH, FOUNDER_LOG_PATH
        ctx = read_business_context()
        ctx["soloos_version"] = "v7"
        ctx["context_files_checked"] = [str(BUSINESS_CONTEXT_PATH), str(FOUNDER_LOG_PATH)]
        return json.dumps(ctx, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Could not read business context. Run /onboard to populate context files.",
        }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: update_context
# ─────────────────────────────────────────────────────────────

def update_context(
    file: str,
    content: str,
    mode: str = "overwrite",
) -> str:
    """
    Write or append to a SoloOS context file. Activates cross-session memory.

    Args:
        file: Which context file to update:
              "business-context" | "experiment-log" | "decision-log" |
              "customer-voice" | "mission" | "founder-profile"
        content: The markdown content to write
        mode: "overwrite" (replace entire file) or "append" (add to end)

    Returns: Confirmation with file path and byte count written.
    """
    try:
        from ..log_manager import (
            BUSINESS_CONTEXT_PATH, EXPERIMENT_LOG_PATH,
            DECISION_LOG_PATH, CUSTOMER_VOICE_PATH, CONTEXT_ROOT,
        )

        file_map = {
            "business-context": BUSINESS_CONTEXT_PATH,
            "experiment-log": EXPERIMENT_LOG_PATH,
            "decision-log": DECISION_LOG_PATH,
            "customer-voice": CUSTOMER_VOICE_PATH,
            "mission": CONTEXT_ROOT / "mission.md",
            "founder-profile": CONTEXT_ROOT / "founder-profile.md",
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
            "message": f"Context file '{file}' updated. Cross-session memory active.",
        }, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: knowledge_base_stats
# ─────────────────────────────────────────────────────────────

def knowledge_base_stats() -> str:
    """
    Return statistics about the SoloOS knowledge base.
    Shows how many patterns, founder cases, and markets are indexed.
    """
    try:
        from ..kb_loader import get_patterns, get_founders, get_markets, KB_ROOT
        from ..log_manager import load_log, FOUNDER_LOG_PATH, BUSINESS_CONTEXT_PATH

        patterns = get_patterns()
        founders = get_founders()
        markets = get_markets()
        log_entries = load_log()

        return json.dumps({
            "status": "ok",
            "kb_root": str(KB_ROOT),
            "patterns": {
                "count": len(patterns),
                "categories": list({p.category for p in patterns} if patterns else []),
            },
            "founder_cases": {"count": len(founders)},
            "market_intelligence": {"count": len(markets)},
            "founder_log": {
                "total_entries": len(log_entries),
                "pending_outcomes": sum(1 for e in log_entries if e.outcome_status == "⏳ Pending"),
                "path": str(FOUNDER_LOG_PATH),
            },
            "business_context": {
                "exists": BUSINESS_CONTEXT_PATH.exists(),
                "path": str(BUSINESS_CONTEXT_PATH),
            },
            "soloos_version": "v7",
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Knowledge base not fully initialized. Check kb_loader and log_manager.",
        }, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: log_decision (extracted from server.py)
# ─────────────────────────────────────────────────────────────

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

    Args:
        summary: One sentence: what was decided
        context: What prompted this decision (signal, conversation, data)
        hypothesis: What you expect to happen
        kill_signal: Specific measurable data that would prove this wrong
        kill_signal_days: Days from now to check kill signal (default 30)
        outcome_days: Days from now to assess outcome (default 30)
        decision_type: "Decision" / "Experiment" / "Pivot" / "Hire" / "Pricing"
        pattern_applied: Pattern ID if applied, e.g. "P-07"
    """
    try:
        from ..log_manager import (
            load_log, append_log_entry, next_log_id,
            today_str, due_date_str, FounderLogEntry,
        )
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
            "message": f"Decision logged as {entry_id}. Kill signal due in {kill_signal_days} days.",
            "ekg_reference": f"[[{entry_id}]]",
        }, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}, indent=2)


# ─────────────────────────────────────────────────────────────
# Tool: check_kill_signals_tool
# ─────────────────────────────────────────────────────────────

def check_kill_signals_tool() -> str:
    """
    Check all pending decisions in founder-log.md for overdue or approaching kill signals.
    This is the CHRONOS CHECK — fires at session start.

    Returns: All pending entries ranked by urgency (OVERDUE → URGENT → WARNING → OK).
    """
    try:
        from ..log_manager import load_log, check_kill_signals

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

        def _action(a) -> str:
            if a.urgency == "OVERDUE":
                return f"⛔ OVERDUE by {abs(a.days_remaining)} days. Record outcome NOW."
            elif a.urgency == "URGENT":
                return f"🔴 {a.days_remaining} days left. Schedule kill signal check this week."
            elif a.urgency == "WARNING":
                return f"🟡 {a.days_remaining} days left. Plan review before due date."
            return f"🟢 {a.days_remaining} days remaining. No action needed."

        def _session_msg() -> str:
            if overdue:
                return f"⛔ KILL SIGNAL CHECK: {len(overdue)} decision(s) OVERDUE. Address before any new work."
            elif urgent:
                return f"🔴 {len(urgent)} kill signal(s) due within 7 days."
            elif warning:
                return f"🟡 {len(warning)} kill signal(s) approaching (14 days). Good momentum."
            return "🟢 All kill signals on track. Clean session."

        return json.dumps({
            "status": "alerts_found" if (overdue or urgent) else "monitoring",
            "total_pending": len(pending),
            "overdue": len(overdue),
            "urgent": len(urgent),
            "warning": len(warning),
            "session_start_message": _session_msg(),
            "alerts": [
                {
                    "entry_id": a.entry_id,
                    "urgency": a.urgency,
                    "summary": a.summary,
                    "kill_signal": a.kill_signal,
                    "due_date": a.due_date,
                    "days_remaining": a.days_remaining,
                    "action_required": _action(a),
                }
                for a in alerts
            ],
        }, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "error": str(e), "alerts": []}, indent=2)
