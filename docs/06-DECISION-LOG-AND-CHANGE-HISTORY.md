# FlowFoundry Decision Log and Change History

**Version:** 4.00  
**Purpose:** Preserve why the current product and first-page design look and behave as they do

---

## 1. Naming Evolution

| Stage | Name | Outcome |
|---|---|---|
| Initial concept | AI Agent Hub | Replaced |
| Initial supervisor | Orc / Orchestrator | Replaced |
| Explored product names | Maestro, Orchestrum, AgentForge | Not selected |
| Final application name | FlowFoundry | Locked |
| Final supervisor name | ForgeMaster | Locked |

The tagline **Forge the right flow.** is the current approved brand line.

---

## 2. Architecture Decisions

### 2.1 Persistent Supervision

ForgeMaster is not only the entry point. It remains logically present throughout the session, listening for escalation or the need to intervene.

---

### 2.2 Direct Selection

Direct Agent selection is a preferred starting point. The path remains `User → ForgeMaster → Selected Agent`.

---

### 2.3 Escalation

Agents escalate to ForgeMaster for missing capability, uncertainty, prerequisites, clarification, or replanning. Agents do not independently form uncontrolled chains.

---

### 2.4 Session History

History represents one user objective. Internal Agent executions are nested within that session.

---

### 2.5 Concurrency

A logical Agent may serve several users through isolated executions. Busy and Unavailable are capacity-facing states, not proof that the Agent is a single human-like worker.

---

## 3. WFG Decisions

1. WFG is an explicit execution hold.
2. The interface must show **WFG ACTIVE** or equivalent visible status.
3. The user may continue adding context while WFG is active.
4. GO releases the complete request.
5. GO automatically turns WFG off.
6. ForgeMaster performs triage before specialists activate.

---

## 4. First-Page Design Evolution

### 4.1 Initial Prototype

The first version established the main prompt, action shortcuts, Agent cards, navigation, and availability concepts. It was judged too decorative and insufficiently enterprise-oriented.

---

### 4.2 Enterprise Workspace Revision

The page moved toward a structured enterprise workspace with:

- global navigation;
- side navigation;
- compact panels;
- operational status;
- explicit ForgeMaster supervision;
- multi-select actions;
- disabled Busy and Unavailable Agents.

---

### 4.3 Light Enterprise Revision

The working surfaces changed to white and pale grey/lavender. The complete FlowFoundry artwork became the main header brand panel. Reset moved near New workflow. The prompt and actions became a side-by-side request builder with an expandable composer.

---

### 4.4 Readability Revision

The design was judged too small at 100% zoom. The final baseline therefore:

- moderately increases typography;
- uses more of wide screens;
- enlarges Agent descriptions and status text;
- adds visible selected-action chips under the prompt;
- replaces initials with temporary role icons;
- makes Agent buttons content-sized.

---

### 4.5 Enterprise Reference Alignment

The interface adopted a light lavender/white enterprise workspace with stronger violet navigation, larger sidebar icons, compact uppercase section headings, portrait-led Agent cards, and explicit selected states. The visual reference informed colour, hierarchy, density, and interaction clarity rather than page structure.

---

### 4.6 Final Logo Revision

Several rustic coin and forged-metal concepts were explored and rejected for the application header because they became illegible or visually disconnected at small size. The approved logo is a modern transparent convergence mark with purple `FLOW`, navy `FOUNDRY`, and a restrained copper coordination point. Its `2095:677` ratio is locked.

---

### 4.7 Final Interaction Refinements

- Available and selected action counts are separate.
- The action catalogue uses a desktop bottom-right vertical resize handle; the mistaken header Expand action was removed.
- The prompt retains its own Expand/Reduce behavior.
- A selected Agent card receives an unmistakable lavender and violet state.
- The selected button reads **✓ Selected** and can be clicked again to unselect.
- Header and sidebar grid boundaries are aligned.

### 4.8 About FlowFoundry Page

- About appears after Governance, keeping the operational navigation sequence intact.
- The page explains the website through the user journey rather than the internal framework.
- Existing ForgeMaster and specialist artwork illustrates coordination without introducing generic marketing imagery.
- The page emphasizes outcomes, visible progress, Wait for GO, and continued user oversight.
- The About experience is the home route and therefore the first page users see; the workflow intake interface moves to `/workspace`.

---

## 5. Removed or Rejected Treatments

- Diamond-F brand mark.
- Split orange/black wordmark treatment.
- Decorative filler panel titled **Context makes the flow smarter**.
- Separate wide Requested outcomes panel below the composer.
- Full-width Agent selection buttons.
- Reset session at the bottom of the page.
- Tiny metadata-style typography across primary content.
- Action selection where order could be mistaken for execution sequence.
- Coin and forged-metal application-header logos.
- A separate action-catalogue Expand link that rearranged the entire request builder.

---

## 6. Current Source Milestones

| Milestone | Description |
|---|---|
| First prototype | Initial FlowFoundry first page and social artwork |
| Enterprise redesign | Workspace structure and enterprise branding |
| Interaction refinement | Side-by-side request builder, guidance, WFG release, reset relocation |
| Readability refinement | Larger type, selected chips, temporary Agent icons, compact controls |
| Handover baseline | Documentation, repository cleanup, current tests, and upload-ready package |
| Final visual baseline | Modern logo, enterprise palette, aligned navigation, portrait Agent cards, and selection clarity |
| Version 4 handover | Claude Code instructions, exact reproduction inventory, extracted-package verification, and new delivery archive |

---

## 7. Important Interpretation Notes

- Visual examples supplied during review were references for look and feel, not instructions to copy another product’s structure.
- The current Agent names, descriptions, icons, recent sessions, counts, and statuses are sample content.
- The current page demonstrates the start experience only.
- No design decision in this document implies that backend orchestration is already implemented.
