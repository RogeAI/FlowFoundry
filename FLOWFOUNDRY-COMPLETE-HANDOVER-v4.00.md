# FlowFoundry Complete Handover

**Handover version:** 4.00  
**Baseline date:** 20 August 2026  
**Application version:** 0.1.0 first-page prototype  
**Live reference:** localhost only (no external deployment configured)  
**Intended continuation environment:** VS Code with Claude Code

---

## 1. Purpose of This Handover

This package transfers the exact runnable FlowFoundry first-page source, its approved architecture and UX decisions, final visual assets, current interaction logic, test baseline, and future-work boundaries.

The package is designed so that a developer or Claude Code can extract the repository, install the locked dependencies, run it locally, and see the same website and functions represented by the current baseline.

This is a functional front-page prototype. It is not yet the complete Agent-execution platform.

---

## 2. Product Identity

| Item | Locked value |
|---|---|
| Application | FlowFoundry |
| Supervisory orchestrator | ForgeMaster |
| Brand line | Forge the right flow. |
| Application-header logo | Modern convergence wordmark without tagline |
| Primary experience | Enterprise Agent-orchestration workspace |

The former AI Agent Hub, Orc, Orchestrator, Maestro, Orchestrum, and AgentForge names are historical only.

---

## 3. Core Architecture

ForgeMaster is the persistent control plane. It receives every request logically first, performs initial triage, decides whether it can handle the request alone or should involve specialists, supervises all selected Agents, receives escalations, and replans when necessary.

```text
User
  │
  ▼
ForgeMaster
  ├── Clarify
  ├── Handle alone
  ├── Assign one Agent
  ├── Build an ordered chain
  └── Form parallel or mixed Agent work
```

Direct selection does not bypass ForgeMaster:

```text
User selects Agent
        │
        ▼
ForgeMaster validates and supervises
        │
        ▼
Selected Agent works
```

Agents escalate to ForgeMaster rather than independently creating uncontrolled peer chains.

---

## 4. Workflow Types

FlowFoundry is intended to support:

1. ForgeMaster-only work.
2. One supervised specialist Agent.
3. Sequential Agent chains.
4. Parallel Agent work.
5. Mixed sequential and parallel workflows.

The current prototype visualizes the entry point only. No real workflow is executed yet.

---

## 5. WFG and GO

WFG means **Wait for GO**. It is a real execution hold.

While WFG is active, the user may continue entering context and making selections, but ForgeMaster and specialists must not execute the request. The UI displays a waiting state and changes the submission control to **GO**.

Pressing GO releases the complete held request and automatically deactivates WFG. The current prototype demonstrates the state transition but does not yet start backend work or navigate to the working-session page.

---

## 6. Current First-Page Structure

The implemented page contains:

1. Modern FlowFoundry logo and global navigation.
2. Desktop workspace sidebar with New workflow, Reset, Start, History, Saved, and recent-session examples.
3. Page introduction and four-step guidance.
4. ForgeMaster request composer.
5. Multi-select action catalogue.
6. WFG and Begin workflow/GO controls.
7. Six portrait-led Specialist Agent cards.
8. Availability, Busy, and Unavailable states.

Navigation destinations, search, help, user menu, attachments, real session data, and workflow execution remain placeholders.

---

## 7. Current Interaction Contract

### 7.1 Prompt

- The user can enter free text.
- Prompt Expand uses the full request-panel width and hides the action selector temporarily.
- Reduce restores the original side-by-side layout.
- State is retained during expansion.

### 7.2 Actions

- Six sample actions are available.
- Any number can be selected.
- Available and selected counts are displayed separately.
- Selected actions appear as removable chips.
- Selection order never becomes execution order.
- The desktop action panel is vertically resizable using its bottom-right handle.

### 7.3 Preferred Agent

- Only Available Agents can be selected.
- Only one Agent can be preferred at a time.
- Selecting another replaces the previous preference.
- Clicking **✓ Selected** unselects the Agent.
- Removing the preferred-Agent label beneath the prompt also unselects it.
- Busy and Unavailable Agents remain disabled.

### 7.4 Reset

Reset requires confirmation. Confirmation clears prompt text, selected actions, preferred Agent, WFG, and expanded-composer state.

---

## 8. History Model

History represents one user objective or session, regardless of how many Agents participate.

```text
History item: Review checkout requirements
  ├── ForgeMaster triage
  ├── Axiom analysis
  ├── Verity validation
  └── Atlas test design
```

The example is one History item, not separate Agent conversations.

