"""Compatibility bridge from Django to FlowFoundry's existing Python domain layer.

The retained backend was originally executed with ``backend/`` as its import root.
Until those packages are fully normalized, this module adds that directory to the
Python module search path and keeps all Django/domain wiring in one place.
"""

from __future__ import annotations

import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from application.begin_workflow import BeginWorkflow
from application.select_agent import SelectAgent
from application.set_wfg import SetWFG
from application.start_session import StartSession
from application.update_actions import UpdateActions
from application.update_prompt import UpdatePrompt
from domain.entities.agent import Agent
from domain.entities.session import Session
from domain.entities.workflow import WorkflowPlan, WorkflowStatus, WorkflowStep, WorkflowType
from infrastructure.repositories.memory_agent_repository import MemoryAgentRepository
from infrastructure.repositories.memory_session_repository import MemorySessionRepository


PORTRAITS = {
    "athena": "Athena.png",
    "hermes": "Hermes.png",
    "themis": "Themis.png",
    "minerva": "Minerva.png",
    "apolo": "Apolo.png",
}

LOCAL_STEPS = (
    ("athena", "Review the request, identify ambiguities, and confirm testable acceptance criteria."),
    ("themis", "Draft test coverage from Athena's reviewed requirements and findings."),
    ("hermes", "Consolidate the specialist outputs into a clear Master Document."),
)


class LocalSimulationForgeMaster:
    """Deterministic ForgeMaster adapter used while live providers are disabled."""

    def triage(self, session: Session, available_agents: list[Agent]) -> WorkflowPlan:
        available_ids = {agent.id for agent in available_agents if agent.is_available()}
        steps = [
            WorkflowStep(agent_id=agent_id, description=description)
            for agent_id, description in LOCAL_STEPS
            if agent_id in available_ids
        ]
        return WorkflowPlan(
            session_id=session.id,
            workflow_type=WorkflowType.CHAINED,
            status=WorkflowStatus.READY,
            steps=steps,
            forgemaster_summary=(
                "Local simulation plan ready: Athena will review the request, "
                "Themis will create test coverage, and Hermes will assemble the Master Document."
            ),
        )


class DjangoDomainGateway:
    """In-process adapter that lets Django use the existing application use cases."""

    def __init__(self) -> None:
        self.sessions = MemorySessionRepository()
        self.agents = MemoryAgentRepository()
        self.forge_master = LocalSimulationForgeMaster()

    def agent_cards(self) -> list[dict]:
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "status": agent.status.value,
                "portrait": PORTRAITS.get(agent.id),
                "description": agent.description,
            }
            for agent in self.agents.get_all()
        ]

    def prepare_workflow(
        self,
        *,
        objective: str,
        actions: list[str],
        preferred_agent: str | None,
        wfg_active: bool,
    ) -> dict:
        normalized_objective = objective.strip()
        if not normalized_objective:
            return {
                "status": "clarification",
                "question": (
                    "Your request is empty — I need you to describe what outcome you are looking for "
                    "so I can identify the right specialists and build a workflow."
                ),
            }

        session = StartSession(self.sessions).execute()
        UpdatePrompt(self.sessions).execute(session.id, normalized_objective)
        UpdateActions(self.sessions).execute(session.id, actions)
        SelectAgent(self.sessions, self.agents).execute(session.id, preferred_agent)
        SetWFG(self.sessions).execute(session.id, wfg_active)
        plan = BeginWorkflow(self.sessions, self.agents, self.forge_master).execute(session.id)
        saved_session = self.sessions.get_by_id(session.id)

        agent_names = {agent.id: agent.name for agent in self.agents.get_all()}
        return {
            "status": "ready",
            "session_id": session.id,
            "summary": plan.forgemaster_summary,
            "steps": [
                {
                    "agent_id": step.agent_id,
                    "agent_name": agent_names.get(step.agent_id, "ForgeMaster"),
                    "description": step.description,
                }
                for step in plan.steps
            ],
            "actions": [action.label for action in saved_session.selected_actions],
            "preferred_agent": saved_session.selected_agent_id,
            "wfg_active": saved_session.wfg.active,
            "workflow_type": plan.workflow_type.value,
            "test_classification": "Local Django simulation — no real Agent or external API execution.",
        }


domain_gateway = DjangoDomainGateway()
