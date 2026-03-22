"""
SoloOS CLI — Terminal interface to the founder intelligence engine.

Usage:
    soloos pattern "should I add a free tier"
    soloos ev --activity "Cold DMs" --hours 3 --prob 0.12 --revenue 2400
    soloos market "AI resume builder"
    soloos stage 3500
    soloos validate "AI invoice reconciliation for accountants"
    soloos signals
    soloos stats
"""

import json
import sys
import argparse
from .kb_loader import ensure_loaded, search_patterns, get_patterns, search_founders, get_founders, get_markets
from .server import (
    match_pattern, calculate_ev, check_market, get_stage_advice,
    validate_idea_gates, check_kill_signals_tool, knowledge_base_stats,
    log_decision, session_synthesis,
)


# ─────────────────────────────────────────────────────────────
# Colors (ANSI — works on macOS/Linux terminals)
# ─────────────────────────────────────────────────────────────

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"

def bold(s): return f"{C.BOLD}{s}{C.RESET}"
def dim(s):  return f"{C.DIM}{s}{C.RESET}"
def green(s): return f"{C.GREEN}{s}{C.RESET}"
def red(s): return f"{C.RED}{s}{C.RESET}"
def yellow(s): return f"{C.YELLOW}{s}{C.RESET}"
def cyan(s): return f"{C.CYAN}{s}{C.RESET}"
def blue(s): return f"{C.BLUE}{s}{C.RESET}"


def header(title: str):
    line = "━" * 50
    print(f"\n{C.CYAN}{line}{C.RESET}")
    print(f"{C.BOLD}{C.WHITE}  {title}{C.RESET}")
    print(f"{C.CYAN}{line}{C.RESET}\n")


def divider():
    print(f"{C.DIM}{'─' * 50}{C.RESET}")


# ─────────────────────────────────────────────────────────────
# Command handlers
# ─────────────────────────────────────────────────────────────

def cmd_pattern(args):
    """Match patterns to a situation."""
    query = " ".join(args.query)
    header(f"PATTERN MATCH: {query[:40]}...")

    result = json.loads(match_pattern(query, top_n=args.n or 3))

    if result.get("patterns_found", 0) == 0:
        print(yellow("No strong pattern match. Try a more specific description."))
        return

    routing = result.get("routing", "")
    if routing:
        if "SYSTEM_1" in routing:
            print(green(f"⚡ {routing}"))
        else:
            print(yellow(f"🔍 {routing}"))
        print()

    for p in result["patterns"]:
        print(bold(f"{p['id']} — {p['name']}"))
        if p.get("category"):
            print(dim(f"  [{p['category']}]"))
        print(f"  {cyan('Situation:')} {p.get('situation', '')[:100]}")
        print(f"  {cyan('Pattern:')}  {p.get('pattern', '')[:120]}")
        if p.get("real_example"):
            print(f"  {cyan('Evidence:')} {p['real_example'][:100]}")
        print(f"  {red('Kill:')}     {p.get('kill_signal', '')[:100]}")
        if p.get("reversibility"):
            print(f"  {cyan('Rev:')}      {p['reversibility']}")
        print()


def cmd_ev(args):
    """Calculate expected value for activities."""
    header("EXPECTED VALUE CALCULATOR")

    if not args.activities:
        # Interactive mode
        print("Enter activities (press Enter twice when done):")
        print(dim("  Format: name, hours, probability(%), revenue_impact($)"))
        print()
        activities = []
        while True:
            line = input(f"  Activity {len(activities)+1}: ").strip()
            if not line:
                if activities:
                    break
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 4:
                try:
                    activities.append({
                        "name": parts[0],
                        "hours": float(parts[1]),
                        "probability": float(parts[2]) / 100,
                        "revenue_impact": float(parts[3].replace("$", "").replace(",", "")),
                    })
                except ValueError:
                    print(red(f"  Invalid format. Use: name, hours, prob%, $revenue"))
    else:
        activities = args.activities

    if not activities:
        print(red("No activities provided."))
        return

    result = json.loads(calculate_ev(activities, use_monte_carlo=getattr(args, "monte_carlo", False)))

    print(f"  {bold('WINNER:')} {green(result['winner'])} @ {bold(result['winner_ev_per_hour'])}\n")

    for act in result["ranked_activities"]:
        rank_color = green if act["rank"] == 1 else (yellow if act["rank"] == 2 else dim)
        rank_label = f"#{act['rank']}"
        print(f"  {rank_color(rank_label)} {act['name']}")
        print(f"     Hours: {act['hours']}h  |  Prob: {act['probability']}  |  EV: {act['ev']}  |  {bold(act['ev_per_hour'])}")
        if "monte_carlo" in act:
            mc = act["monte_carlo"]
            print(f"     Monte Carlo: {mc['p10_pessimistic']} → {mc['p50_median']} → {mc['p90_optimistic']}")
        print()

    print(dim(f"  Caveat: {result['caveat'][:100]}"))


