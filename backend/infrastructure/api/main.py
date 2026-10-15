import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.dispatch_specialist import DispatchSpecialist
from domain.services.forge_master import ForgeMasterService
from infrastructure.api.routers import agents, sessions, workflows
from infrastructure.repositories.memory_agent_repository import MemoryAgentRepository
from infrastructure.repositories.memory_session_repository import MemorySessionRepository
from infrastructure.repositories.local_source_repository import LocalSourceRepository
from infrastructure.runtime_registry import MemorySpecialistRuntimeRegistry

app = FastAPI(title="FlowFoundry API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wire dependencies onto app state (simple DI for in-memory dev)
app.state.agent_repo = MemoryAgentRepository()
app.state.session_repo = MemorySessionRepository()
default_source_root = Path(__file__).resolve().parents[3] / ".flowfoundry" / "runtime" / "sources"
app.state.source_storage_root = Path(
    os.environ.get("FLOWFOUNDRY_SOURCE_ROOT", str(default_source_root))
).resolve()
app.state.source_repo = LocalSourceRepository(app.state.source_storage_root)
app.state.forge_master = ForgeMasterService()
app.state.runtime_registry = MemorySpecialistRuntimeRegistry()
app.state.specialist_dispatcher = DispatchSpecialist(
    app.state.agent_repo,
    app.state.runtime_registry,
)

app.include_router(agents.router)
app.include_router(sessions.router)
app.include_router(workflows.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "FlowFoundry API"}
