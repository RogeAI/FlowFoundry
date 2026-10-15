# FlowFoundry Technical Handover

**Version:** 5.01
**Implementation:** Three-page Django application connected in-process to the existing Python domain and application layers
**Runtime:** Python 3.12, Django 5.2 LTS, server-rendered templates, CSS, and focused browser JavaScript

---

## 1. Current Technical Status

The current application entry point is Django. It contains the About experience, workflow intake page, and supervised Working Session at `/`, `/workspace/`, and `/session/`. Django now calls the existing FlowFoundry domain entities, application use cases, Agent Registry, and in-memory repositories directly through `web/domain_gateway.py`. The browser layer manages presentation state, controls, and the minimum 3.5-second ForgeMaster state visibility.

The experience is explicitly a local simulation. It does not invoke real Agents or an external model API. The existing `backend/domain/`, `backend/application/`, and in-memory repository code is now part of the Django request path. The FastAPI transport and React/vinext files remain available as migration/reference material but are not required by the current Django runtime. Live provider integration and durable persistence remain future work.

---

## 2. Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 with focused browser JavaScript |
| UI | Django 5.2 server-rendered templates |
| App conventions | Django project `flowfoundry` and app `web` |
| Styling | Application-owned CSS under `static/flowfoundry/css/` |
| Local runtime | Django development server on port `3001` |
| Local state | Existing in-memory domain repositories; SQLite foundation remains unused for workflows |
| Retained migration inputs | React 19, vinext, Vite, and the optional FastAPI transport |

Python dependencies are frozen in the root `requirements.txt`. Node.js is only required when inspecting or reproducing the retained legacy React implementation.

---

## 3. Important Files

| Path | Responsibility |
|---|---|
| `manage.py` | Django management entry point |
| `flowfoundry/` | Django configuration, URLs, WSGI, and ASGI entry points |
| `web/views.py` | About, Workspace, Working Session, and JSON endpoint views |
| `web/services.py` | Django-facing workflow and local session services |
| `web/domain_gateway.py` | In-process bridge to existing domain use cases, Agent Registry, and repositories |
| `backend/domain/` | Shared FlowFoundry entities, value objects, and orchestration rules |
| `backend/application/` | Shared workflow application use cases called by Django |
| `templates/web/` | Server-rendered About, Workspace, and Working Session templates |
| `static/flowfoundry/css/site.css` | Current responsive visual system and component states |
| `static/flowfoundry/js/` | Focused browser interaction and timed presentation controls |
| `app/page.tsx` | Retained React migration input for the former first page |
| `app/session/page.tsx` | Retained React migration input for the former Working Session |
| `app/globals.css` | Retained React styling reference |
| `app/layout.tsx` | Retained React root layout reference |
| `public/flowfoundry-logo-modern-v1.png` | Final transparent application logo, `2095 × 677` |
| `public/agent-portraits.png` | Six-portrait sprite used by the Specialist Agent cards |
| `public/og.png` | Social-sharing artwork |
| `public/favicon.svg` | Current browser icon |
| `vite.config.ts` | Retained vinext/Cloudflare configuration |
| `worker/index.ts` | Retained Worker entry surface |
| `db/` and `drizzle/` | Retained starter persistence foundation |
| `tests/rendered-html.test.mjs` | Retained React build-output smoke tests |
| `docs/` | Product, UX, design, technical, test, history, and delivery handover |

---

## 4. Current State Model

The current Django templates render the initial application state. `static/flowfoundry/js/workspace.js` and `session.js` hold browser-local presentation state; Python owns the plan definitions and response payloads.

| State | Meaning |
|---|---|
| `prompt` | Current outcome text |
| `selectedActions` | Multi-selected action labels |
| `selectedAgent` | One preferred Agent name or null |
| `wfg` | Whether execution is being held |
| `expanded` | Whether the composer occupies the full panel width |
| `attachedFiles` | Browser-local selected File objects; no durable upload occurs in the current simulation |

Browser presentation state is not persisted. Each prepared plan creates an in-process domain session, which is lost when the Django process restarts and is not yet exposed as durable History.

---

## 5. Implemented Interactions

