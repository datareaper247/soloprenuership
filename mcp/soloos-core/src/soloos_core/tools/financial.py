"""
SoloOS v7 — Financial Intelligence

Clean math. Real API calls. No heuristics pretending to be calculations.

Handles:
- Unit economics (LTV, CAC, payback, NRR)
- Runway calculations
- Valuation estimates
- Live Stripe MRR
- Live Mercury runway
- EV / decision value calculations

Phase E upgrades:
- calculate_unit_economics: auto-fills arpu + churn from DuckDB when available
- calculate_runway: auto-fills mrr from DuckDB when available
- get_stripe_mrr / get_mercury_runway: DuckDB cache layer (check recency, fall back to live)

All parameters remain Optional (None default) for backward compatibility.
If DuckDB has no data, behaviour is 100% identical to the pre-Phase-E version.
"""

import json
import math
import os
import base64
import urllib.request
import urllib.error
from typing import Optional


# ─────────────────────────────────────────────────────────────
# HTTP helper (Stripe/Mercury specific)
# ─────────────────────────────────────────────────────────────

def _api_get(url: str, auth_header: str, timeout: int = 10) -> dict:
    """Authenticated GET request. Raises on HTTP error."""
    req = urllib.request.Request(
        url,
        headers={"Authorization": auth_header, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:500]
        raise RuntimeError(f"HTTP {e.code}: {body}")


# ─────────────────────────────────────────────────────────────
# Unit Economics
# ─────────────────────────────────────────────────────────────

def calculate_unit_economics(
    arpu: Optional[float] = None,
    churn_rate_monthly_pct: Optional[float] = None,
    cac: float = 0.0,
    gross_margin_pct: float = 80.0,
    expansion_mrr_pct: float = 0.0,
) -> dict:
    """
    Calculate full unit economics from inputs.

    Args:
        arpu: Average Revenue Per User (monthly, dollars). Auto-filled from
              DuckDB (last-30-day revenue / unique customers) when not provided.
        churn_rate_monthly_pct: Monthly churn rate as percentage (e.g., 5.0 = 5%).
              Auto-filled from DuckDB when not provided.
        cac: Customer Acquisition Cost (dollars)
        gross_margin_pct: Gross margin percentage (default 80% for SaaS)
        expansion_mrr_pct: Monthly expansion revenue as % of MRR (upsell/cross-sell)

    Returns: Full unit economics dict with interpretation and data_source field.
    """
    data_source = "manual_input"

    # Try live data first — silently, never fail
    if arpu is None or churn_rate_monthly_pct is None:
        try:
            from ..data.analytics_db import get_analytics_db
            db = get_analytics_db()
            if db.has_data():
                if arpu is None:
                    live_arpu = db.get_current_arpu()
                    if live_arpu is not None:
                        arpu = live_arpu
                        data_source = "live_stripe"
                if churn_rate_monthly_pct is None:
                    live_churn = db.get_churn_rate()
                    if live_churn:
                        churn_rate_monthly_pct = live_churn * 100
                        data_source = "live_stripe"
        except Exception:
            pass  # fail-open — never let DB errors surface to caller

    # Fall back gracefully — arpu is the only truly required input
    if arpu is None:
        return {
            "error": (
                "arpu is required. Provide it manually or connect Stripe "
                "(set STRIPE_API_KEY and run a sync)."
            ),
            "data_source": "manual_input",
        }

    # Churn has a safe default when not provided
    if churn_rate_monthly_pct is None:
        churn_rate_monthly_pct = 5.0  # conservative SaaS default

    if churn_rate_monthly_pct <= 0:
        churn_rate_monthly_pct = 0.1  # Prevent division by zero

    churn_decimal = churn_rate_monthly_pct / 100
    gm_decimal = gross_margin_pct / 100

    # LTV = ARPU × (1 / monthly_churn_rate) × gross_margin
    avg_customer_lifetime_months = 1 / churn_decimal
    ltv = arpu * avg_customer_lifetime_months * gm_decimal

    # LTV:CAC ratio
    ltv_cac = ltv / cac if cac > 0 else float("inf")

    # CAC Payback period (months to recover CAC)
    monthly_gm_per_customer = arpu * gm_decimal
    payback_months = cac / monthly_gm_per_customer if monthly_gm_per_customer > 0 else float("inf")

    # NRR (Net Revenue Retention) = 1 - churn + expansion
    nrr_pct = (1 - churn_decimal + expansion_mrr_pct / 100) * 100

    # Interpretation
    if ltv_cac >= 3:
        ltv_cac_verdict = "HEALTHY (3x+ is the B2B SaaS benchmark)"
    elif ltv_cac >= 1:
        ltv_cac_verdict = "MARGINAL (paying for customers, barely profitable)"
    else:
        ltv_cac_verdict = "UNDERWATER (spending more acquiring than earning — fix before scaling)"

    if payback_months <= 12:
        payback_verdict = "STRONG (< 12mo payback — can scale)"
    elif payback_months <= 24:
        payback_verdict = "ACCEPTABLE (12-24mo — tight at early stage)"
    else:
        payback_verdict = "SLOW (> 24mo — capital-intensive; fix CAC or churn first)"

    if nrr_pct >= 110:
        nrr_verdict = "EXCEPTIONAL (>110% — product is growing customers in place)"
    elif nrr_pct >= 100:
        nrr_verdict = "GOOD (100-110% — net growth even with churn)"
    else:
        nrr_verdict = f"LEAKY ({nrr_pct:.0f}% — losing revenue to churn faster than expanding)"

    return {
        "inputs": {
            "arpu_monthly": f"${arpu:,.2f}",
            "churn_monthly_pct": f"{churn_rate_monthly_pct:.1f}%",
            "cac": f"${cac:,.2f}",
            "gross_margin_pct": f"{gross_margin_pct:.0f}%",
            "expansion_mrr_pct": f"{expansion_mrr_pct:.1f}%",
        },
        "outputs": {
            "ltv": f"${ltv:,.0f}",
            "ltv_cac_ratio": f"{ltv_cac:.1f}x",
            "ltv_cac_verdict": ltv_cac_verdict,
            "avg_customer_lifetime_months": f"{avg_customer_lifetime_months:.1f} months",
            "cac_payback_months": f"{payback_months:.1f} months",
            "payback_verdict": payback_verdict,
            "nrr_pct": f"{nrr_pct:.1f}%",
            "nrr_verdict": nrr_verdict,
        },
        "kill_signal": (
            f"If LTV:CAC doesn't reach 3x within 6 months of optimization, "
            f"the unit economics model is broken — pivot acquisition or pricing strategy."
        ),
        "highest_leverage_action": (
            "Fix churn first" if churn_rate_monthly_pct > 5
            else "Reduce CAC" if ltv_cac < 2
            else "Add expansion revenue (upsell/cross-sell)" if nrr_pct < 100
            else "Scale acquisition — unit economics are healthy"
        ),
        "data_source": data_source,
    }


def calculate_runway(
    cash_on_hand: float,
    monthly_burn: float,
    mrr: Optional[float] = None,
    expected_mrr_growth_pct: float = 0.0,
) -> dict:
    """
    Calculate runway with optional MRR growth modeling.

    Args:
        cash_on_hand: Current cash balance (dollars) — required
        monthly_burn: Total monthly expenses (dollars) — required
        mrr: Current MRR (dollars). Auto-filled from DuckDB when not provided.
        expected_mrr_growth_pct: Expected MoM MRR growth (e.g., 10.0 = 10%)

    Returns: Runway analysis with alert level, actions, and data_source field.
    """
    if monthly_burn <= 0:
        return {"error": "monthly_burn must be > 0"}

    data_source = "manual_input"

    # Try live MRR from DuckDB when not provided
    if mrr is None:
        try:
            from ..data.analytics_db import get_analytics_db
            db = get_analytics_db()
            if db.has_data():
                live_mrr = db.get_current_mrr()
                if live_mrr > 0:
                    mrr = live_mrr
                    data_source = "live_stripe"
        except Exception:
            pass  # fail-open

    # Safe default when still not set
    if mrr is None:
        mrr = 0.0

    net_burn = monthly_burn - mrr
    if net_burn <= 0:
        return {
            "status": "PROFITABLE",
            "message": f"Revenue (${mrr:,.0f}/mo) exceeds burn (${monthly_burn:,.0f}/mo).",
            "net_cashflow_monthly": f"+${abs(net_burn):,.0f}",
            "cash_preservation": "Cash is growing. Focus on growth, not survival.",
            "data_source": data_source,
        }

    # Simple runway
    simple_runway_months = cash_on_hand / net_burn

    # Growth-adjusted runway (if MRR growing, net burn decreases over time)
    growth_runway_months = simple_runway_months  # Default to simple if no growth
    if expected_mrr_growth_pct > 0:
        # Simulate month by month
        running_cash = cash_on_hand
        running_mrr = mrr
        growth_factor = 1 + expected_mrr_growth_pct / 100
        for month in range(1, 37):  # Max 3 years
            running_mrr *= growth_factor
            running_net_burn = monthly_burn - running_mrr
            if running_net_burn <= 0:
                growth_runway_months = month
                break
            running_cash -= running_net_burn
            if running_cash <= 0:
                growth_runway_months = month - 1 + (running_cash + running_net_burn) / running_net_burn
                break
        else:
            growth_runway_months = 36  # > 3 years

    # Alert level
    runway = simple_runway_months
    if runway > 18:
        alert = "GREEN"
        action = "Healthy runway. Optimize for growth, not survival."
    elif runway > 12:
        alert = "YELLOW"
        action = "Good runway. Start preparing next milestone NOW before it compresses."
    elif runway > 6:
        alert = "ORANGE"
        action = "Warning. Begin fundraising OR revenue sprint OR burn reduction immediately."
    elif runway > 3:
        alert = "RED"
        action = "CRITICAL. Reduce burn AND accelerate revenue. Both, simultaneously, now."
    else:
        alert = "CRITICAL"
        action = "EMERGENCY. < 3 months. Cut all non-essential costs today. Focus only on revenue."

    return {
        "inputs": {
            "cash_on_hand": f"${cash_on_hand:,.0f}",
            "monthly_burn": f"${monthly_burn:,.0f}",
            "current_mrr": f"${mrr:,.0f}",
            "net_burn_monthly": f"${net_burn:,.0f}",
        },
        "runway": {
            "simple_runway_months": f"{simple_runway_months:.1f}",
            "growth_adjusted_months": f"{growth_runway_months:.1f}" if expected_mrr_growth_pct > 0 else "not modeled",
            "alert_level": alert,
            "recommended_action": action,
        },
        "milestones": {
            "months_to_ramen": f"{cash_on_hand / monthly_burn:.1f} months at full burn (no revenue)",
            "break_even_mrr_needed": f"${monthly_burn:,.0f}/mo MRR would make you break-even",
            "mrr_to_green": f"${max(0, monthly_burn - mrr):,.0f}/mo MRR needed to reach positive cashflow",
        },
        "kill_signal": (
            f"If runway drops below 6 months without a clear path to break-even, "
            f"immediately cut burn to extend to 12 months OR close funding within 90 days."
        ),
        "data_source": data_source,
    }


def calculate_valuation(
    mrr: float,
    growth_rate_monthly_pct: float = 0.0,
    churn_rate_monthly_pct: float = 5.0,
    nrr_pct: float = 0.0,
    model: str = "saas",
    profitable: bool = False,
) -> dict:
    """
    Estimate company valuation using multiple methods.

    Args:
        mrr: Current Monthly Recurring Revenue
        growth_rate_monthly_pct: MoM growth rate (%)
        churn_rate_monthly_pct: Monthly churn rate (%)
        nrr_pct: Net Revenue Retention (%)
        model: "saas" | "service" | "marketplace" | "content"
        profitable: Whether the business is profitable

    Returns: Multi-method valuation estimate with acquirer context
    """
    arr = mrr * 12

    # Growth rate signals
    mom_growth = growth_rate_monthly_pct / 100
    yoy_growth_estimate = ((1 + mom_growth) ** 12 - 1) * 100 if mom_growth > 0 else 0

    # Revenue multiple range (by model and growth)
    base_multiples = {
        "saas": (2.0, 6.0),
        "service": (0.5, 1.5),
        "marketplace": (2.0, 5.0),
        "content": (1.0, 3.0),
    }
    low_multiple, high_multiple = base_multiples.get(model, (2.0, 4.0))

    # Adjust for growth
    if yoy_growth_estimate > 100:
        high_multiple *= 2.0
        low_multiple *= 1.5
    elif yoy_growth_estimate > 50:
        high_multiple *= 1.5
        low_multiple *= 1.2
    elif yoy_growth_estimate < 20:
        low_multiple *= 0.7
        high_multiple *= 0.8

    # Adjust for churn
    if churn_rate_monthly_pct > 10:
        low_multiple *= 0.5
        high_multiple *= 0.6
    elif churn_rate_monthly_pct > 5:
        low_multiple *= 0.8
        high_multiple *= 0.85

    # ARR-based valuation
    arr_valuation_low = arr * low_multiple
    arr_valuation_high = arr * high_multiple

    # MRR-based (common for small acquisitions on Acquire.com, MicroAcquire)
    # Micro-acquisition: 2-4x ARR is typical for <$500K ARR businesses
    if arr < 500_000:
        micro_multiple_low = 2.0
        micro_multiple_high = 4.0
        if profitable:
            micro_multiple_high = 5.0
        micro_val_low = arr * micro_multiple_low
        micro_val_high = arr * micro_multiple_high
    else:
        micro_val_low = None
        micro_val_high = None

    # Build result
    result = {
        "inputs": {
            "mrr": f"${mrr:,.0f}",
            "arr": f"${arr:,.0f}",
            "model": model,
            "growth_yoy_estimate": f"{yoy_growth_estimate:.0f}%",
            "monthly_churn": f"{churn_rate_monthly_pct:.1f}%",
        },
        "valuation_estimates": {
            "arr_multiple_range": f"{low_multiple:.1f}x–{high_multiple:.1f}x ARR",
            "estimated_value_low": f"${arr_valuation_low:,.0f}",
            "estimated_value_high": f"${arr_valuation_high:,.0f}",
        },
        "acquirer_contexts": {
            "strategic_buyer": f"${arr_valuation_high * 1.3:,.0f} (1.3x strategic premium on high estimate)",
            "financial_buyer": f"${arr_valuation_low:,.0f}–${arr_valuation_high:,.0f}",
            "micro_acquisition": f"${micro_val_low:,.0f}–${micro_val_high:,.0f}" if micro_val_low else "N/A for this scale",
        },
        "value_drivers": {
            "most_impactful": "Churn reduction" if churn_rate_monthly_pct > 5 else "Growth rate",
            "churn_impact": f"Reducing monthly churn from {churn_rate_monthly_pct:.1f}% to 2% would increase valuation by ~{((churn_rate_monthly_pct - 2) / churn_rate_monthly_pct * 30):.0f}%",
        },
        "platforms": [
            "Acquire.com (micro-SaaS, < $5M)",
            "MicroAcquire (renamed to Acquire.com)",
            "Empire Flippers ($50K–$50M)",
            "FE International ($1M+)",
        ],
        "caveat": "These are ranges based on market comps. Actual valuation depends on buyer, deal terms, and due diligence findings.",
    }

    return result


def calculate_ev(
    option_a_outcomes: list[tuple[float, float]],
    option_b_outcomes: list[tuple[float, float]],
    option_a_name: str = "Option A",
    option_b_name: str = "Option B",
) -> dict:
    """
    Calculate Expected Value for two options.

    Args:
        option_a_outcomes: List of (probability, value) tuples. Probabilities must sum to 1.0.
        option_b_outcomes: Same for option B.
        option_a_name: Label for option A
        option_b_name: Label for option B

    Returns: EV comparison with interpretation
    """
    def _ev(outcomes: list[tuple[float, float]]) -> float:
        return sum(p * v for p, v in outcomes)

    ev_a = _ev(option_a_outcomes)
    ev_b = _ev(option_b_outcomes)

    winner = option_a_name if ev_a > ev_b else option_b_name
    diff = abs(ev_a - ev_b)
    diff_pct = (diff / max(abs(ev_a), abs(ev_b), 1)) * 100

    return {
        option_a_name: {
            "expected_value": f"${ev_a:,.0f}",
            "outcomes": [{"probability": f"{p:.0%}", "value": f"${v:,.0f}"} for p, v in option_a_outcomes],
        },
        option_b_name: {
            "expected_value": f"${ev_b:,.0f}",
            "outcomes": [{"probability": f"{p:.0%}", "value": f"${v:,.0f}"} for p, v in option_b_outcomes],
        },
        "verdict": f"{winner} has higher EV by ${diff:,.0f} ({diff_pct:.0f}%)",
        "confidence_note": (
            "EV is a mathematical tool, not a prediction. "
            "It's most useful when probabilities are based on data, not intuition. "
            "If your probability estimates are gut feelings, widen the ranges and rerun."
        ),
    }


# ─────────────────────────────────────────────────────────────
# Live Stripe MRR  (Phase E: DuckDB cache layer)
# ─────────────────────────────────────────────────────────────

def get_stripe_mrr(stripe_api_key: str = "", include_trials: bool = False) -> dict:
    """
    Pull MRR from Stripe. Checks DuckDB cache first (if synced within 1 hour),
    falls back to direct Stripe API call when cache is stale or empty.

    Phase E upgrade: data_source field = "live_stripe_cached" | "live_stripe" | error.
    """
    # Check DuckDB cache first
    try:
        from ..data.analytics_db import get_analytics_db
        from datetime import datetime, timezone, timedelta

        db = get_analytics_db()
        sync_state = db.get_sync_state("stripe")
        last_synced = sync_state.get("last_synced_at")

        if last_synced and db.has_data():
            # Parse the synced_at timestamp — DuckDB may return datetime or string
            if isinstance(last_synced, str):
                # Remove timezone info for naive comparison
                last_synced_dt = datetime.fromisoformat(last_synced.replace("Z", "+00:00"))
            else:
                last_synced_dt = last_synced
            # Make both tz-aware for comparison
            now = datetime.now(timezone.utc)
            if last_synced_dt.tzinfo is None:
                last_synced_dt = last_synced_dt.replace(tzinfo=timezone.utc)
            age = now - last_synced_dt
            if age < timedelta(hours=1):
                # Cache is fresh — compute from DuckDB
                mrr = db.get_current_mrr()
                arpu = db.get_current_arpu()
                return {
                    "live_mrr": f"${mrr:,.0f}",
                    "live_mrr_raw": mrr,
                    "arr_estimate": f"${mrr * 12:,.0f}",
                    "arpu_monthly": f"${arpu:,.0f}" if arpu is not None else "unknown",
                    "cache_age_minutes": int(age.total_seconds() / 60),
                    "data_source": "live_stripe_cached",
                }
    except Exception:
        pass  # fail-open — fall through to live API call

    # Live Stripe API call
    key = stripe_api_key or os.environ.get("STRIPE_API_KEY", "")
    if not key:
        return {
            "error": "STRIPE_API_KEY not set",
            "setup": "export STRIPE_API_KEY=sk_live_... (or sk_test_ for testing)",
            "data_source": "manual_input",
        }

    auth = "Basic " + base64.b64encode(f"{key}:".encode()).decode()

    try:
        # Fetch active subscriptions
        data = _api_get(
            "https://api.stripe.com/v1/subscriptions?status=active&limit=100&expand[]=data.plan",
            auth_header=auth,
        )
        subs = data.get("data", [])

        if not subs:
            return {
                "live_mrr": "$0",
                "customer_count": 0,
                "message": "No active subscriptions. Verify you're using the live API key.",
                "is_test_mode": key.startswith("sk_test_"),
                "data_source": "live_stripe",
            }

        # Normalize to monthly
        def _monthly_cents(sub: dict) -> int:
            total = 0
            for item in sub.get("items", {}).get("data", []):
                plan = item.get("plan", {})
                amount = plan.get("amount", 0)
                interval = plan.get("interval", "month")
                interval_count = plan.get("interval_count", 1)
                qty = item.get("quantity", 1)
                if interval == "year":
                    total += int(amount * qty / (12 * interval_count))
                elif interval == "week":
                    total += int(amount * qty * 52 / (12 * interval_count))
                else:
                    total += int(amount * qty / interval_count)
            return total

        monthly_cents_list = [_monthly_cents(s) for s in subs]
        mrr_cents = sum(monthly_cents_list)
        mrr = mrr_cents / 100
        customer_count = len(subs)
        arpu = mrr / customer_count if customer_count else 0

        return {
            "live_mrr": f"${mrr:,.0f}",
            "live_mrr_raw": mrr,
            "arr_estimate": f"${mrr * 12:,.0f}",
            "customer_count": customer_count,
            "arpu_monthly": f"${arpu:,.0f}",
            "is_test_mode": key.startswith("sk_test_"),
            "data_source": "live_stripe",
        }

    except RuntimeError as e:
        return {"error": str(e), "data_source": "live_stripe"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "data_source": "live_stripe"}


# ─────────────────────────────────────────────────────────────
# Live Mercury runway  (Phase E: DuckDB cache layer)
# ─────────────────────────────────────────────────────────────

def get_mercury_runway(
    mercury_api_key: str = "",
    monthly_burn: float = 0.0,
    mrr: float = 0.0,
) -> dict:
    """
    Pull cash balance and runway from Mercury. Checks DuckDB cache first
    (if synced within 1 hour), falls back to direct Mercury API call.

    Phase E upgrade: data_source field = "live_mercury_cached" | "live_mercury" | error.
    """
    # Check DuckDB cache for Mercury banking data
    try:
        from ..data.analytics_db import get_analytics_db
        from datetime import datetime, timezone, timedelta

        db = get_analytics_db()
        sync_state = db.get_sync_state("mercury")
        last_synced = sync_state.get("last_synced_at")

        if last_synced:
            if isinstance(last_synced, str):
                last_synced_dt = datetime.fromisoformat(last_synced.replace("Z", "+00:00"))
            else:
                last_synced_dt = last_synced
            now = datetime.now(timezone.utc)
            if last_synced_dt.tzinfo is None:
                last_synced_dt = last_synced_dt.replace(tzinfo=timezone.utc)
            age = now - last_synced_dt
            if age < timedelta(hours=1):
                # Cache is fresh — read balance from banking_events if available
                rows = db.query(
                    """
                    SELECT COALESCE(SUM(amount_cents), 0) / 100.0 AS total_cash
                    FROM revenue_events
                    WHERE source = 'mercury'
                    """
                )
                if rows:
                    total_cash = float(rows[0].get("total_cash") or 0.0)
                    if total_cash > 0:
                        # Reuse existing runway calc logic
                        runway_data: dict = {}
                        if monthly_burn > 0:
                            live_mrr = mrr or db.get_current_mrr()
                            net_burn = monthly_burn - live_mrr
                            if net_burn <= 0:
                                runway_data = {
                                    "alert": "GREEN",
                                    "runway_months": "inf (profitable)",
                                    "net_burn": f"+${abs(net_burn):,.0f}/mo positive cashflow",
                                }
                            else:
                                months = total_cash / net_burn
                                alert = "GREEN" if months > 18 else "YELLOW" if months > 12 else "ORANGE" if months > 6 else "RED" if months > 3 else "CRITICAL"
                                runway_data = {
                                    "alert": alert,
                                    "runway_months": f"{months:.1f}",
                                    "net_burn": f"${net_burn:,.0f}/mo",
                                }
                        return {
                            "total_cash": f"${total_cash:,.2f}",
                            "total_cash_raw": total_cash,
                            "runway": runway_data,
                            "cache_age_minutes": int(age.total_seconds() / 60),
                            "data_source": "live_mercury_cached",
                        }
    except Exception:
        pass  # fail-open

    # Live Mercury API call
    key = mercury_api_key or os.environ.get("MERCURY_API_KEY", "")
    if not key:
        return {
            "error": "MERCURY_API_KEY not set",
            "setup": "Mercury → Settings → API → Create read-only token. export MERCURY_API_KEY=...",
            "data_source": "manual_input",
        }

    auth = f"Bearer {key}"

    try:
        data = _api_get("https://api.mercury.com/api/v1/accounts", auth_header=auth)
        accounts = data.get("accounts", [])

        total_cash = sum(
            float(a.get("currentBalance", a.get("availableBalance", 0)))
            for a in accounts
        )
        account_details = [
            {
                "name": a.get("name", "Account"),
                "type": a.get("type", ""),
                "balance": f"${float(a.get('currentBalance', 0)):,.2f}",
            }
            for a in accounts
        ]

        runway_data = {}
        if monthly_burn > 0:
            net_burn = monthly_burn - mrr
            if net_burn <= 0:
                runway_data = {
                    "alert": "GREEN",
                    "runway_months": "inf (profitable)",
                    "net_burn": f"+${abs(net_burn):,.0f}/mo positive cashflow",
                }
            else:
                months = total_cash / net_burn
                alert = "GREEN" if months > 18 else "YELLOW" if months > 12 else "ORANGE" if months > 6 else "RED" if months > 3 else "CRITICAL"
                runway_data = {
                    "alert": alert,
                    "runway_months": f"{months:.1f}",
                    "net_burn": f"${net_burn:,.0f}/mo",
                    "action": calculate_runway(total_cash, monthly_burn, mrr)["runway"]["recommended_action"],
                }

        return {
            "total_cash": f"${total_cash:,.2f}",
            "total_cash_raw": total_cash,
            "accounts": account_details,
            "runway": runway_data,
            "data_source": "live_mercury",
        }

    except RuntimeError as e:
        return {"error": str(e), "data_source": "live_mercury"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "data_source": "live_mercury"}
