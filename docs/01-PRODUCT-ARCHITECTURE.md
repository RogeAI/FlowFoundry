# FlowFoundry Product Architecture

**Version:** 4.00  
**Status:** Current product baseline  
**Scope:** Product logic and orchestration model

---

## 1. Product Purpose

FlowFoundry is a unified workspace for achieving outcomes through coordinated AI Agents. Users should not need to understand the internal Agent catalogue before they can begin. They can describe an outcome in natural language, add context, select useful actions, or express a preferred starting Agent.

The product is an orchestration environment, not a collection of unrelated chatbots.

---

## 2. Core Terminology

### 2.1 FlowFoundry

FlowFoundry is the application and user-facing workspace.

---

### 2.2 ForgeMaster

ForgeMaster is the persistent system-level orchestrator and supervisor. It replaced the earlier working name **Orc / Orchestrator**.

ForgeMaster:

- receives every request first at the logical control-plane level;
- understands the user’s intended outcome;
- performs initial triage before specialist work begins;
- decides whether clarification is needed;
- selects, validates, sequences, and supervises Agents;
- maintains session context and workflow state;
- receives Agent escalations;
- replans when dependencies, failures, capacity, or new information require it;
- remains present even when the user directly selects an Agent.

The governing principle is:

> Observe continuously. Intervene selectively.

---

### 2.3 Specialist Agent

A specialist Agent is a focused worker with a declared role and capability boundary. It performs work assigned or validated by ForgeMaster. It does not own platform-wide orchestration and does not independently construct uncontrolled peer-to-peer Agent chains.

---

### 2.4 Session

A session represents one user objective and its full context. It may contain ForgeMaster-only work, a single specialist, several specialists, sequential dependencies, or parallel branches.

The session is the top-level History object.

---

## 3. Control-Plane Architecture

```text
                         USER
                           │
                           ▼
                 ┌─────────────────┐
                 │   ForgeMaster   │
                 │ Triage, control │
                 │ and supervision │
                 └────────┬────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
       Agent A          Agent B          Agent C
          │               │               │
          └───────────────┴───────────────┘
                          │
                   ForgeMaster retains
                    session oversight
```

The effective path remains:

```text
User → ForgeMaster → Specialist Agent(s)
```

Direct Agent selection changes the preferred starting specialist; it does not bypass ForgeMaster.

---

## 4. Initial Request Flow

1. The user describes an outcome.
2. The user may attach context.
3. The user may select one or more requested actions.
4. The user may identify a preferred starting Agent.
5. The user may activate WFG to hold execution.
6. Submission or GO sends the complete request to ForgeMaster.
7. ForgeMaster alone performs initial triage.
8. ForgeMaster asks for clarification or forms an execution strategy.
9. Specialist Agents start only after that decision.
10. The user moves to a working-session experience.

```text
User request
     │
     ▼
ForgeMaster triage
     │
     ├── Ask for clarification
     ├── Handle alone
     ├── Assign one Agent
     ├── Build an ordered chain
     └── Form a parallel or mixed team
```

---

## 5. Supported Workflow Types

### 5.1 ForgeMaster-Only

```text
User → ForgeMaster → Result
```

Used when specialist delegation would add no value.

---

### 5.2 Single-Agent

```text
User → ForgeMaster → Agent A → Result
```

ForgeMaster supervises the assigned or preferred Agent.

---

### 5.3 Chained

```text
User → ForgeMaster → Agent A → Agent B → Agent C → Result
```

ForgeMaster owns the dependency order, context transfer, and replanning.

---

### 5.4 Parallel or Mixed

```text
                   ┌→ Agent A ─┐
User → ForgeMaster ├→ Agent B ─┼→ ForgeMaster / Result
                   └→ Agent C ─┘
```

Logical participation can be parallel even when a provider, model, tool, or queue imposes physical capacity limits.

---

## 6. Direct Agent Selection

Direct selection is a user preference, not an architectural bypass.

```text
User selects Agent
        │
        ▼
   ForgeMaster validates
        │
        ▼
  Preferred Agent works
        │
        ▼
ForgeMaster continues supervising
```

