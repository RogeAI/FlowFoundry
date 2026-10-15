from pydantic import BaseModel


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    status: str
    portrait_index: int
