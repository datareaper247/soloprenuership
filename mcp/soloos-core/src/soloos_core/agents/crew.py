"""
CrewAI multi-agent team configuration.
Dep: crewai>=0.11.0 (optional)

The crew:
- FounderAgent (orchestrator)
- ProductAgent (roadmap, features, user research)
- EngineeringAgent (code, deploy, bugs)
- MarketingAgent (content, social, email)
- FinanceAgent (MRR, runway, unit economics)
- CustomerSuccessAgent (support, NPS, retention)

Each agent:
- Has a specific role + goal + backstory
- Has access to a defined subset of SoloOS tools
- Reports to FounderAgent
- Operates within ActionRegistry permission limits

Weekly crew run (Monday 09:00):
1. FounderAgent reads World Model
2. Assigns weekly objectives to each agent
3. Agents execute autonomously within their domains
4. FounderAgent synthesizes outcomes → human weekly report
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_CREWAI_AVAILABLE = False
try:
    import crewai  # type: ignore[import]
    _CREWAI_AVAILABLE = True
except ImportError:
    pass


class _UnavailableCrew:
    """Stub when crewai not installed."""

    def run_weekly_crew(self) -> str:
        return (
            "Multi-agent crew unavailable.\n"
            "Install: pip install 'soloos-core[autonomous]'\n"
            "Then the weekly crew will run automatically on Mondays at 09:00."
        )


class SoloOSCrew:
    """
    CrewAI-powered multi-agent team.
    Falls back to individual agent calls when crewai not installed.
    """

    def __init__(self) -> None:
        if not _CREWAI_AVAILABLE:
            logger.info("crewai not installed — SoloOSCrew using direct agent mode")

    def run_weekly_crew(self) -> str:
        """Run the full multi-agent weekly crew."""
        if not _CREWAI_AVAILABLE:
            return self._run_direct_agents()

        return self._run_crewai()

    def _run_direct_agents(self) -> str:
        """Run agents directly without CrewAI orchestration."""
        from ..core.action_registry import is_kill_switch_active
        if is_kill_switch_active():
            return "Weekly crew blocked: kill switch active"

        from .founder_agent import FounderAgent
        from .customer_success_agent import CustomerSuccessAgent
        from .marketing_agent import MarketingAgent
        from .engineering_agent import EngineeringAgent

        results = []
        founder = FounderAgent()

        # 1. Strategy session
        strategy = founder.run_weekly_strategy()
        results.append(f"**Strategy**: {strategy.get('status', 'unknown')}")

        # 2. Customer success scan
        cs = CustomerSuccessAgent()
        churn_risks = cs.scan_churn_risks()
        results.append(f"**Customer Success**: {len(churn_risks)} churn risks identified")

        # 3. Marketing plan
        mkt = MarketingAgent()
        plan = mkt.generate_content_plan()
        results.append(f"**Marketing**: Content plan {plan.get('status', 'unknown')}")

        # 4. Engineering scan
        eng = EngineeringAgent()
        scan = eng.daily_code_scan()
        results.append(f"**Engineering**: {len(scan.get('findings', []))} findings")

        # 5. Weekly report
        report = founder.generate_weekly_report()

        return report + "\n\n## Agent Results\n" + "\n".join(f"- {r}" for r in results)

    def _run_crewai(self) -> str:
        """Run agents via CrewAI orchestration."""
        try:
            from crewai import Agent, Task, Crew, Process  # type: ignore[import]
            from ..agent.world_model import get_world_model

            context = get_world_model().get_context_for_agent("Crew")

            # Define agents
            founder_agent = Agent(
                role="Founder & CEO",
                goal="Set strategic objectives and synthesize team outputs into actionable decisions",
                backstory="Serial entrepreneur, data-driven, kills experiments ruthlessly if not meeting kill signals",
                verbose=False,
                allow_delegation=True,
            )

            cs_agent = Agent(
                role="Customer Success Manager",
                goal="Maximize customer retention and NPS by resolving issues proactively",
                backstory="Ex-enterprise CS lead, specializes in churn prevention and expansion revenue",
                verbose=False,
            )

            mkt_agent = Agent(
                role="Growth Marketer",
                goal="Generate qualified leads through content and community engagement",
                backstory="Ex-B2B SaaS marketer, SEO-first approach, measures everything",
                verbose=False,
            )

            eng_agent = Agent(
                role="Lead Engineer",
                goal="Ship reliable features and maintain code quality",
                backstory="Senior engineer, TDD advocate, ships fast without breaking things",
                verbose=False,
            )

            # Define tasks
            strategy_task = Task(
                description=f"Review business context and set 3 weekly priorities per domain:\n{context}",
                agent=founder_agent,
                expected_output="3 priorities per domain with kill signals",
            )

            cs_task = Task(
                description="Scan for churn risks and prioritize customer outreach",
                agent=cs_agent,
                expected_output="List of at-risk customers and recommended actions",
            )

            mkt_task = Task(
                description="Generate content plan for the week",
                agent=mkt_agent,
                expected_output="5-piece content calendar with topics and keywords",
            )

            eng_task = Task(
                description="Review open PRs and flag any code quality issues",
                agent=eng_agent,
                expected_output="Code quality summary and priority fixes",
            )

            report_task = Task(
                description="Synthesize all team outputs into weekly founder report",
                agent=founder_agent,
                expected_output="Structured weekly report with metrics, priorities, and kill signals",
            )

            crew = Crew(
                agents=[founder_agent, cs_agent, mkt_agent, eng_agent],
                tasks=[strategy_task, cs_task, mkt_task, eng_task, report_task],
                process=Process.sequential,
                verbose=False,
            )

            result = crew.kickoff()
            return str(result)

        except Exception as exc:
            logger.warning("CrewAI execution failed, falling back to direct: %s", exc)
            return self._run_direct_agents()


_crew: SoloOSCrew | None = None


def get_crew() -> SoloOSCrew:
    global _crew
    if _crew is None:
        _crew = SoloOSCrew()
    return _crew
