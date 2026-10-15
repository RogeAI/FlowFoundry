# Claude Code and VS Code Continuation Guide

**Version:** 4.00  
**Baseline date:** 20 August 2026  
**Purpose:** Reproduce and continue the exact current FlowFoundry first-page prototype

---

## 1. What This Package Provides

The source package contains the application code, dependency lockfile, final image assets, tests, configuration, and complete decision documentation required to run the same FlowFoundry first page in VS Code and continue development with Claude Code.

This is not a screenshot recreation. The archive contains the runnable source that produced the current hosted page.

---

## 2. Extraction and Opening in VS Code

1. Extract the complete handover ZIP.
2. Open the extracted `flowfoundry-site` folder in VS Code. Do not open only its parent delivery folder.
3. Confirm that `package.json`, `pnpm-lock.yaml`, `app/`, `public/`, `docs/`, and `CLAUDE.md` are visible at the workspace root.
4. Open a VS Code terminal in that folder.
5. Run the installation and startup commands below.

---

## 3. Required Local Tools

| Tool | Required version |
|---|---|
| Node.js | `22.13.0` or newer |
| pnpm | `11.19.0` |
| VS Code | Current supported release |
| Claude Code | Current supported release |

If pnpm is not available but Node includes Corepack:

```bash
corepack enable
corepack prepare pnpm@11.19.0 --activate
```

---

## 4. Exact Installation and Startup

```bash
pnpm install --frozen-lockfile
pnpm dev
```

Open `http://localhost:3000`. If port 3000 is occupied, use the exact URL printed in the terminal.

---

## 5. First Claude Code Instruction

Paste this message into Claude Code after opening the repository:

```text
This is the authoritative FlowFoundry first-page repository. Before changing anything, read CLAUDE.md and then every document linked from its Read First section. Inspect app/page.tsx, app/globals.css, app/layout.tsx, package.json, and the final assets in public/. Run the current build and tests to establish a clean baseline. Preserve all locked FlowFoundry and ForgeMaster decisions, the modern logo proportions, current UI behavior, and the distinction between implemented prototype features and future backlog. Do not implement backlog items or alter product logic until I give a specific request.
```

---

## 6. Exact Current User-Visible Behavior

### 6.1 Prompt and Composer

- The user can type a natural-language outcome.
- **Expand** enlarges the prompt and temporarily hides the action selector.
- **Reduce** restores the side-by-side layout.
- Selected actions and Agent preference remain retained while the prompt is expanded.
- **Attach context** opens a multi-file picker and shows removable filename chips on the intake page. The root workflow-file provider carries actual File objects and backend source IDs into `/session`; later selections join the same collection and upload to the same backend session. On the working-session page, **Workflow Files** is the only filename display, while the right ForgeMaster panel retains the attachment action without duplicating the collection. Client state is still cleared by refresh and backend metadata is in-memory only.

### 6.2 Actions

- Six sample actions are available and any number may be selected.
- Available and selected counts are displayed separately.
- Selected actions receive a violet state and appear as removable chips below the prompt.
- Removing a chip deselects the corresponding action.
- The action panel can be resized vertically from its native bottom-right resize handle on desktop.
- Action selection order never represents execution order.

### 6.3 WFG and GO

- WFG toggles an explicit execution hold.
- Active WFG shows **WFG active · waiting for GO**.
- The primary button changes from **Begin workflow** to **GO**.
- Pressing GO turns WFG off automatically.
- Submission synchronizes the complete request with the Python backend. GO releases WFG during ForgeMaster triage, and a successful initial specialist result can be opened in `/session`.

### 6.4 Agent Cards

- Available Agents may be selected as a preference.
- Only one preferred Agent may be selected at a time.
- Selecting another Available Agent replaces the previous preference.
- Clicking the filled **✓ Selected** button unselects the Agent.
- The selected card receives a lavender background, violet border, and left indicator.
- Busy and Unavailable Agents cannot be selected.
- The preferred Agent appears beneath the prompt and can also be removed there.

### 6.5 Reset

- Reset asks for browser confirmation.
- Confirmation clears the prompt, actions, preferred Agent, WFG, and expanded composer state.
- Cancellation preserves everything.

---

## 7. Exact Logo Requirement

The final logo is `public/flowfoundry-logo-modern-v1.png`.

- Native dimensions: `2095 × 677`.
- Native aspect ratio: `2095:677`.
- Transparent PNG.
- Purple `FLOW`, navy `FOUNDRY`, converging purple/navy paths, and a restrained copper coordination point.
- No tagline, coin, anvil, metal plate, or dark rectangle.
- Rendered at a maximum width of 220 pixels while preserving its native ratio.
- Never use `object-fit: cover` for this asset.

---

## 8. Source Ownership Map

| File | Responsibility |
|---|---|
| `app/page.tsx` | Visible content, sample data, and client-side interaction logic |
| `app/globals.css` | Layout, typography, colours, states, responsive rules, and logo sizing |
| `app/layout.tsx` | Metadata, fonts, favicon, and social-card metadata |
| `public/flowfoundry-logo-modern-v1.png` | Approved application logo |
| `public/agent-portraits.png` | Six-image Agent portrait sprite |
| `public/og.png` | Social-sharing artwork |
| `tests/rendered-html.test.mjs` | Baseline smoke-test assertions |
| `docs/` | Product, UX, design, technical, and acceptance authority |

---

## 9. Validation Before and After Changes

```bash
pnpm run build
pnpm test
pnpm run lint
```

Visual changes should additionally be inspected at 1440 × 900, a 1920-pixel-wide desktop, 768 × 1024, and 390 × 844. Structural success is not visual proof.

---

## 10. Common Mistakes to Avoid

- Opening the parent delivery folder instead of `flowfoundry-site`.
- Running commands outside the directory containing `package.json`.
- Ignoring `pnpm-lock.yaml` and receiving different dependency versions.
- Replacing the final logo with retired artwork preserved for historical context.
- Treating Attach context, History, Saved, or Begin workflow as completed backend features.
- Allowing direct Agent selection to bypass ForgeMaster.
- Changing WFG into ordinary prompt text.
- Making action-selection order imply workflow order.
- Turning the enterprise application into a marketing landing page.
- Shrinking descriptive text until it is difficult to read at 100% zoom.

---

## 11. Next Major Phase

The recommended next phase is the working-session screen. Resolve the relevant questions in `08-BACKLOG-AND-OPEN-QUESTIONS.md` before coding it, then preserve the current first page as the entry experience.