def cmd_market(args):
    """Check market saturation."""
    category = " ".join(args.category)
    header(f"MARKET INTELLIGENCE: {category}")

    result = json.loads(check_market(category))

    if "error" in result or result.get("status") == "not_found":
        print(yellow(f"  '{category}' not found in market database."))
        closest = result.get("closest_categories", [])
        if closest:
            print(f"  Closest: {', '.join(closest[:3])}")
        heuristics = result.get("heuristics", {})
        if heuristics:
            print(f"\n  {dim('General heuristics:')}")
            print(f"  {heuristics.get('note', '')}")
        return

    saturation = result["saturation"]
    sat_color = {
        "Dead": red, "Saturated": red, "Viable-with-niche": yellow,
        "Open": green, "Emerging": cyan,
    }.get(saturation, dim)

    print(f"  Category:   {bold(result['category'])}")
    print(f"  Saturation: {sat_color(bold(saturation))}")
    print(f"  Verdict:    {result['verdict']}")
    print()
    print(f"  Signal:     {dim(result.get('signal', '')[:120])}")
    print()

    ue = result.get("unit_economics", {})
    if any(ue.values()):
        print(f"  {bold('Unit Economics:')}")
        for k, v in ue.items():
            if v:
                print(f"    {k}: {v}")


def cmd_stage(args):
    """Get stage-calibrated advice."""
    mrr = args.mrr
    topic = " ".join(args.topic) if args.topic else ""
    header(f"STAGE ADVICE: {mrr} MRR")

    result = json.loads(get_stage_advice(str(mrr), topic))

    print(f"  Stage:      {bold(result['stage'])}")
    print(f"  Objective:  {cyan(result['primary_objective'])}")
    print()

    print(bold("  FOCUS ON:"))
    for f in result["what_to_focus"]:
        print(f"    {green('✓')} {f}")

    print()
    print(bold("  DO NOT DO:"))
    for a in result["what_not_to_do"]:
        print(f"    {red('✗')} {a}")

    print()
    print(f"  {bold('Biggest mistake at this stage:')} {yellow(result.get('biggest_mistake_at_stage', result.get('biggest_mistake', '')))}")
    print(f"  {bold('Watch:')} {result.get('metric_to_watch', '')}")

    flags = result.get("topic_flags", [])
    if flags:
        print()
        for flag in flags:
            print(f"  {yellow(flag)}")


def cmd_validate(args):
    """Validate an idea through all gates."""
    idea = " ".join(args.idea)
    header(f"IDEA VALIDATION: {idea[:50]}...")

    result = json.loads(validate_idea_gates(
        idea=idea,
        category=getattr(args, "category", "") or "",
        self_is_customer=getattr(args, "self", False),
        heard_from_customers=getattr(args, "heard", 0) or 0,
    ))

    verdict = result["overall_verdict"]
    if "🟢" in verdict:
        vcolor = green
    elif "🟡" in verdict:
        vcolor = yellow
    else:
        vcolor = red

    print(f"  {bold('VERDICT:')} {vcolor(verdict)}")
    print(f"  {bold('NEXT:')}    {result['next_step']}")
    print()

    gates = result["gates"]
    for gate_name, gate in gates.items():
        if not isinstance(gate, dict):
            continue
        status = gate.get("status", "")
        if not status:
            continue
        status_icon = "✅" if "PASS" in status or "LOW_RISK" in status else ("⚠️" if "UNCLEAR" in status or "WARNING" in status or "HIGH_RISK" in status else "❌")
        print(f"  {status_icon} {gate_name.upper().replace('_', ' ')}")
        finding = gate.get("finding") or gate.get("verdict") or gate.get("verdict") or ""
        if finding:
            print(f"     {dim(finding[:120])}")
        action = gate.get("action") or gate.get("next_step") or ""
        if action:
            print(f"     {cyan('→')} {action[:120]}")


