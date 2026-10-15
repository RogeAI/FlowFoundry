# Local Development and Testing Before the Live API

## Current Rule

Until the real external API, approved credentials, and target environment are available, FlowFoundry is developed and exercised locally. The current Django application runs at `http://localhost:3001`.

Local execution can validate the interface, navigation, client-side behavior, request construction, validation, and local frontend-to-backend wiring. It does **not** prove that FlowFoundry integrates successfully with the real external API or production services.

## How to Run Locally

### Current Django application

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:3001
```

Open `http://localhost:3001`.

Use this mode for the About page, Workspace, Working Session, WFG/GO, clarification, local plan preparation, and supervised session simulation. Django calls the existing Python domain/application layer in-process for Agent Registry data, session preparation, and WFG release. The UI identifies this mode as a local Django simulation because no real Agent or external provider is invoked.

Run the current checks with:

```bash
python manage.py check
python manage.py test web
cd backend
python -m pytest tests -q
```

### Retained legacy React implementation

The React/vinext files remain as migration inputs. If they must be reproduced for comparison, use `pnpm install --frozen-lockfile` and `pnpm dev`, then open `http://localhost:3000`.

### Retained FastAPI/domain backend

In the backend terminal:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn infrastructure.api.main:app --reload --port 8000
```

In a second terminal, from the repository root:

```bash
pnpm install --frozen-lockfile
pnpm dev
```

Open `http://localhost:3000`.

Starting the local backend does not by itself make a test live. If an external provider call requires an unavailable API or credential, keep that path disabled, mocked, or explicitly recorded as blocked.

## Required Test Labels

Use precise language in test notes, commits, and handovers:

- **Local UI test:** browser behavior at localhost with no real external service.
- **Mock/stub test:** an external response is simulated.
- **Local integration test:** two or more local components communicate, such as the frontend on port 3000 and the Python backend on port 8000.
- **Live integration test:** the application communicates with the real approved external API in an approved environment using valid credentials.
- **End-to-end test:** the complete intended workflow crosses every real required component and verifies the final outcome.

Do not describe a localhost-only, mock/stub, or local-backend result as a live integration test or production validation.

## Before Claiming Live Integration

Confirm all of the following:

1. The real API endpoint and approved environment are known.
2. Valid credentials are available through an approved secret-management method and are not committed to Git.
3. Mock and stub modes are disabled for the tested path.
4. The request reaches the real service and its response is verified.
5. Expected success and failure behavior are recorded.
6. Logs and evidence contain no exposed secrets or confidential data.

Until every applicable condition is met, report the result as local or blocked—not live.
