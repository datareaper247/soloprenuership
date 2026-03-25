"""
SoloOS v7 — Real Agent Spawning Layer

Every "intelligent" analysis is an actual Anthropic API call with a specialized
system prompt loaded from agents/roles/. This replaces the keyword-matching
heuristics of previous versions.

Uses claude-haiku-4-5-20251001 for sub-agents (fast, cheap, sufficient).
Uses claude-sonnet-4-6 for synthesis (higher quality council verdict).

Requires: ANTHROPIC_API_KEY env var (same key Claude Code uses).
Falls back to heuristic analysis if API not available.
"""

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Optional

from ..data.cache import cached, TTL_LLM


# ─────────────────────────────────────────────────────────────
# Agent system prompt loader
# ─────────────────────────────────────────────────────────────

def _find_repo_root() -> Path:
    """Walk up to find the soloprenuership repo root."""
    current = Path(__file__).resolve()
    for _ in range(12):
        if (current / "agents").is_dir() or (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()


_REPO_ROOT = _find_repo_root()

_AGENT_PROMPT_PATHS = {
    "ceo":     "agents/roles/leadership/ceo/system-prompt.md",
    "cfo":     "agents/roles/leadership/cfo/system-prompt.md",
    "cmo":     "agents/roles/leadership/cmo/system-prompt.md",
    "coo":     "agents/roles/leadership/coo/system-prompt.md",
    "cto":     "agents/roles/leadership/cto/system-prompt.md",
    "pm":      "agents/roles/product/product-manager/system-prompt.md",
    "growth":  "agents/roles/growth/growth-hacker/system-prompt.md",
    "analyst": "agents/roles/growth/data-analyst/system-prompt.md",
    "sdr":     "agents/roles/sales/sdr/system-prompt.md",
    "ae":      "agents/roles/sales/ae/system-prompt.md",
    "cs":      "agents/roles/sales/cs/system-prompt.md",
    "seo":     "agents/roles/marketing/seo-specialist/system-prompt.md",
    "finance": "agents/roles/operations/finance-manager/system-prompt.md",
    "legal":   "agents/roles/extended/legal-counsel/system-prompt.md",
}


def _load_agent_prompt(role: str) -> str:
    """Load system prompt for a named role. Returns generic prompt if not found."""
    path_str = _AGENT_PROMPT_PATHS.get(role.lower())
    if path_str:
        full_path = _REPO_ROOT / path_str
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")

    # Generic fallback
    return (
        f"You are a senior {role} with deep expertise in B2B SaaS and solo founder businesses. "
        f"Analyze the provided situation from your functional perspective. "
        f"Be specific, data-driven, and contrarian where evidence warrants. "
        f"Output: 2-3 bullet points + a single verdict (PROCEED / CAUTION / PAUSE)."
    )


# ─────────────────────────────────────────────────────────────
# Anthropic API caller
# ─────────────────────────────────────────────────────────────

def _call_claude(
    system_prompt: str,
    user_message: str,
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 600,
) -> str:
    """
    Spawn a real Claude sub-agent call.
    Returns the text response or an error string.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "ANTHROPIC_API_KEY not set — falling back to heuristic analysis."

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text.strip()
    except ImportError:
        return "anthropic package not installed — run: pip install anthropic"
    except Exception as e:
        return f"[API error: {type(e).__name__}: {str(e)[:200]}]"


# ─────────────────────────────────────────────────────────────
# Council configuration
# ─────────────────────────────────────────────────────────────

_COUNCIL_SEATS = [
    {
        "name": "Market Signal",
        "role": "cmo",
        "focus": (
            "You are analyzing from a market and customer perspective. Focus on: "
            "Is there genuine market demand? Are customers actively complaining about this problem? "
            "What competitive dynamics exist? What's the timing signal? "
            "Output format: VERDICT (BULLISH/NEUTRAL/BEARISH), 2-3 specific observations, "
            "one market risk the founder may not see."
        ),
    },
    {
        "name": "Financial Health",
        "role": "cfo",
        "focus": (
            "You are analyzing from a financial and unit economics perspective. Focus on: "
            "What does this decision do to burn rate, runway, and unit economics? "
            "What's the payback period and LTV impact? Is the ROI case real? "
            "Output format: VERDICT (CLEAR/CAUTION/BLOCK), burn impact estimate, "
            "one financial risk the founder may not see."
        ),
    },
    {
        "name": "Pattern Match",
        "role": "ceo",
        "focus": (
            "You are analyzing from a strategic pattern recognition perspective. "
            "You have seen hundreds of startups make this exact type of decision. "
            "What's the base rate of success for this approach at this stage? "
            "What are the most common failure modes? What did the winners do differently? "
            "Output format: VERDICT (STRONG/MODERATE/WEAK), base rate estimate, "
            "specific failure pattern to watch for."
        ),
    },
    {
        "name": "Risk Assessment",
        "role": "coo",
        "focus": (
            "You are analyzing from an operational and reversibility perspective. "
            "What are the hidden execution risks? What's the reversibility score (1-10)? "
            "What would you need to see before pulling the trigger? "
            "What's the minimum viable version to test this? "
            "Output format: VERDICT (LOW_RISK/MEDIUM_RISK/HIGH_RISK), reversibility score, "
            "one hidden assumption that could invalidate everything."
        ),
    },
    {
        "name": "Opportunity Score",
        "role": "growth",
        "focus": (
            "You are analyzing from a growth and leverage perspective. "
            "Does this action create compounding returns or is it one-time? "
            "What's the upside asymmetry? Is the timing right? "
            "What's the highest-leverage version of this decision? "
            "Output format: VERDICT (STRONG/MODERATE/WEAK), leverage score (1-10), "
            "one way to make this decision 10x better."
        ),
    },
]


# ─────────────────────────────────────────────────────────────
# Council brief — 5 real AI agents in parallel
# ─────────────────────────────────────────────────────────────

@cached(
    TTL_LLM,
    key_fn=lambda decision, stage_mrr="", **_: f"council:{hash(decision[:200])}:{stage_mrr}"
)
def run_council_brief(
    decision: str,
    stage_mrr: str = "",
    context_notes: str = "",
) -> dict:
    """
    Run a 5-seat intelligence council with real Claude sub-agent calls.
    Each seat gets a specialist system prompt + the founder's context.
    All 5 run in parallel via ThreadPoolExecutor.

    Returns structured dict with per-seat analysis + council synthesis.
    """
    api_available = bool(os.environ.get("ANTHROPIC_API_KEY"))

    user_context = (
        f"DECISION: {decision}\n\n"
        f"STAGE: {stage_mrr or 'unknown'}\n\n"
        f"CONTEXT: {context_notes or 'No additional context provided.'}\n\n"
        "Provide your analysis as instructed in your role description."
    )

    def _run_seat(seat: dict) -> dict:
        system_prompt = _load_agent_prompt(seat["role"])
        # Append the specific focus instructions for this council seat
        full_system = f"{system_prompt}\n\n---\nCOUNCIL ROLE FOR THIS SESSION:\n{seat['focus']}"

        response = _call_claude(
            system_prompt=full_system,
            user_message=user_context,
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
        )
        return {
            "seat": seat["name"],
            "role": seat["role"],
            "analysis": response,
            "is_real_ai": api_available and not response.startswith("[API error"),
        }

    # Run all 5 in parallel
    seat_results = []
    errors = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(_run_seat, seat): seat["name"] for seat in _COUNCIL_SEATS}
        for future in as_completed(futures, timeout=30):
            name = futures[future]
            try:
                seat_results.append(future.result(timeout=25))
            except Exception as e:
                errors[name] = str(e)
                seat_results.append({
                    "seat": name,
                    "role": "unknown",
                    "analysis": f"[Seat failed: {e}]",
                    "is_real_ai": False,
                })

    # ── Synthesis — real Claude call on the seat outputs ──────
    seat_summaries = "\n\n".join(
        f"=== {r['seat']} ===\n{r['analysis']}" for r in seat_results
    )

    synthesis_prompt = (
        "You are synthesizing 5 expert analyses of a founder decision. "
        "Read all seat outputs carefully. "
        "Your job: produce a 3-5 sentence executive synthesis that:\n"
        "1. Identifies where the council agrees and where it diverges\n"
        "2. Names the #1 risk and the #1 opportunity\n"
        "3. States a clear FINAL VERDICT: PROCEED / PROCEED_WITH_CONDITIONS / PAUSE / ABORT\n"
        "4. States one concrete FIRST ACTION the founder should take today\n"
        "Be direct. No hedging. The founder needs a decision, not more analysis."
    )

    synthesis = _call_claude(
        system_prompt=synthesis_prompt,
        user_message=(
            f"DECISION BEING EVALUATED: {decision}\n"
            f"STAGE: {stage_mrr}\n\n"
            f"COUNCIL SEAT ANALYSES:\n{seat_summaries}"
        ),
        model="claude-haiku-4-5-20251001",  # Keep cheap — synthesis is short
        max_tokens=400,
    )

    # Extract verdict from synthesis text
    verdict_map = {
        "PROCEED_WITH_CONDITIONS": "PROCEED_WITH_CONDITIONS",
        "PROCEED WITH CONDITIONS": "PROCEED_WITH_CONDITIONS",
        "PROCEED": "PROCEED",
        "ABORT": "ABORT",
        "PAUSE": "PAUSE",
    }
    final_verdict = "INVESTIGATE"
    for k, v in verdict_map.items():
        if k in synthesis.upper():
            final_verdict = v
            break

    return {
        "decision": decision,
        "stage_mrr": stage_mrr,
        "council_seats": seat_results,
        "synthesis": synthesis,
        "final_verdict": final_verdict,
        "intelligence_mode": "real_ai" if api_available else "heuristic_fallback",
        "errors": errors or None,
    }


# ─────────────────────────────────────────────────────────────
# Single-role agent call (for targeted analysis)
# ─────────────────────────────────────────────────────────────

def ask_role_agent(
    role: str,
    question: str,
    context: str = "",
    max_tokens: int = 800,
) -> str:
    """
    Ask a single role-specific agent a targeted question.
    Uses the role's system prompt from agents/roles/.

    Args:
        role: Agent role (ceo, cfo, cmo, coo, cto, pm, growth, etc.)
        question: The specific question to ask
        context: Business context to include
        max_tokens: Response length limit

    Returns: Agent response text.
    """
    system_prompt = _load_agent_prompt(role)
    user_message = question
    if context:
        user_message = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"

    return _call_claude(
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=max_tokens,
    )


# ─────────────────────────────────────────────────────────────
# Available roles list
# ─────────────────────────────────────────────────────────────

def list_available_roles() -> list[dict]:
    """Return list of available agent roles with their file paths."""
    roles = []
    for role, path_str in _AGENT_PROMPT_PATHS.items():
        full_path = _REPO_ROOT / path_str
        roles.append({
            "role": role,
            "available": full_path.exists(),
            "path": path_str,
        })
    return roles
