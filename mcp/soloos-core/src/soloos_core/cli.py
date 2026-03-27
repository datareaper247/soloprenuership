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
    calculate_unit_economics, calculate_valuation, score_pmf,
    generate_competitor_brief, calculate_runway,
    monitor_competitor, enrich_prospect,
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


def cmd_unit_economics(args):
    result = json.loads(calculate_unit_economics(args.arpu, args.churn, args.gm, args.cac))
    header("UNIT ECONOMICS")
    print(f"  ARPU: {cyan(result['inputs']['arpu_monthly'])}  "
          f"Churn: {result['inputs']['monthly_churn']}  "
          f"GM: {result['inputs']['gross_margin']}")
    print()
    print(bold("LTV Methods:"))
    for k, v in result["ltv_methods"].items():
        print(f"  {dim(k.replace('_', ' ').title())}: {green(v)}")
    print()
    print(bold("Key Ratios:"))
    for k, v in result["ratios"].items():
        print(f"  {k.replace('_', ' ').title()}: {cyan(str(v))}")
    print()
    print(bold("Health Assessment:"))
    for h in result["health_assessment"]:
        print(f"  {h}")
    print()
    print(f"  {bold('Action:')} {result['action']}")


def cmd_valuation(args):
    result = json.loads(calculate_valuation(args.arr, args.growth, args.nrr, sde_annual=args.sde))
    header("COMPANY VALUATION")
    m1 = result["method_1_arr_multiple"]
    print(f"  {bold('ARR:')} {cyan(result['inputs']['arr'])}  "
          f"Growth: {result['inputs']['yoy_growth']}  "
          f"NRR: {result['inputs']['nrr']}")
    print()
    print(bold("Method 1 — ARR Multiple:"))
    print(f"  Range: {green(m1['valuation_range'])}")
    print(f"  Midpoint: {bold(green(m1['midpoint']))}")
    print(f"  Multiple: {m1['adjusted_multiple']}")
    print()
    print(bold("Method 2 — Acquirer ROI:"))
    m2 = result["method_2_acquirer_roi"]
    print(f"  Strategic buyer max: {m2['strategic_buyer_max']}")
    print(f"  Typical bootstrapped deal: {green(m2['typical_bootstrapped_deal'])}")
    if result["method_3_sde_multiple"] != "Provide sde_annual for SDE-based valuation":
        m3 = result["method_3_sde_multiple"]
        print()
        print(bold("Method 3 — SDE Multiple:"))
        print(f"  Range: {green(m3['sde_valuation_low'])} – {green(m3['sde_valuation_high'])}")
    print()
    print(bold("Value Levers:"))
    for lever in result["biggest_value_levers"]:
        print(f"  {lever}")
    print()
    print(f"  {cyan(result['key_insight'])}")


def cmd_pmf(args):
    result = json.loads(score_pmf(
        args.ellis, args.nrr, args.l30, args.referral,
        args.churn, args.weeks, args.customers
    ))
    header("PMF SCORE")
    print(f"  Score: {bold(cyan(result['pmf_score']))}")
    print(f"  Verdict: {bold(result['verdict'])}")
    print()
    print(bold("Signals:"))
    for s in result["signals"]:
        print(f"  {s}")
    if result["gaps_to_close"]:
        print()
        print(bold("Gaps to Close:"))
        for g in result["gaps_to_close"]:
            print(f"  {yellow('→')} {g}")
    if result["warnings"]:
        print()
        for w in result["warnings"]:
            print(f"  {yellow(w)}")
    print()
    print(f"  {bold('Scale Gate:')} {result['scale_gate']}")


def cmd_runway(args):
    result = json.loads(calculate_runway(
        args.cash, args.burn, args.mrr, args.churn, args.new_mrr
    ))
    header("RUNWAY PROJECTION")
    print(f"  Cash: {cyan(result['inputs']['cash_balance'])}  "
          f"Burn: {result['inputs']['adjusted_burn_with_buffer']}")
    print(f"  MRR: {cyan(result['inputs']['current_mrr'])}")
    print()
    print(f"  Naive runway: {dim(result['naive_runway'])}")
    print(f"  {bold('True runway:')} {bold(cyan(str(result['true_runway_months']) + ' months'))}")
    print(f"  Status: {result['status']}")
    print(f"  Default alive: {'✅ YES' if result['default_alive'] else '🔴 NO'}")
    print()
    print(bold("Month-by-Month:"))
    for m in result["month_by_month"]:
        cash_str = f"${m['cash_remaining']:,.0f}"
        cashflow = m['net_cashflow']
        cf_str = green(f"+${cashflow:,.0f}") if cashflow >= 0 else red(f"-${abs(cashflow):,.0f}")
        print(f"  Mo {m['month']:>2}: MRR ${m['mrr']:>7,.0f}  Cashflow {cf_str:>20}  Cash {cash_str:>10}  {m['status']}")
    print()
    print(f"  Break-even MRR needed: {yellow(result['break_even_mrr'])}")
    print(f"  Gap to break-even: {yellow(result['mrr_gap_to_break_even'])}")
    print()
    print(f"  {bold('Action:')} {result['action']}")


