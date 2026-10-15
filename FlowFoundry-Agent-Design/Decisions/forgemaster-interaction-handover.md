# FlowFoundry — ForgeMaster Interaction Discussion Handover

**Date:** 25 August 2026
**Status:** Current agreed state for this discussion
**Scope:** FlowFoundry first-page interaction model involving ForgeMaster, Extra Options, and the Agents section
**Out of scope:** Full FlowFoundry architecture, detailed Agent definitions, visual styling, technical implementation, and complete product handover

---

## 1. Purpose

This handover records the decisions reached during the focused discussion about how a user begins work in the FlowFoundry web app.

The discussion took place before defining the individual Agents. Its purpose was to establish how the three main first-page sections work together and how ForgeMaster responds when the user expresses a preference for a particular Agent.

This is a latest-state decision document, not a transcript of the conversation.

---

## 2. First-Page Interaction Areas

The FlowFoundry first page is understood as having three related interaction areas:

1. **ForgeMaster section** — the user describes the required outcome, problem, question, or task in natural language.
2. **Extra Options section** — the user may select one or more optional actions that further describe the requested work. Also referred to as "Select Actions" in the UI.
3. **Agents section** — the user may select one preferred specialist Agent.

These areas contribute to one assembled request. They are not separate execution paths, and none of them bypasses ForgeMaster.

---

## 3. Supported Request Combinations

The user may begin work in any of the following ways:

### 3.1 ForgeMaster request only

The user writes what is needed in the ForgeMaster section and submits the request.

ForgeMaster interprets the request, determines whether clarification is required, and decides how the work should be handled.

### 3.2 ForgeMaster request with actions

The user writes what is needed and selects one or more actions from Extra Options before submitting.

The selected actions enrich the request by expressing the types of work the user wants. They do not determine execution order. ForgeMaster interprets the objective and actions together, resolves dependencies, and determines the appropriate workflow.

### 3.3 ForgeMaster request with actions and one preferred Agent

The user writes what is needed, may select one or more actions, and selects one preferred Agent before submitting.

Only one Agent may be selected on the first page. The selected Agent represents the user's preferred destination or starting specialist; it is not a binding routing instruction and does not bypass ForgeMaster.

Actions remain optional. Therefore, a request consisting of an objective and one preferred Agent is also valid even when no Extra Options are selected.

---

## 4. ForgeMaster's Role

ForgeMaster receives and evaluates the complete assembled request in every case.

ForgeMaster must:

- understand the intended user outcome;
- consider the natural-language request, selected actions, and preferred Agent together;
- identify missing or ambiguous information;
- determine whether ForgeMaster can handle the request alone or whether specialist participation is needed;
- validate any preferred-Agent selection;
- determine dependencies and execution order;
- explain meaningful routing corrections to the user;
- continue supervising after routing is agreed.

The governing route remains:

```
User → ForgeMaster → Specialist Agent(s), when needed
```

---

## 5. Preferred-Agent Selection

### 5.1 Selection constraint

The user may select no Agent or one Agent. Selecting several Agents directly is not allowed on the first page.

### 5.2 Meaning of the selection

Selecting an Agent indicates an informed user preference. FlowFoundry may presume that the user has a reason for the choice, but it must not presume that the choice is correct.

The selection is therefore a **preferred Agent**, not a guaranteed Agent assignment.

### 5.3 ForgeMaster validation

Before specialist work begins, ForgeMaster validates the preferred Agent against:

- the user's intended outcome;
- the selected actions;
- the Agent's declared capabilities and boundaries;
- required prerequisites and dependencies;
- availability or operational constraints;
- whether additional specialties are required.

### 5.4 Validation outcomes

#### Suitable selection
ForgeMaster confirms the selected Agent and proceeds.

#### Possibly unsuitable selection
ForgeMaster explains the apparent mismatch and recommends the Agent that appears better suited.

#### Clearly unsuitable selection
ForgeMaster must not silently redirect. It explains why and asks the user to approve the proposed replacement.

> Example: "You selected the Test Designer Agent, but this request appears to concern an API integration. The Integration Architect Agent is a better match. Would you like me to redirect the task?"

#### Several specialties required
ForgeMaster may propose the selected Agent as the lead while coordinating supporting Agents. ForgeMaster must explain this plan rather than making additional Agent participation invisible.

#### No suitable Agent available
ForgeMaster states that no suitable Agent is currently available or defined. It must not force the task into the nearest Agent merely to continue.

### 5.5 User approval boundary

A meaningful change from the user's selected Agent requires explanation and user approval. ForgeMaster may not silently substitute a different specialist.

---

## 6. Submission and Workflow Controls

| Control | Meaning |
|---|---|
| New workflow | Start a fresh request draft or session |
| Begin workflow | Submit the request while WFG is inactive |
| GO | Release and submit a WFG-held request |

These controls are not interchangeable.

---

## 7. Agreed Interaction Sequence

```
User describes the desired outcome
             │
             ├── optionally selects action(s)
             │
             └── optionally selects one preferred Agent
                         │
                         ▼
              User submits or presses GO
                         │
                         ▼
               ForgeMaster evaluates the
                complete assembled request
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Clarify input   Confirm route   Recommend correction
                                         │
                                         ▼
                              User approves redirection
                                         │
                                         ▼
                              ForgeMaster supervises work
```

---

## 8. Confirmed Decisions

1. The first page contains ForgeMaster, Select Actions (Extra Options), and Agents sections.
2. The user can submit a natural-language objective without selecting actions or an Agent.
3. Actions are optional and may be combined with the objective.
4. Agent selection is optional.
5. Only one preferred Agent may be selected by the user.
6. The selected Agent is a preference, not a binding route.
7. ForgeMaster always validates the preferred Agent before specialist work begins.
8. ForgeMaster explains mismatches and recommends a better Agent.
9. ForgeMaster does not silently redirect a meaningful Agent choice.
10. The user approves a meaningful redirection.
11. ForgeMaster may coordinate supporting Agents when several specialties are required.
12. ForgeMaster does not force a request into an unsuitable Agent.
13. New workflow starts a fresh draft; Begin workflow submits normally; GO releases and submits a WFG-held request.
14. ForgeMaster retains orchestration and supervisory authority in every entry path.

---

## 9. Design Principle

FlowFoundry should respect informed user choice without requiring the user to understand or control the orchestration architecture.

The user may express intent and preference. ForgeMaster remains responsible for validation, transparent correction, workflow design, and supervision.

---

## 10. Open Matters for Later Discussion

- The exact contents and names of Select Actions;
- The final Agent catalogue, names, roles, and capability boundaries;
- The wording and visual design of validation and redirection messages;
- Whether low-impact supporting-Agent additions require confirmation or only notification;
- How Agent availability affects redirection and queueing;
- How unsaved drafts are recovered when New workflow is selected;
- The detailed working-session experience after ForgeMaster triage;
- Technical implementation and acceptance criteria.

---

## 11. Recommended Next Discussion

Before defining individual Agents, decide the purpose and behavior of the Select Actions, including:

- what each action communicates to ForgeMaster;
- whether actions are always multi-select;
- how incompatible or redundant actions are handled;
- whether ForgeMaster may recommend adding or removing an action;
- how selected actions are summarized before submission.

After those rules are established, the Agent catalogue can be designed against clearer routing and capability requirements.
