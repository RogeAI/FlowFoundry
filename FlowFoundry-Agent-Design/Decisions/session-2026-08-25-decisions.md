# Session Decisions — 25 August 2026

This file records all decisions and agreements reached during the working session on 25 August 2026.
It is a living document — updated as decisions are made during the session.

---

## 1. Folder Structure Created

`FlowFoundry-Agent-Design/` was created as the authoritative design workspace for all FlowFoundry agent work.

```
FlowFoundry-Agent-Design/
  00-INDEX.md
  Foundation/
    Skills/        ← shared skills inherited by all agents
    Tools/         ← shared tools available to all agents
    Guardrails/    ← shared guardrails applied to all agents
  Agents/          ← individual agent profile documents
  Decisions/       ← backlog items and key decisions
```

---

## 2. Two-Layer Agent Design Approach Agreed

Agents will use a shared foundation plus individual profiles:

- **Layer 1 — Foundation (shared):** Skills, Tools, and Guardrails that every agent inherits automatically. Defined once in `Foundation/`.
- **Layer 2 — Individual profiles:** Each agent gets its own file in `Agents/` defining only what is unique to that agent.

---

## 3. Agent Catalogue — Finalized

| # | Name | Role | Status | Portrait |
|---|---|---|---|---|
| 1 | Athena | The Testing Mentor | Active | `public/Athena.png` |
| 2 | Hermes | The Summarizer | Active | `public/Hermes.png` |
| 3 | Themis | Test Cases Creator | Active | `public/Themis.png` |
| 4 | Minerva | Test Strategy Advisor | Active | `public/Minerva.png` |
| 5 | Agent 5 | TBD | Grayed out — Phase 2 | Placeholder "?" |
| 6 | Agent 6 | TBD | Grayed out — Phase 2 | Placeholder "?" |

**Card descriptions:**
- **Athena:** "Teaches you how to create test scenarios and manual test cases step by step. Covers requirements analysis, test approaches, coverage, and test data — aligned with ISTQB concepts."
- **Hermes:** "Transforms raw documents into clear, actionable insights. Surfaces risks, gaps, and contradictions — then classifies findings as Testable, Partially testable, or Not yet testable."
- **Themis:** "Designs high-quality test assets from requirements, user stories, and handoff materials. Produces clear scenarios, test data, and manual test cases with atomic steps and measurable expected results."
- **Minerva:** "Guides you through creating and finalizing your Test Strategy — what's being tested, what could go wrong, how testing builds confidence, and what dependencies apply."

Individual portrait images replaced the sprite sheet (`agent-portraits.png`). ForgeMaster icon updated to `public/ForgeMaster_Icon_4.png`.

---

## 4. Agent Registry Migration Deferred

Agent data currently lives hardcoded in `app/page.tsx`. The decision was made to migrate this to a registry-driven data source in the future — but not now.

Tracked in: `Decisions/checklist-agent-registry-migration.md`

---

## 5. ForgeMaster Interaction Model Agreed

The first page has three input areas forming one assembled request:
1. ForgeMaster section (natural language objective)
2. Select Actions / Extra Options (optional, multi-select)
3. Agents section (optional, one preferred agent only)

Three valid entry paths:
- **Option 1:** Objective only → Begin Workflow
- **Option 2:** Objective + Select Actions → Begin Workflow
- **Option 3:** Objective + Select Actions + preferred Agent → Begin Workflow

ForgeMaster always receives everything, validates, routes, supervises, and may decline if insufficient information is provided.

Full detail in: `Decisions/forgemaster-interaction-handover.md`

---

## 6. ForgeMaster Response Screen — New Screen Required

A critical gap was identified: **there is no second screen defined yet.**

After "Begin Workflow" is pressed, the first page cannot hold ForgeMaster's response. A new screen or state is needed.

ForgeMaster must surface one of two outcomes:

- **Outcome A — Ready to proceed:** Plan created, Agent(s) selected, user sees the plan and can approve or adjust.
- **Outcome B — Needs more information:** Request incomplete or ambiguous, ForgeMaster prompts the user for what is missing.

This screen must be designed before individual Agents can be fully defined.

Tracked in: `Decisions/checklist-forgemaster-response-screen.md`

---

## 7. Select Actions Must Be Defined Before the Agent Catalogue

Per the ForgeMaster Interaction Handover (Section 11), the Select Actions must be agreed before finalizing the Agent catalogue. Actions shape what ForgeMaster understands about a request, which shapes what each Agent needs to be capable of.

**This is the recommended next discussion.**

---

## 8. ForgeMaster Robot Images — Three Poses Confirmed

Three ForgeMaster robot poses were created using AI image generation and confirmed on 25 August 2026.
All must be saved manually to the `public/` folder.

| Pose | Filename | Used In | Message |
|---|---|---|---|
| Standard — holding hammer | `public/forgemaster-default.png` | Processing/thinking modal | *"ForgeMaster is working on your task..."* |
| Questioning — hands up, "?" marks | `public/forgemaster-confused.png` | Outcome B modal | *"I am sorry but I have a few questions..."* |
| Thumbs up — smiling | `public/forgemaster-happy.png` | Outcome A modal | *"We are good to go! I am back to the task"* |