def cmd_competitor(args):
    result = json.loads(generate_competitor_brief(args.name, args.pricing, args.icp))
    header(f"COMPETITOR AUTOPSY: {args.name.upper()}")
    print(result["template"])
    print()
    print(bold("Research Agenda (Priority Order):"))
    for i, item in enumerate(result["research_agenda"], 1):
        print(f"  {i}. {item}")
    if result["displacement_opportunities"]:
        print()
        print(bold("Displacement Opportunities Detected:"))
        for d in result["displacement_opportunities"]:
            print(f"  {green(d)}")
    print()
    print(bold("Live Research Commands (paste into Claude with MCPs):"))
    for cmd in result["live_research_commands"]:
        print(f"  {dim(cmd)}")


def cmd_monitor(args):
    result = json.loads(monitor_competitor(
        args.name,
        competitor_url=args.url,
        your_mrr=args.mrr,
        category=args.category,
        known_recent_changes=args.changes,
    ))
    header(f"COMPETITIVE BRIEF: {args.name.upper()}")
    print(f"{bold('Monitoring Intensity:')} {result['monitoring_intensity']}")
    print(f"{bold('Stage Context:')} {result['stage_context']}")
    print()
    print(bold("MCP Commands to Run Now (paste into Claude):"))
    for cmd in result["mcp_commands_to_run_now"]:
        print(f"  {dim(cmd)}")
    print()
    print(bold("Signal Classification:"))
    for signal_type, signals in result["signal_classification"].items():
        print(f"  {bold(signal_type)}")
        for s in signals:
            print(f"    • {s}")
    print()
    print(bold("Displacement Trigger:"))
    print(f"  {result['displacement_outreach_trigger']}")
    print()
    print(bold("Kill Signal:"))
    print(f"  {red(result['kill_signal'])}")


def cmd_setup(args):
    """Interactive first-run setup wizard — writes env vars to ~/.soloos/.env."""
    import shutil
    from pathlib import Path

    header("SOLOOS SETUP WIZARD")
    print(f"  Writes your config to {cyan('~/.soloos/.env')}")
    print(f"  {dim('Press Enter to skip any field.')}\n")

    env_path = Path.home() / ".soloos" / ".env"
    env_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing values so we show defaults
    existing: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                existing[k.strip()] = v.strip()

    fields = [
        ("ANTHROPIC_API_KEY",    "Anthropic API key",         "sk-ant-..."),
        ("RESEND_API_KEY",       "Resend API key (email)",    "re_..."),
        ("RESEND_FROM_EMAIL",    "From email address",        "ai@yourdomain.com"),
        ("STRIPE_SECRET_KEY",    "Stripe secret key",         "sk_live_..."),
        ("STRIPE_WEBHOOK_SECRET","Stripe webhook secret",     "whsec_..."),
        ("GITHUB_WEBHOOK_SECRET","GitHub webhook secret",     "gh_..."),
        ("SOLOOS_SLACK_WEBHOOK", "Slack webhook URL (alerts)", "https://hooks.slack.com/..."),
        ("SOLOOS_NTFY_TOPIC",    "ntfy.sh topic (alerts)",    "your-topic"),
        ("MERCURY_API_KEY",      "Mercury bank API key",      ""),
        ("POSTHOG_API_KEY",      "PostHog API key",           "phc_..."),
    ]

    updates: dict[str, str] = {}
    for key, label, placeholder in fields:
        current = existing.get(key, "")
        display_default = f"[{current[:6]}...]" if current else f"[{placeholder}]"
        val = input(f"  {bold(label)} {dim(display_default)}: ").strip()
        if val:
            updates[key] = val
        elif current:
            updates[key] = current  # keep existing

    if not updates:
        print(yellow("\n  Nothing to save."))
        return

    # Write .env file
    lines = ["# SoloOS configuration — generated by `soloos setup`", ""]
    for k, v in updates.items():
        lines.append(f"{k}={v}")
    env_path.write_text("\n".join(lines) + "\n")
    print(green(f"\n  Saved {len(updates)} values to {env_path}"))

    # Remind user to source it
    shell_rc = "~/.zshrc" if shutil.which("zsh") else "~/.bashrc"
    print(f"\n  {dim('Add to your shell profile to auto-load:')}")
    print(f"  {cyan(f'  echo \"source ~/.soloos/.env\" >> {shell_rc}')}")
    print()
    print(bold("  Next steps:"))
    print(f"  {green('1.')} Restart your terminal (or source ~/.soloos/.env)")
    print(f"  {green('2.')} Run: {cyan('soloos signals')}  — check kill signals")
    print(f"  {green('3.')} Run: {cyan('soloos stats')}    — verify knowledge base")
    print()


