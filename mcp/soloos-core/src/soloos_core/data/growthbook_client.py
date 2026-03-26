"""
SoloOS V10 — GrowthBook A/B Testing Client

Thin wrapper around the GrowthBook Python SDK for self-hosted instances.

Config (env vars):
    GROWTHBOOK_API_HOST   — GrowthBook server URL (default: http://localhost:3100)
    GROWTHBOOK_CLIENT_KEY — SDK client key from the GrowthBook dashboard

Fail-open: if the growthbook package is not installed, or no env vars are set,
all methods return safe defaults without raising. The module is always importable.

Self-hosting:
    docker run -d -p 3100:3100 -e MONGODB_URI=mongodb://mongo/growthbook \\
        --link mongo growthbook/growthbook
    Then visit http://localhost:3100 to create an account.

Set after first login:
    GROWTHBOOK_API_HOST=http://localhost:3100
    GROWTHBOOK_CLIENT_KEY=sdk-<key-from-dashboard>
"""

import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Availability check (lazy — never imported at module level)
# ─────────────────────────────────────────────────────────────

def _growthbook_available() -> bool:
    """Return True if the growthbook package is importable."""
    try:
        import growthbook  # noqa: F401
        return True
    except ImportError:
        return False


# ─────────────────────────────────────────────────────────────
# GrowthBookClient
# ─────────────────────────────────────────────────────────────