def cmd_signals(args):
    """Check kill signals."""
    header("KILL SIGNAL CHECK")

    result = json.loads(check_kill_signals_tool())

    msg = result.get("session_start_message", "")
    if msg:
        if "⛔" in msg:
            print(f"  {red(msg)}")
        elif "🔴" in msg:
            print(f"  {yellow(msg)}")
        else:
            print(f"  {green(msg)}")
    print()

    alerts = result.get("alerts", [])
    if not alerts:
        print(dim("  No pending kill signals to check."))
        return

    for a in alerts:
        urgency = a["urgency"]
        color = red if urgency in ("OVERDUE", "URGENT") else (yellow if urgency == "WARNING" else green)
        print(f"  {color(f'[{urgency}]')} {bold(a['entry_id'])} — {a['summary'][:60]}")
        print(f"     Kill signal: {dim(a['kill_signal'][:80])}")
        print(f"     Due: {a['due_date']}  |  {a['action_required'][:80]}")
        print()


def cmd_stats(args):
    """Show knowledge base statistics."""
    header("SOLOOS CORE — KNOWLEDGE BASE")

    result = json.loads(knowledge_base_stats())

    print(f"  {bold('Status:')}    {green(result['status'])}")
    print(f"  {bold('Version:')}   {result['version']}")
    print(f"  {bold('Root:')}      {dim(result['knowledge_base_root'])}")
    print()
    print(f"  {cyan('Patterns:')}         {result['patterns_loaded']}")
    print(f"  {cyan('Founder Cases:')}    {result['founder_cases_loaded']}")
    print(f"  {cyan('Market Categories:')} {result['market_categories_loaded']}")
    print(f"  {cyan('Log Entries:')}      {result['founder_log_entries']}")
    print(f"  {cyan('Pending Outcomes:')} {result['pending_outcomes']}")
    print()
    cats = result.get("pattern_categories", [])
    if cats:
        print(f"  {bold('Pattern Categories:')}")
        for c in sorted(cats):
            print(f"    · {c}")


# ─────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="soloos",
        description="SoloOS Founder Intelligence CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
commands:
  pattern    Match decision patterns to your situation
  ev         Calculate expected value per hour for competing activities
  market     Check market saturation for a category
  stage      Get stage-calibrated advice for your MRR
  validate   Run idea through validation gates
  signals    Check overdue kill signals
  stats      Show knowledge base stats
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # pattern
    p_pattern = subparsers.add_parser("pattern", help="Match patterns to a situation")
    p_pattern.add_argument("query", nargs="+", help="Describe your situation")
    p_pattern.add_argument("-n", type=int, default=3, help="Number of patterns (default 3)")

    # ev
    p_ev = subparsers.add_parser("ev", help="Calculate EV/hr for activities")
    p_ev.add_argument("--monte-carlo", action="store_true", help="Run Monte Carlo simulation")
    p_ev.set_defaults(activities=None)

    # market
    p_market = subparsers.add_parser("market", help="Check market saturation")
    p_market.add_argument("category", nargs="+", help="Market category")

    # stage
    p_stage = subparsers.add_parser("stage", help="Get stage-calibrated advice")
    p_stage.add_argument("mrr", help="Current MRR e.g. '$3K' or '0'")
    p_stage.add_argument("topic", nargs="*", help="What you're asking about (optional)")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate an idea through all gates")
    p_val.add_argument("idea", nargs="+", help="The idea to validate")
    p_val.add_argument("--category", help="Market category")
    p_val.add_argument("--self", action="store_true", help="You are the target customer")
    p_val.add_argument("--heard", type=int, default=0, help="Number of customers who described this pain unprompted")

    # signals
    subparsers.add_parser("signals", help="Check overdue kill signals")

    # stats
    subparsers.add_parser("stats", help="Show knowledge base statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    ensure_loaded()

    dispatch = {
        "pattern": cmd_pattern,
        "ev": cmd_ev,
        "market": cmd_market,
        "stage": cmd_stage,
        "validate": cmd_validate,
        "signals": cmd_signals,
        "stats": cmd_stats,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