- Multi-select action toggling.
- Selected-action count.
- Removable selected-action chips.
- Single preferred Agent selection.
- Toggle-based Agent unselection from the selected card.
- Removal of the preferred Agent.
- Disabled Busy and Unavailable Agents.
- WFG activation and visible state.
- GO automatically turning WFG off.
- Expand and Reduce composer behavior.
- Reset confirmation and full draft clearing.
- Responsive layout rules.
- Desktop vertical resizing of the action selector through native CSS resize behavior.
- Simulated working-session route with Running, Investigating, Paused, and Complete states.
- Agent-specific clarification: Athena remains complete while Hermes is marked Input Required.
- ForgeMaster attention panel opens for the user response, then resumes Hermes.
- Transparent ForgeMaster state images for running, investigating, and successful completion.
- Multi-file context selection on both pages, with visible removable filename chips.
- Python-owned local plan preparation and investigation-response payloads through Django endpoints.
- Django workflow preparation through the existing `StartSession`, `UpdatePrompt`, `UpdateActions`, `SelectAgent`, `SetWFG`, and `BeginWorkflow` use cases.
- Agent cards sourced from the Python-owned Agent Registry instead of a duplicate Django list.
- Backend-enforced GO release of WFG; the browser sends the held state and the domain releases it when beginning the workflow.
- Working Session pause/resume, three staged Agent states, investigation, response, resumption, and completion.
- Minimum 3.5-second visibility for timed ForgeMaster and workflow states.
- Browser-local Working Session attachments with visible removable filename rows.
- Explicit local-simulation labeling and honest handling when no downloadable artifact exists.

---

## 6. Prototype-Only Elements

The following controls are intentionally non-functional placeholders:

- Workspace navigation destinations other than the implemented Workspace and About routes;
- Activity, Agents, and Governance routes;
- search and help;
- user-menu behavior;
- History and Saved data;
- recent-session items;
- production-grade source persistence, malware scanning, authentication, and retention;
- real Agent execution and external model calls;
- generated downloadable Agent files and Master Documents;
- real Agent availability;
- durable workflow, chat, attachment, and history persistence.

These must not be represented as production-complete features.

---

## 7. Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:3001
```

The local application runs at `http://localhost:3001`.

---

## 8. Validation Commands

```bash
python manage.py check
python manage.py test web
node --check static/flowfoundry/js/workspace.js
node --check static/flowfoundry/js/session.js
cd backend
python -m pytest tests -q
```

These checks validate Django configuration, the nine current web tests, the retained backend/domain suite, and browser-script syntax. Browser walkthroughs remain required for visual layout and timed interaction verification.

---

## 9. Deployment Status

No production Django deployment is configured. The verified result is a local development application only. A deployment design must select a supported WSGI/ASGI server, database, static-file strategy, secret-management method, and approved hosting environment before any production claim.

---

## 10. Environment and Secrets

The frontend requires no secrets. Live backend triage and Hermes execution require server-side `ANTHROPIC_API_KEY` plus `HERMES_MODEL`. Do not commit secrets, credentials, access tokens, or local environment files.

If future orchestration uses server-side model calls, secrets should be managed by the deployment platform rather than embedded in client code.

---

## 11. Data and Persistence

The Django project includes a local SQLite foundation, but current workflow state is browser-local and the application does not persist workflow records. The retained Drizzle/D1 files are legacy migration inputs.

Before introducing persistence, define:

- session ownership;
- History schema;
- messages and attachments;
- workflow steps and Agent executions;
- audit events;
- status transitions;
- retention and deletion;
- tenant isolation;
- migrations and rollback.

---

## 12. Security and Privacy Considerations

Production implementation must address:

- authorization for sessions and attachments;
- tenant and user isolation;
- prompt and output retention;
- safe secret storage;
- tool permissions;
- audit logging;
- rate limiting;
- file scanning and content-type validation;
- safe display of model-generated content;
- privacy controls and deletion.

The private Site gate protects access to the prototype but is not a substitute for application-level authorization once user-specific records exist.

---

## 13. Recommended Implementation Boundaries

Future development should separate:

1. user interface and routes;
2. session and History services;
3. ForgeMaster orchestration service;
4. Agent registry and capability metadata;
5. execution queue and capacity service;
6. tool and provider adapters;
7. attachment service;
8. events, telemetry, and audit;
9. authorization and tenancy.

The current in-file sample Agent array should become registry-driven data when a real service exists.

---

## 14. Deployment Baseline

The application currently runs via localhost only. No external deployment is configured. When a hosting provider is chosen (e.g. Cloudflare Pages, Vercel), update this section with the deployment URL and any required configuration.
