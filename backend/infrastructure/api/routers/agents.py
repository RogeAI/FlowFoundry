from fastapi import APIRouter, Request

from infrastructure.api.schemas.agent import AgentResponse

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=list[AgentResponse])
def list_agents(request: Request) -> list[AgentResponse]:
    agent_repo = request.app.state.agent_repo
    agents = agent_repo.get_all()
    return [
        AgentResponse(
            id=a.id,
            name=a.name,
            role=a.role,
            description=a.description,
            status=a.status.value,
            portrait_index=a.portrait_index,
        )
        for a in agents
    ]
