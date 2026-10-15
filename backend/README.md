# FlowFoundry Backend

Python FastAPI backend with Domain-Driven Design (DDD).

## Structure

```
backend/
├── domain/           Pure Python domain layer — no frameworks
│   ├── entities/     Agent, Session, Workflow
│   ├── value_objects/Action, WFGState
│   ├── services/     ForgeMaster (Claude Opus 5)
│   ├── repositories/ Abstract interfaces
│   └── events/       Domain events
├── application/      Use cases (thin orchestration)
└── infrastructure/   FastAPI app, in-memory repos, Pydantic schemas
```

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file (never commit this):

```
ANTHROPIC_API_KEY=your-key-here
HERMES_MODEL=your-approved-model-id
```

## Run

Run from inside the `backend/` directory so that absolute imports resolve correctly:

```bash
cd backend
uvicorn infrastructure.api.main:app --reload --port 8000
```

API docs available at http://localhost:8000/docs

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/agents` | List all Agents |
| POST | `/api/sessions` | Create session |
| GET | `/api/sessions/{id}` | Get session state |
| PATCH | `/api/sessions/{id}/prompt` | Set the workflow objective |
| PATCH | `/api/sessions/{id}/wfg` | Toggle WFG |
| PATCH | `/api/sessions/{id}/agent` | Select or deselect preferred Agent |
| PATCH | `/api/sessions/{id}/actions` | Update selected actions |
| POST | `/api/sessions/{id}/sources` | Attach one validated session source |
| GET | `/api/sessions/{id}/sources` | List safe source metadata |
| DELETE | `/api/sessions/{id}/sources/{source_id}` | Remove one source from that session |
| POST | `/api/sessions/{id}/begin` | Run ForgeMaster triage and dispatch an eligible specialist step |
| DELETE | `/api/sessions/{id}` | Reset session and remove its sources |

The Python backend owns the operational Agent Registry. Hermes is the first specialist with a contract-backed `AgentManifest`, defined in `backend/agents/hermes.py` and validated against Agent Contract v1.00. The public `/api/agents` response remains a safe projection and does not expose private instructions, permissions, or internal capability configuration.

Hermes runtime execution is implemented in `backend/agents/hermes_runtime.py`. The adapter validates assignment identity and capability activation, checks scoped read permissions and source hashes, extracts authorized text/DOCX content, loads persistent Hermes governance plus only the selected skills, invokes a dependency-injected model gateway, and returns a contract-valid `AgentResult`.

The Anthropic implementation of that model boundary is `backend/infrastructure/model_gateways/anthropic_hermes.py`. It requires both `ANTHROPIC_API_KEY` and `HERMES_MODEL`, keeps source material inside an explicitly untrusted user-data payload, accepts only a schema-valid JSON result, and converts provider or parsing failures into safe runtime errors.

ForgeMaster-controlled specialist dispatch is implemented in `backend/application/dispatch_specialist.py`, with runtime registration in `backend/infrastructure/runtime_registry.py`. Hermes is created lazily so backend startup and non-Hermes workflows do not require live provider credentials. The dispatcher checks Agent registration, availability, contract and Agent versions, runtime registration, and returned result identity; failures are converted into safe structured `AgentError` values. No direct user-to-specialist execution route is exposed.

Session-scoped source ingestion is implemented in `backend/application/attach_source.py`. Supported text formats and DOCX files are size-limited, copied beneath a server-controlled per-session runtime directory, assigned a SHA-256 identity, and exposed to a specialist only through an explicit read grant. `BuildAgentTask` converts a released ForgeMaster plan into Agent contract v1.00, and `RunWorkflow` dispatches only the first dependency-free specialist step. Reset removes only that session's source directory. The browser intake and working-session file controls are connected to these endpoints; later multi-step execution and conversation remain future work.
