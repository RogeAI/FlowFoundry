# FlowFoundry Claude Code Instructions

This repository is the authoritative, runnable FlowFoundry first-page baseline. Preserve the existing application before extending it.

---

## 1. Read First

Read these documents in order before changing code:

1. `PRODUCT-OVERVIEW.md`
2. `docs/LOCAL-DEVELOPMENT-AND-TESTING.md`
3. `docs/00-HANDOVER-INDEX.md`
4. `docs/01-PRODUCT-ARCHITECTURE.md`
5. `docs/02-UX-INTERACTION-SPECIFICATION.md`
6. `docs/03-DESIGN-SYSTEM-AND-CONTENT.md`
7. `docs/04-TECHNICAL-HANDOVER.md`
8. `docs/09-CLAUDE-CODE-CONTINUATION.md`
9. `docs/10-EXACT-BASELINE-INVENTORY.md`

Treat locked product decisions as requirements. Treat backlog items as proposals, not authorization to implement them.

---

## 2. Preserve the Current Baseline

- Application name: **FlowFoundry**.
- Supervisory orchestrator: **ForgeMaster**.
- ForgeMaster performs initial triage and remains continuously supervising.
- Direct Agent selection never bypasses ForgeMaster.
- WFG means **Wait for GO** and prevents execution until GO.
- GO automatically turns WFG off.
- History represents one user objective/session, with Agent execution nested inside it.
- Actions are multi-select; selection order is not execution order.
- Busy and Unavailable Agents are visible but cannot be selected.
- Only one preferred Agent may be selected, and clicking **Selected** unselects it.

Do not rename the product, supervisor, Agents, or current interface language without explicit approval.

---

## 3. Visual Baseline

The page is an enterprise workspace, not a marketing landing page. Preserve:

- the final transparent modern logo at `public/flowfoundry-logo-modern-v1.png`;
- the logo's natural `2095:677` aspect ratio without cropping or stretching;
- the light lavender/white workspace, violet primary actions, deep-navy typography, and restrained copper accent;
- the 240-pixel desktop header/sidebar grid alignment;
- portrait-led specialist cards using `public/agent-portraits.png`;
- clear selected, Busy, Unavailable, WFG, and operational states;
- comfortable readability at 100% browser zoom.

Do not restore the retired coin, metal-plate header logo, dark-green navigation header, or tiny typography.

---

## 4. Current Functional Boundaries

This is a two-page application with an optional local Python backend. When that backend is running and configured, the first page creates a session, uploads validated workflow sources, sends the objective/actions/preferred Agent/WFG state to ForgeMaster, and carries the initial specialist result into `/session`. Later working-session conversation, pause/resume, multi-step continuation, durable persistence, authentication, scanning, and History routes remain prototype behavior. Do not claim those production capabilities exist.

Current functional UI behavior lives in `app/page.tsx`. Current visual behavior lives in `app/globals.css`.

---

## 5. Run and Validate

Until the real external API and its credentials are available, run FlowFoundry locally and follow the test classification in `docs/LOCAL-DEVELOPMENT-AND-TESTING.md`. A successful localhost browser flow, mock, stub, or local backend check is **not** a live end-to-end integration test.

Use Node.js `>=22.13.0` and pnpm `11.19.0`.

```bash
pnpm install --frozen-lockfile
pnpm dev
```

Open `http://localhost:3000`.

Before handing back any change, run:

```bash
pnpm run build
pnpm test
pnpm run lint
```

Do not commit `node_modules`, `dist`, `.vinext`, `.wrangler`, environment files, credentials, or temporary archives.

---

## 6. Change Discipline

When requirements are ambiguous, ask before changing locked behavior or visual identity. Make focused changes, preserve working interactions, and update the corresponding documentation and acceptance criteria whenever behavior changes.
