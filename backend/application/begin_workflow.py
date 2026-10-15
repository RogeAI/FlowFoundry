from typing import Protocol

from domain.entities.agent import Agent
from domain.entities.workflow import WorkflowPlan
from domain.repositories.agent_repository import AgentRepository
from domain.repositories.session_repository import SessionRepository


class ForgeMaster(Protocol):
    def triage(self, session, available_agents: list[Agent]) -> WorkflowPlan: ...


class BeginWorkflow:
    def __init__(
        self,
        session_repo: SessionRepository,
        agent_repo: AgentRepository,
        forge_master: ForgeMaster,
    ) -> None:
        self._sessions = session_repo
        self._agents = agent_repo
        self._forge_master = forge_master

    def execute(self, session_id: str) -> WorkflowPlan:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Locked domain rule: GO automatically turns WFG off
        if session.wfg.active:
            session.release_wfg()
            self._sessions.save(session)

        available_agents = self._agents.get_all()

        # ForgeMaster always triages — even when user pre-selected an agent
        plan = self._forge_master.triage(session, available_agents)

        # Record in session history (one entry per objective)
        session.history.append({
            "workflow_plan_id": plan.id,
            "workflow_type": plan.workflow_type,
            "summary": plan.forgemaster_summary,
            "prompt": session.prompt,
        })
        self._sessions.save(session)

        return plan
