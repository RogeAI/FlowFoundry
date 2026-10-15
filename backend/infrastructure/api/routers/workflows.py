from fastapi import APIRouter, HTTPException, Request

from application.begin_workflow import BeginWorkflow
from application.build_agent_task import BuildAgentTask
from application.run_workflow import RunWorkflow
from infrastructure.api.schemas.session import WorkflowPlanResponse, WorkflowStepResponse

router = APIRouter(prefix="/api/sessions", tags=["workflows"])


@router.post("/{session_id}/begin", response_model=WorkflowPlanResponse)
def begin_workflow(session_id: str, request: Request) -> WorkflowPlanResponse:
    try:
        begin = BeginWorkflow(
            request.app.state.session_repo,
            request.app.state.agent_repo,
            request.app.state.forge_master,
        )
        run = RunWorkflow(
            begin,
            request.app.state.session_repo,
            BuildAgentTask(request.app.state.agent_repo, request.app.state.source_repo),
            request.app.state.specialist_dispatcher,
        ).execute(session_id)
        plan = run.plan
        result = run.dispatch.result if run.dispatch else None
        error = run.dispatch.error if run.dispatch else None
        return WorkflowPlanResponse(
            id=plan.id,
            session_id=plan.session_id,
            workflow_type=plan.workflow_type.value,
            status=plan.status.value,
            steps=[
                WorkflowStepResponse(
                    agent_id=s.agent_id,
                    description=s.description,
                    depends_on=s.depends_on,
                )
                for s in plan.steps
            ],
            forgemaster_summary=plan.forgemaster_summary,
            clarification_needed=plan.clarification_needed,
            clarification_question=plan.clarification_question,
            specialist_result=result.model_dump(mode="json") if result else None,
            specialist_error=error.model_dump(mode="json") if error else None,
        )
    except ValueError as exc:
        status_code = 404 if "not found" in str(exc).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
