# Backlog: ForgeMaster Response Screen

## Context

The current prototype only has a first-page intake screen. When the user presses
"Begin Workflow", there is no second screen or state defined to show ForgeMaster's response.

This screen must be designed and built before individual Agents can be fully defined,
because Agent presentation, plan approval, and ForgeMaster validation messages all
belong on this screen — not the first page.

**Do not act on this until explicitly prioritized.**

---

## Robot Images Required

| Image | Filename | Use |
|---|---|---|
| Standard — holding hammer | `public/forgemaster-default.png` | Processing/thinking state |
| Questioning — hands up, "?" marks | `public/forgemaster-confused.png` | Outcome B — needs more info |
| Thumbs up — smiling | `public/forgemaster-happy.png` | Outcome A — plan ready |

---

## ForgeMaster Must Surface One of Two Outcomes

### Outcome A — Ready to proceed (partially agreed)
- Request was understood, plan was created, Agent(s) selected
- **Robot image:** ForgeMaster thumbs up pose (`public/forgemaster-happy.png`) with smile
- **Message:** *"We are good to go! I am back to the task"*
- **Right side of modal:** Plan summary — content still to be designed:
  - [ ] Which Agent(s) were selected and why
  - [ ] What each Agent will do
  - [ ] Execution order (single Agent vs. chain)
  - [ ] How the user approves and starts the workflow
  - [ ] Whether the user can adjust the plan before approving

### Outcome B — Needs more information ✅ Designed
- Request received but incomplete or ambiguous
- ForgeMaster cannot responsibly build a plan yet
- **Scope:** Outcome B is ONLY about the initial prompt — not about attachment/document quality. Document issues are discovered later during workflow execution by the agents (e.g. Hermes detects contradictions).
- **Robot image:** ForgeMaster questioning pose (`forgemaster-confused.png`) with "?" marks
- **ForgeMaster message:** *"I am sorry but I have a few questions...."*
- **Explanation (NEW):** A warm-toned warning box explains WHAT the problem is:
  - Empty prompt: *"Your request is empty — I need you to describe what outcome you are looking for so I can identify the right specialists and build a workflow."*
  - Vague prompt: *"Your request doesn't provide enough detail for me to determine which specialists to assign. Please clarify what you are trying to achieve."*
- **Summary box** showing what ForgeMaster received:
  - What the user wrote in the first screen
  - Agents Selected (if any)
  - Actions Selected (if any)
- **Recovery options:**
  - *"Let me try again"* — text input box for the user to clarify
  - Two buttons: **"Begin workflow →"** (resubmit) and **"Go back to initial screen"** (returns to intake)

---

## Agreed Design Decisions

- **Trigger:** "Begin Workflow" opens a modal overlay — the intake screen remains visible but dimmed behind it
- **Layout:** ForgeMaster robot image on the left; spinner and status messages on the right
- **Spinner:** Violet, centered on the right half of the modal
- **Rotating status messages** below the spinner:
  - *"Identifying the right specialists..."*
  - *"Building your workflow plan..."*
- **Transition:** Modal transforms in place into Outcome A or Outcome B — no new page, no navigation
- **Name:** ForgeMaster (not MasterForger — correct all mockups and images)

---

## Checklist

### Design decisions still needed
- [x] Does "Begin Workflow" open a new page, a modal, or an inline panel? ✅ **Modal overlay**
- [ ] What does Outcome A look like — how is the plan presented?
- [x] What does Outcome B look like — how does ForgeMaster ask for clarification? ✅ **Designed — see above**
- [ ] How does the user approve the plan in Outcome A?
- [x] How does the user provide missing details in Outcome B? ✅ **Text input + "Begin workflow →" button**
- [x] Can the user go back to the intake screen to edit their request? ✅ **"Or Go back to the initial screen" back arrow**
- [ ] How are multi-Agent chains displayed in the plan view?
- [ ] How does ForgeMaster explain a routing correction on this screen?

### Implementation tasks (after design is agreed)
- [ ] Create the ForgeMaster Response Screen component
- [ ] Implement Outcome A — plan view with Agent(s) listed
- [ ] Implement Outcome B — clarification request view
- [ ] Implement user approval / adjustment flow
- [ ] Implement navigation back to intake screen
- [ ] Update `docs/02-UX-INTERACTION-SPECIFICATION.md` to include this screen
- [ ] Update `docs/04-TECHNICAL-HANDOVER.md` to reflect the new screen

---

## Related

- [ForgeMaster Interaction Handover](forgemaster-interaction-handover.md)
- [Session Decisions 2026-08-25](session-2026-08-25-decisions.md)