def cmd_log(args):
    """Tail or inspect the audit log / tool call log."""
    import json as _json
    from pathlib import Path

    if args.audit:
        log_file = Path.home() / ".soloos" / "logs" / "audit.jsonl"
        label = "AUDIT LOG"
    else:
        log_file = Path.home() / ".soloos" / "logs" / "tool_calls.jsonl"
        label = "TOOL CALLS LOG"

    header(f"{label}{' (live)' if args.follow else ''}")

    if not log_file.exists():
        print(yellow(f"  No log file yet: {log_file}"))
        print(dim("  (Run some tools first to populate it.)"))
        return

    def _fmt_line(line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        try:
            e = _json.loads(line)
            ts = (e.get("ts") or e.get("timestamp") or "")[:19]
            tool = e.get("tool_name") or e.get("action") or "?"
            success = e.get("success", True)
            dur = e.get("duration_ms")
            status = green("OK") if success else red("ERR")
            dur_str = dim(f" {dur}ms") if dur is not None else ""
            err = e.get("error", "")
            err_str = f" {red(err[:60])}" if err else ""
            return f"  {dim(ts)}  {status}  {bold(tool)}{dur_str}{err_str}"
        except Exception:
            return f"  {dim(line[:120])}"

    if args.follow:
        import time
        print(dim("  Ctrl-C to stop\n"))
        try:
            with log_file.open(encoding="utf-8") as fh:
                # Seek to end then watch for new lines
                fh.seek(0, 2)
                while True:
                    line = fh.readline()
                    if line:
                        out = _fmt_line(line)
                        if out:
                            print(out)
                    else:
                        time.sleep(0.3)
        except KeyboardInterrupt:
            print()
    else:
        n = args.lines or 50
        try:
            all_lines = log_file.read_text(encoding="utf-8").splitlines()
            for line in all_lines[-n:]:
                out = _fmt_line(line)
                if out:
                    print(out)
            print()
            print(dim(f"  Showing last {min(n, len(all_lines))} of {len(all_lines)} entries."))
            print(dim(f"  Use -f to tail live, --audit for audit log."))
        except Exception as exc:
            print(red(f"  Error reading log: {exc}"))


def cmd_prospect(args):
    result = json.loads(enrich_prospect(
        args.company,
        contact_name=args.contact,
        contact_role=args.role,
        your_product=args.product,
        your_mrr=args.mrr,
    ))
    header(f"PROSPECT BRIEF: {args.company.upper()}")
    print(f"{bold('Outreach Motion:')} {result['outreach_motion']}")
    print(f"{bold('Follow-up Sequence:')} {result['follow_up_sequence']}")
    print()
    print(bold("Research Agenda:"))
    for section, items in result["research_agenda"].items():
        print(f"  {bold(section.replace('_', ' ').title())}:")
        for item in items:
            print(f"    • {dim(item)}")
    print()
    print(bold("Outreach Variants:"))
    for key, v in result["outreach_variants"].items():
        print(f"\n  {bold(v['approach'])}")
        print(f"  Best for: {v['best_for']}")
        print(f"  {dim(v['template'][:200] + '...' if len(v['template']) > 200 else v['template'])}")
    print()
    print(bold("Kill Signal:"))
    print(f"  {red(result['kill_signal'])}")


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
  setup      Interactive first-run setup wizard (writes ~/.soloos/.env)
  pattern    Match decision patterns to your situation
  ev         Calculate expected value per hour for competing activities
  market     Check market saturation for a category
  stage      Get stage-calibrated advice for your MRR
  validate   Run idea through validation gates
  signals    Check overdue kill signals
  stats      Show knowledge base stats
  log        View or tail the tool call / audit log (-f to follow live)
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

    # uniteconomics
    p_ue = subparsers.add_parser("uniteconomics", help="Calculate LTV, CAC payback, health")
    p_ue.add_argument("arpu", type=float, help="Monthly ARPU in dollars")
    p_ue.add_argument("churn", type=float, help="Monthly churn rate (0.03 = 3%)")
    p_ue.add_argument("--gm", type=float, default=80, help="Gross margin % (default 80)")
    p_ue.add_argument("--cac", type=float, default=0, help="CAC in dollars")

    # valuation
    p_val2 = subparsers.add_parser("valuation", help="Multi-method company valuation")
    p_val2.add_argument("arr", type=float, help="Annual Recurring Revenue in dollars")
    p_val2.add_argument("growth", type=float, help="YoY growth rate % (50 = 50%)")
    p_val2.add_argument("--nrr", type=float, default=100, help="Net Revenue Retention % (default 100)")
    p_val2.add_argument("--sde", type=float, default=0, help="Annual SDE for SDE-multiple method")

    # pmf
    p_pmf = subparsers.add_parser("pmf", help="Score your Product-Market Fit")
    p_pmf.add_argument("--ellis", type=float, default=0, help="Sean Ellis %% Very Disappointed")
    p_pmf.add_argument("--nrr", type=float, default=0, help="Net Revenue Retention %%")
    p_pmf.add_argument("--l30", type=float, default=0, help="Day 30 retention %%")
    p_pmf.add_argument("--churn", type=float, default=0, help="Monthly churn %%")
    p_pmf.add_argument("--referral", type=float, default=0, help="%% new users from referral")
    p_pmf.add_argument("--customers", type=int, default=0, help="Number of paying customers")
    p_pmf.add_argument("--weeks", type=int, default=0, help="Weeks since launch")

    # runway
    p_runway = subparsers.add_parser("runway", help="Calculate true runway with MRR trajectory")
    p_runway.add_argument("cash", type=float, help="Cash balance in dollars")
    p_runway.add_argument("burn", type=float, help="Monthly operating expenses")
    p_runway.add_argument("--mrr", type=float, default=0, help="Current MRR")
    p_runway.add_argument("--new-mrr", type=float, default=0, help="New MRR added per month")
    p_runway.add_argument("--churn", type=float, default=0.05, help="Monthly MRR churn rate (0.05 = 5%%)")

    # competitor
    p_comp = subparsers.add_parser("competitor", help="Generate competitor autopsy template")
    p_comp.add_argument("name", help="Competitor name")
    p_comp.add_argument("--pricing", default="", help="Known pricing info")
    p_comp.add_argument("--icp", default="", help="Their known target ICP")

    # monitor — weekly competitive intelligence brief
    p_monitor = subparsers.add_parser("monitor", help="Weekly competitive intelligence brief")
    p_monitor.add_argument("name", help="Competitor name")
    p_monitor.add_argument("--url", default="", help="Their website URL")
    p_monitor.add_argument("--mrr", default="$0", help="Your current MRR")
    p_monitor.add_argument("--category", default="", help="Market category")
    p_monitor.add_argument("--changes", default="", help="Known recent changes")

    # prospect — 90-second prospect research brief
    p_prospect = subparsers.add_parser("prospect", help="90-second prospect research + outreach brief")
    p_prospect.add_argument("company", help="Target company name")
    p_prospect.add_argument("--contact", default="", help="Contact name")
    p_prospect.add_argument("--role", default="", help="Contact role/title")
    p_prospect.add_argument("--mrr", default="$0", help="Your current MRR")
    p_prospect.add_argument("--product", default="", help="What your product does (1 sentence)")

    # setup — first-run onboarding wizard
    subparsers.add_parser("setup", help="Interactive first-run setup wizard")

    # log — tail / inspect audit/tool logs
    p_log = subparsers.add_parser("log", help="View or tail the tool call / audit log")
    p_log.add_argument("-f", "--follow", action="store_true", help="Follow log in real time (like tail -f)")
    p_log.add_argument("-n", "--lines", type=int, default=50, help="Number of recent lines to show (default 50)")
    p_log.add_argument("--audit", action="store_true", help="Show audit.jsonl instead of tool_calls.jsonl")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # setup and log don't need KB loaded
    if args.command == "setup":
        cmd_setup(args)
        return
    if args.command == "log":
        cmd_log(args)
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
        "uniteconomics": cmd_unit_economics,
        "valuation": cmd_valuation,
        "pmf": cmd_pmf,
        "runway": cmd_runway,
        "competitor": cmd_competitor,
        "monitor": cmd_monitor,
        "prospect": cmd_prospect,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