ForgeMaster may change the plan when the selected Agent is inappropriate, blocked, unavailable, uncertain, or missing prerequisite input. The eventual working-session UI should explain any such change.

---

## 7. Agent Escalation

A specialist escalates to ForgeMaster when:

- the request is outside its scope;
- the selected Agent is not appropriate;
- prerequisite work is missing;
- another specialty is required;
- the Agent lacks confidence;
- clarification is required;
- a tool, provider, or dependency fails;
- policy or safety constraints block progress.

```text
Specialist Agent
      │
      ▼
ForgeMaster
      ├── Ask the user
      ├── Add or substitute an Agent
      ├── Revise the sequence
      ├── Retry or queue work
      └── Return work to the original Agent
```

---

## 8. WFG and GO Logic

WFG means **Wait for GO**. It is an execution hold, not merely wording in a prompt.

While WFG is active:

- context may be entered and retained;
- attachments may be added;
- actions and an Agent preference may be selected;
- ForgeMaster does not start execution;
- specialists do not begin work;
- the interface visibly shows that the system is waiting for GO.

When GO is pressed:

1. the complete held request is released;
2. WFG automatically becomes inactive;
3. ForgeMaster performs initial triage;
4. specialist execution begins only if ForgeMaster decides it is needed.

The next new request starts with WFG off unless the user activates it again.

---

## 9. Availability, Capacity, and Concurrency

A logical Agent definition can serve multiple users through isolated executions. It should not be modeled as one human-like worker that can only hold one conversation.

However, an execution can be constrained by:

- model-provider rate limits;
- tool concurrency;
- external-system limits;
- account quotas;
- long-running jobs;
- organizational policies;
- cost controls;
- queue capacity.

The first page currently represents three simplified states:

- **Available:** selectable as a preference.
- **Busy:** visible but selection is disabled.
- **Unavailable:** visible but selection is disabled.

The production capacity algorithm, queuing rules, wait estimates, substitution policy, and retry behavior remain open.

---

## 10. Reset Session

Reset Session clears the current draft state:

- prompt text;
- selected actions;
- selected Agent preference;
- WFG state;
- expanded composer state.

Reset requires confirmation. It is placed persistently near **New workflow**, not at the bottom of the page.

The production rule for whether a reset draft creates, updates, or preserves a History record remains open.

---

## 11. History Model

History follows the user’s objective, not the internal execution path.

```text
History item: Review checkout requirements
  ├── ForgeMaster triage
  ├── Axiom analysis
  ├── Verity validation
  ├── Atlas test design
  └── Final result
```

The example above is one History item, not four.

---

## 12. Locked Decisions

1. The application name is **FlowFoundry**.
2. The supervisory orchestrator is **ForgeMaster**.
3. ForgeMaster is always logically present and listening for needed intervention.
4. ForgeMaster performs initial triage before specialist activation.
5. Direct Agent selection remains supervised by ForgeMaster.
6. Agents escalate to ForgeMaster rather than independently forming uncontrolled chains.
7. The platform supports ForgeMaster-only, single-Agent, chained, parallel, and mixed workflows.
8. Actions are multi-select.
9. Action selection order does not define execution order.
10. ForgeMaster determines dependencies and execution order.
11. WFG holds execution until GO.
12. GO deactivates WFG automatically.
13. Reset clears the full current draft and requires confirmation.
14. Busy and Unavailable Agents cannot be selected from the current first page.
15. One user objective creates one top-level History item.
16. The user transitions away from the first page after triage.
17. The current first page is a functional prototype, not the complete platform.
18. Clicking an already-selected preferred Agent unselects it and returns control to ForgeMaster.
19. The modern FlowFoundry logo is the approved application identity; retired coin and metal-plate concepts are historical only.

---

## 13. Product Boundaries

The current code does not implement real orchestration, AI calls, uploads, Agent services, persistence, authentication-driven personalization, History storage, or queues. It demonstrates the approved first-page concept and a simulated working-session route with Agent progress, escalation for user clarification, resumption, and completion states.