---

## 9. Visual Baseline

The approved design is a light enterprise application with:

- pale lavender/grey canvas;
- white structured surfaces;
- deep-navy typography;
- violet primary actions, navigation, and selected states;
- restrained copper brand accent;
- compact uppercase section headings;
- subtle borders, shadows, and rounding;
- readable text at 100% browser zoom;
- portrait-led Agent cards.

The supplied external enterprise interface was a look-and-feel reference, not a structure to copy.

---

## 10. Final Logo Contract

The active header logo is:

```text
public/flowfoundry-logo-modern-v1.png
```

Requirements:

- native dimensions `2095 × 677`;
- transparent PNG;
- ratio `2095:677` preserved;
- converging paths on the left;
- small copper coordination point;
- purple `FLOW` and navy `FOUNDRY`;
- no tagline in the compact header;
- no coin, anvil, rustic plate, dark rectangle, or cropped illustration;
- no stretching or `object-fit: cover`.

Older logo assets are retained only as historical material and must not be restored accidentally.

---

## 11. Technology and Source

| Area | Baseline |
|---|---|
| Language | TypeScript |
| UI | React 19 |
| App layout | Next-compatible app directory |
| Build | vinext and Vite |
| Output | Cloudflare Worker-compatible ESM |
| Package manager | pnpm 11.19.0 |
| Minimum Node | 22.13.0 |
| Lockfile | `pnpm-lock.yaml` |

Primary implementation files:

- `app/page.tsx` — markup, sample data, and state behavior;
- `app/globals.css` — full styling, layout, states, and responsiveness;
- `app/layout.tsx` — metadata and root layout;
- `tests/rendered-html.test.mjs` — smoke tests;
- `public/` — final brand and Agent assets.

---

## 12. Exact Local Reproduction

Extract the ZIP and open the `flowfoundry-site` directory in VS Code.

```bash
pnpm install --frozen-lockfile
pnpm dev
```

Open `http://localhost:3000`, or the exact alternative URL printed by the server.

Validate:

```bash
pnpm run build
pnpm test
pnpm run lint
```

Use the complete source tree. Do not copy only `app/page.tsx` and `app/globals.css`, because the exact result also depends on the public image assets, layout metadata, package versions, and build configuration.

---

## 13. Claude Code Start Procedure

Claude Code automatically reads `CLAUDE.md`. The first explicit instruction should still be:

```text
Read CLAUDE.md and every document in its Read First list before changing anything. Establish the current baseline by running the build and tests. Preserve locked FlowFoundry and ForgeMaster decisions, the final logo proportions, and current first-page interactions. Do not implement backlog items until I provide a specific approved request.
```

---

## 14. Implemented Versus Future Capability

### Implemented now

- first-page rendering;
- prompt input state;
- multi-select action state and chips;
- prompt expansion;
- desktop action-panel resizing;
- WFG/GO state transition;
- Agent selection, replacement, and unselection;
- disabled Busy and Unavailable Agents;
- reset confirmation;
- responsive layout.

### Not implemented

- real AI or Agent execution;
- ForgeMaster backend;
- file uploads;
- session persistence;
- authentication-driven content;
- History or Saved routes;
- working-session screen;
- real availability or queue service;
- tool/provider integration;
- production mobile navigation.

---

## 15. Locked Decisions

1. Product name is FlowFoundry.
2. Supervisor name is ForgeMaster.
3. ForgeMaster performs triage first and remains supervising.
4. Direct Agent selection never bypasses ForgeMaster.
5. Agents escalate to ForgeMaster.
6. WFG holds execution until GO.
7. GO deactivates WFG automatically.
8. Actions are multi-select.
9. Selection order is not execution order.
10. One objective creates one History item.
11. Reset clears the entire current draft after confirmation.
12. Busy and Unavailable Agents cannot be selected.
13. Clicking the selected Agent unselects it.
14. The final modern convergence logo is the active application identity.
15. The current deliverable is the start experience, not the complete platform.

---

## 16. Recommended Next Work

The next major design topic is the working-session experience: ForgeMaster triage, participating Agents, sequence and parallelism, progress, escalation, user clarification, replanning, intermediate artifacts, and completion.

Review and decide those topics before implementation. Do not infer production behavior from the current sample UI.

---

## 17. Detailed Supporting Documents

The numbered files in `docs/` are part of this handover and remain authoritative for product architecture, interaction details, design, technical implementation, acceptance tests, history, deployment, backlog, Claude Code continuation, and the exact baseline inventory.