- **Correct name on all images:** ForgeMaster
- **Tagline (standard pose only):** "Forging Intelligence. Building the Future."

---

## 9. Three Initial Agents Provided for Context

These agents were shared for context — not yet created as formal profiles.

| Agent | Role | Nature |
|---|---|---|
| **Themis** | Test Cases Creator | Does the work — produces test assets |
| **Hermes** | The Summarizer | Transforms raw docs into structured insights |
| **Athena** | The "Testing" Mentor | Teaches the process — educational |

**Example chain:** User → ForgeMaster → Athena (teaches) → ForgeMaster routes to Hermes (analyze) and/or Themis (create test cases).

---

## 10. ForgeMaster Processing Modal — Agreed Design

When the user presses "Begin Workflow", a modal overlay appears on top of the first page (the intake screen remains visible but dimmed behind it).

### Agreed design:
- **ForgeMaster robot image** on the left side of the modal
- **Violet spinner** centered on the right half of the modal
- **Rotating status messages** below the spinner — confirmed messages:
  - *"Identifying the right specialists..."*
  - *"Building your workflow plan..."*
- The modal **transforms in place** into Outcome A or Outcome B when ForgeMaster finishes — no new page, no navigation

### Name correction required:
The mockup reviewed showed "MasterForger" — this must be corrected to **ForgeMaster** everywhere.

---

## 9. ForgeMaster Name — Confirmed Correct Spelling

The correct and only name is **ForgeMaster**.

A mockup was reviewed showing "MasterForger" — this is incorrect and must be corrected in any image, UI text, or document where it appears.

---

## 10. ForgeMaster Response Modal — Outcome A Partially Agreed

When ForgeMaster has successfully reviewed the request and built a plan:

- **Robot image:** ForgeMaster thumbs up pose (`public/forgemaster-happy.png`) with smile
- **Message:** *"We are good to go! I am back to the task"*
- **Right side of modal:** Plan summary — still to be designed (see open items)

Still needed:
- What the plan summary shows (Agent(s) selected, what each will do, execution order)
- How the user approves and starts the workflow

---

## 11. ForgeMaster Response Modal — Outcome B Agreed

When ForgeMaster cannot build a plan due to insufficient or ambiguous information:

- **Robot image:** ForgeMaster questioning pose (`public/forgemaster-confused.png`) with "?" marks
- **Message:** *"I am sorry but I have a few questions...."*
- **Summary box** showing what ForgeMaster received:
  - What the user wrote in the first screen
  - Agents Selected (if any)
  - Actions Selected (if any)
- **Two recovery options:**
  - *"Let me try again"* — text input box for the user to type clarification
  - *"Or Go back to the initial screen"* — back arrow returns to intake screen
- **"Begin workflow →" button** at bottom right — resubmits the clarified request directly

### Robot Images Confirmed
| Image | Filename | Use |
|---|---|---|
| Standard pose | `public/forgemaster-default.png` | Processing/thinking state |
| Questioning pose | `public/forgemaster-confused.png` | Outcome B — needs more info |

Both images created using AI image generation. Must be saved manually to `public/` folder.

---

## Open Items This Session Did Not Resolve

- Outcome A plan summary — what Agent(s), what they will do, execution order, how user approves
- Final names, roles, and descriptions for agents 3–6
- Select Actions: final list, behavior, and rules
- ✅ Approved ForgeMaster image set saved in `public/`: `forgemaster-garcon.png`, `forgemaster-default.png`, `forgemaster-confused.png`, `forgemaster-happy.png`, `forgemaster-running.png`, and `forgemaster-investigating.png`.
- Foundation Skills, Tools, and Guardrails content
- ForgeMaster's own agent profile
- ✅ Simulation built and working — processing modal, Outcome A, Outcome B all confirmed
- ✅ Session page (Outcome A working view) designed and built with:
  - Two-panel layout: left (workflow) + right (agent select + chat)
  - "Select an Agent" grayed out with "Coming soon" (phase 2)
  - Chat available after completion and during an Agent-specific question, action, or decision requiring user input
  - Per-agent download + Master Document (unified single source of truth)
  - Scroll arrows for 6+ agents in workflow plan
  - "My Saved Prompts" / "My Saved Projects" in sidebar (global, phase 2)
  - ForgeMaster Live Feed with Expand option

## 12. Approved Working-Session State Sequence — 27 August 2026

- Running Agent work uses `forgemaster-running.png` with a violet **Running** badge.
- When an Agent needs user input, that Agent is marked **Input Required**; completed Agents remain complete and the progress count does not reset.
- ForgeMaster changes to `forgemaster-investigating.png` with an amber **Investigating** badge.
- The right ForgeMaster panel opens, identifies the affected Agent, displays the question/action/decision, and enables the response field.
- After the user responds, only the affected Agent resumes and ForgeMaster returns to Running.
- `forgemaster-happy.png` and the green **Complete** badge appear only when every participating Agent is complete.
- The approved demonstration is: Athena completes, Hermes requests clarification, the user responds, Hermes resumes, and the workflow completes.
