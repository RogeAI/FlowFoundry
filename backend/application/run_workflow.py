from dataclasses import dataclass

from application.begin_workflow import BeginWorkflow
from application.build_agent_task import BuildAgentTask
from application.dispatch_specialist import DispatchOutcome, DispatchSpecialist
from domain.entities.workflow import WorkflowPlan
from domain.repositories.session_repository import SessionRepository


@dataclass(frozen=True)
class WorkflowRun:
    plan: WorkflowPlan
    dispatch: DispatchOutcome | None = None


class RunWorkflow:
    """Begin under ForgeMaster and dispatch the first dependency-free specialist step."""

    def __init__(
        self,
        begin_workflow: BeginWorkflow,
        session_repo: SessionRepository,
        task_builder: BuildAgentTask,
        dispatcher: DispatchSpecialist,
    ) -> None:
        self._begin = begin_workflow
        self._sessions = session_repo
        self._task_builder = task_builder
        self._dispatcher = dispatcher

    def execute(self, session_id: str) -> WorkflowRun:
        plan = self._begin.execute(session_id)
        if plan.clarification_needed:
            return WorkflowRun(plan=plan)

        step = next(
            (item for item in plan.steps if item.agent_id and not item.depends_on),
            None,
        )
        if step is None:
            return WorkflowRun(plan=plan)

        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        task = self._task_builder.execute(session, plan, step)
        return WorkflowRun(plan=plan, dispatch=self._dispatcher.execute(task))