class GrowthBookClient:
    """
    Wrapper around the GrowthBook Python SDK for self-hosted GrowthBook instances.

    All public methods are fail-open:
    - If the growthbook package is not installed, returns safe defaults.
    - If env vars are not set (not configured), returns safe defaults.
    - Never raises in the happy-path callers; errors are logged.

    Usage:
        client = get_growthbook_client()
        if client.is_configured():
            exp_id = client.create_experiment(
                name="Pricing Page CTA",
                hypothesis="Changing CTA from 'Start Trial' to 'Start Free' improves signups",
                metric="signup_conversion",
                variants=["control", "treatment"],
            )
    """

    def __init__(self) -> None:
        self._api_host: str = os.environ.get(
            "GROWTHBOOK_API_HOST", "http://localhost:3100"
        ).rstrip("/")
        self._client_key: str = os.environ.get("GROWTHBOOK_CLIENT_KEY", "")
        self._sdk_available: bool = _growthbook_available()

    # ── Configuration ──────────────────────────────────────────

    def is_configured(self) -> bool:
        """
        Return True only when:
        - growthbook SDK is installed
        - GROWTHBOOK_CLIENT_KEY is set (non-empty)
        """
        return self._sdk_available and bool(self._client_key)

    def _not_configured_response(self, method: str) -> dict:
        """Standard not-configured response for all methods."""
        return {
            "configured": False,
            "method": method,
            "message": (
                "GrowthBook not configured. Set GROWTHBOOK_API_HOST and "
                "GROWTHBOOK_CLIENT_KEY. Install: pip install 'soloos-core[ab-testing]'"
            ),
            "setup_url": f"{self._api_host}",
        }

    # ── Experiment management ───────────────────────────────────

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        metric: str,
        variants: list[str],
        traffic_split: Optional[list[float]] = None,
    ) -> dict:
        """
        Create a new A/B experiment in GrowthBook.

        Args:
            name: Human-readable experiment name (e.g. "Pricing CTA Test")
            hypothesis: What you expect to happen (e.g. "New CTA increases signups by 15%")
            metric: Primary metric to track (e.g. "signup_conversion", "mrr_per_user")
            variants: List of variant names; first is treated as control
                      (e.g. ["control", "variant_a", "variant_b"])
            traffic_split: Weight per variant. Must sum to 1.0.
                          Defaults to equal split across all variants.

        Returns:
            dict with experiment_id, setup_instructions, and kill_signal template.
            Falls back to a setup guide if GrowthBook is not configured.
        """
        if not self.is_configured():
            return self._not_configured_response("create_experiment")

        if not variants:
            variants = ["control", "treatment"]

        n = len(variants)
        if traffic_split is None:
            traffic_split = [round(1.0 / n, 4)] * n
        elif len(traffic_split) != n:
            traffic_split = [round(1.0 / n, 4)] * n

        # Normalise to sum exactly 1.0
        total = sum(traffic_split)
        if total > 0:
            traffic_split = [round(w / total, 4) for w in traffic_split]

        experiment_id = f"exp_{name.lower().replace(' ', '_')[:40]}"

        try:
            import httpx  # optional — used only if SDK doesn't expose REST

            payload = {
                "trackingKey": experiment_id,
                "name": name,
                "hypothesis": hypothesis,
                "metrics": [metric],
                "variations": [
                    {"id": str(i), "key": v, "name": v, "weight": traffic_split[i]}
                    for i, v in enumerate(variants)
                ],
                "status": "running",
            }

            resp = httpx.post(
                f"{self._api_host}/api/v1/experiments",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._client_key}",
                    "Content-Type": "application/json",
                },
                timeout=10.0,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                server_id = data.get("experiment", {}).get("id", experiment_id)
                return {
                    "experiment_id": server_id,
                    "tracking_key": experiment_id,
                    "name": name,
                    "hypothesis": hypothesis,
                    "metric": metric,
                    "variants": variants,
                    "traffic_split": traffic_split,
                    "status": "running",
                    "dashboard_url": f"{self._api_host}/experiments/{server_id}",
                    "kill_signal_template": (
                        f"KILL SIGNAL: If {metric} does not improve by at least 10% "
                        f"within 30 days, stop experiment and discard variant."
                    ),
                    "setup_instructions": self._get_sdk_setup_snippet(experiment_id, variants),
                }
            else:
                # Non-fatal — return local-only experiment record
                logger.warning("GrowthBook API returned %s: %s", resp.status_code, resp.text[:200])
        except Exception as exc:
            logger.warning("GrowthBook create_experiment failed (using local record): %s", exc)

        # Fallback: return local record without server persistence
        return {
            "experiment_id": experiment_id,
            "tracking_key": experiment_id,
            "name": name,
            "hypothesis": hypothesis,
            "metric": metric,
            "variants": variants,
            "traffic_split": traffic_split,
            "status": "local_only",
            "note": "GrowthBook server not reachable — experiment created locally. Dashboard will not show this experiment.",
            "kill_signal_template": (
                f"KILL SIGNAL: If {metric} does not improve by at least 10% "
                f"within 30 days, stop experiment and discard variant."
            ),
            "setup_instructions": self._get_sdk_setup_snippet(experiment_id, variants),
        }

    def get_experiment_results(self, experiment_id: str) -> dict:
        """
        Fetch results for a running or completed experiment.

        Returns statistical results including conversion rates per variant,
        relative uplift, p-value, and a plain-language recommendation.

        Args:
            experiment_id: The experiment ID returned by create_experiment()

        Returns:
            dict with per-variant stats, winner (if any), and recommendation.
        """
        if not self.is_configured():
            return self._not_configured_response("get_experiment_results")

        try:
            import httpx

            resp = httpx.get(
                f"{self._api_host}/api/v1/experiments/{experiment_id}/results",
                headers={"Authorization": f"Bearer {self._client_key}"},
                timeout=10.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", {})
                variants = results.get("variations", [])

                # Determine winner
                winner = None
                best_conversion = -1.0
                for v in variants:
                    cr = v.get("conversionRate", 0)
                    if cr > best_conversion:
                        best_conversion = cr
                        winner = v.get("key", "unknown")

                recommendation = self._generate_recommendation(variants, winner)

                return {
                    "experiment_id": experiment_id,
                    "status": results.get("status", "unknown"),
                    "variants": variants,
                    "winner": winner,
                    "recommendation": recommendation,
                    "dashboard_url": f"{self._api_host}/experiments/{experiment_id}",
                }
            elif resp.status_code == 404:
                return {
                    "experiment_id": experiment_id,
                    "status": "not_found",
                    "message": "Experiment not found in GrowthBook. Check the experiment ID.",
                }
            else:
                return {
                    "experiment_id": experiment_id,
                    "status": "api_error",
                    "http_status": resp.status_code,
                    "message": resp.text[:300],
                }
        except Exception as exc:
            logger.warning("GrowthBook get_experiment_results failed: %s", exc)
            return {
                "experiment_id": experiment_id,
                "status": "connection_error",
                "message": str(exc),
                "hint": f"Is GrowthBook running at {self._api_host}?",
            }

    def get_variation(self, experiment_id: str, user_id: str) -> str:
        """
        Get the variant assignment for a specific user in an experiment.

        Uses the GrowthBook SDK's consistent hashing to ensure the same user
        always gets the same variant.

        Args:
            experiment_id: The experiment tracking key
            user_id: Unique identifier for the user (e.g. customer_id, email hash)

        Returns:
            Variant key as a string (e.g. "control", "treatment").
            Returns "control" as safe default if SDK is unavailable.
        """
        if not self.is_configured():
            return "control"

        try:
            from growthbook import GrowthBook, Experiment

            gb = GrowthBook(attributes={"id": user_id})
            exp = Experiment(key=experiment_id, variations=["control", "treatment"])
            result = gb.run(exp)
            return result.value
        except Exception as exc:
            logger.warning("GrowthBook get_variation failed (returning control): %s", exc)
            return "control"

    def list_experiments(self, status: str = "all") -> list[dict]:
        """
        List experiments from GrowthBook.

        Args:
            status: Filter by status — "running", "completed", "stopped", or "all"

        Returns:
            List of experiment summaries with id, name, status, metric, variants.
            Returns empty list if GrowthBook is not configured or unreachable.
        """
        if not self.is_configured():
            return []

        try:
            import httpx

            params = {}
            if status != "all":
                params["status"] = status

            resp = httpx.get(
                f"{self._api_host}/api/v1/experiments",
                headers={"Authorization": f"Bearer {self._client_key}"},
                params=params,
                timeout=10.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                experiments = data.get("experiments", [])
                return [
                    {
                        "id": e.get("id", ""),
                        "name": e.get("name", ""),
                        "status": e.get("status", ""),
                        "hypothesis": e.get("hypothesis", ""),
                        "metrics": e.get("metrics", []),
                        "variation_count": len(e.get("variations", [])),
                        "dashboard_url": f"{self._api_host}/experiments/{e.get('id', '')}",
                    }
                    for e in experiments
                ]
            else:
                logger.warning("GrowthBook list_experiments returned %s", resp.status_code)
                return []
        except Exception as exc:
            logger.warning("GrowthBook list_experiments failed: %s", exc)
            return []

    def track_event(
        self,
        experiment_id: str,
        user_id: str,
        metric_name: str,
        value: float,
    ) -> bool:
        """
        Track a conversion or metric event for an experiment participant.

        Args:
            experiment_id: The experiment tracking key
            user_id: The user's unique identifier
            metric_name: Which metric to record (e.g. "signup_conversion", "mrr")
            value: Numeric value for the metric (e.g. 1.0 for conversion, dollar amount for MRR)

        Returns:
            True if the event was tracked successfully, False otherwise (fail-open).
        """
        if not self.is_configured():
            return False

        try:
            import httpx

            payload = {
                "experimentId": experiment_id,
                "userId": user_id,
                "metric": metric_name,
                "value": value,
            }
            resp = httpx.post(
                f"{self._api_host}/api/v1/experiments/{experiment_id}/events",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._client_key}",
                    "Content-Type": "application/json",
                },
                timeout=5.0,
            )
            return resp.status_code in (200, 201, 204)
        except Exception as exc:
            logger.warning("GrowthBook track_event failed: %s", exc)
            return False

    # ── Private helpers ─────────────────────────────────────────

    def _get_sdk_setup_snippet(self, experiment_id: str, variants: list[str]) -> str:
        """Generate Python SDK usage snippet for this experiment."""
        return (
            f"# Install: pip install growthbook\n"
            f"from growthbook import GrowthBook, Experiment\n\n"
            f"gb = GrowthBook(attributes={{\"id\": user_id}})\n"
            f"exp = Experiment(key=\"{experiment_id}\", variations={variants!r})\n"
            f"result = gb.run(exp)\n"
            f"variant = result.value  # e.g. \"{variants[0]}\" or \"{variants[-1]}\""
        )

    def _generate_recommendation(self, variants: list[dict], winner: Optional[str]) -> str:
        """Generate plain-language recommendation based on variant results."""
        if not variants:
            return "No data yet. Run the experiment longer to collect sufficient samples."

        control = next((v for v in variants if v.get("key") == "control"), None)
        if control is None and variants:
            control = variants[0]

        control_cr = control.get("conversionRate", 0) if control else 0
        winner_cr = max((v.get("conversionRate", 0) for v in variants), default=0)

        if winner_cr <= control_cr:
            return (
                "No improvement detected vs. control. "
                "Consider stopping the experiment and revisiting the hypothesis."
            )

        uplift = round((winner_cr - control_cr) / max(control_cr, 0.0001) * 100, 1)
        p_values = [v.get("pValue", 1.0) for v in variants if v.get("key") != "control"]
        min_p = min(p_values) if p_values else 1.0

        if min_p < 0.05:
            return (
                f"Statistically significant win: '{winner}' shows {uplift}% uplift "
                f"(p={min_p:.3f} < 0.05). Ship the winning variant."
            )
        elif min_p < 0.10:
            return (
                f"Trending positive: '{winner}' shows {uplift}% uplift "
                f"(p={min_p:.3f}). Run longer for significance (target p < 0.05)."
            )
        else:
            return (
                f"Inconclusive: '{winner}' shows {uplift}% nominal uplift "
                f"but p={min_p:.3f} — not statistically significant. Run longer or increase traffic."
            )


# ─────────────────────────────────────────────────────────────
# Module-level singleton
# ─────────────────────────────────────────────────────────────

_client: Optional[GrowthBookClient] = None


def get_growthbook_client() -> GrowthBookClient:
    """
    Return the module-level GrowthBookClient singleton.

    Initialised on first call. Always safe to call — returns a not-configured
    client if env vars are absent or growthbook is not installed.
    """
    global _client
    if _client is None:
        _client = GrowthBookClient()
    return _client


# ─────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = get_growthbook_client()
    print(f"GrowthBook configured: {client.is_configured()}")
    print(f"API host: {client._api_host}")

    if not client.is_configured():
        print(
            "Not configured — set GROWTHBOOK_API_HOST and GROWTHBOOK_CLIENT_KEY "
            "to connect to a running GrowthBook instance."
        )
        result = client.create_experiment(
            name="Test Experiment",
            hypothesis="Just a smoke test",
            metric="conversion",
            variants=["control", "treatment"],
        )
        print(f"Not-configured response: {json.dumps(result, indent=2)}")
    else:
        experiments = client.list_experiments()
        print(f"Active experiments: {len(experiments)}")
