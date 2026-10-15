# Hermes–FlowFoundry Integration Plan

**Document status:** Approved direction; implementation not started  
**Agent:** Hermes  
**Supervisor:** ForgeMaster  
**Platform:** FlowFoundry  
**Development environment:** Claude Code  
**Backend language:** Python only

---

## 1. Purpose

This document explains what we are doing with Hermes, why the integration is necessary, the architectural boundaries that must be preserved, and the planned sequence of work.

Hermes already has a substantial information-intelligence design: identity, evidence discipline, source analysis, information-quality assessment, recommendations and actions, opt-in testability analysis, Test Design Handover, input handling, tool principles, and a final quality gate.

The next objective is not to rewrite that analytical behavior. The objective is to make Hermes a real FlowFoundry specialist Agent that can be selected, activated, supervised, and evaluated through ForgeMaster.

---

## 2. Why This Work Is Needed

Hermes currently exists mainly as a modular Agent definition. Those documents explain how Hermes should reason and respond, but they do not by themselves provide the runtime integration required by FlowFoundry.

Without a shared integration standard:

- ForgeMaster would need custom communication logic for every Agent;
- each Agent could use different task, result, status, error, and escalation formats;
- permissions and WFG/GO authorization could be interpreted inconsistently;
- session context, evidence references, logging, and audit behavior could diverge;
- future Agents would repeat the same infrastructure work;
- invalid or incomplete Agent responses could reach ForgeMaster without reliable validation.

The solution is to define a shared Agent contract and then implement a reusable Python Agent SDK based on that contract.

---

## 3. Meaning of the Agent Contract

The **Agent contract** defines the mandatory rules every specialist Agent must follow when communicating with FlowFoundry and ForgeMaster.

It will define:

- how an Agent identifies itself and declares its version;
- how capabilities, boundaries, prerequisites, and availability are described;
- the structured task ForgeMaster sends to an Agent;
- the structured result an Agent returns;
- permitted lifecycle and execution states;
- progress, completion, failure, cancellation, and blocked-state behavior;
- clarification and escalation messages;
- permission and tool-request behavior;
- session and context handling;
- WFG/GO authorization propagation;
- evidence, source, and deliverable references;
- logging, audit, validation, and error requirements.

The contract will be enforced through Python models and validation. It must not depend only on prompt wording or voluntary Agent behavior.

---

## 4. Meaning of the Agent SDK

**SDK** means **Software Development Kit**.

The FlowFoundry Agent SDK will be a reusable Python package that implements the common parts of the approved Agent contract. It will allow Hermes and future Agents to follow the same rules without rebuilding the same infrastructure separately.

Expected SDK components include:

- a base Agent interface;
- Agent manifest and capability models;
- task and result models;
- lifecycle status definitions;
- clarification and escalation models;
- input and output validation;
- permission and authorization checks;
- ForgeMaster communication helpers;
- logging and audit hooks;
- structured errors and safe failure handling;
- testing utilities for contract compliance.

The contract defines the rules. The SDK provides the reusable Python components for following those rules.

---

## 5. Target Architecture

```text
User
  ↓
ForgeMaster
  ├─ validates the objective and preferred Agent
  ├─ checks capabilities, prerequisites, availability, and permissions
  ├─ enforces WFG/GO
  └─ creates a structured Agent task
          ↓
FlowFoundry Agent Contract + Python Agent SDK
          ↓
Hermes Runtime
  ├─ loads only the required Hermes capabilities
  ├─ analyzes the supplied sources and context
  ├─ preserves evidence, uncertainty, and provenance
  ├─ validates the structured result
  └─ completes, asks for clarification, or escalates
          ↓
ForgeMaster
  ├─ supervises the result and Agent state
  ├─ replans or activates another Agent when required
  └─ presents the controlled outcome to the user
```

---

## 6. Responsibility Boundaries

### ForgeMaster owns

- request triage and routing;
- validation of a preferred Agent;
- WFG/GO control;
- activation and supervision;
- permission and tool authorization;
- session-level orchestration;
- progress and escalation handling;
- replanning and multi-Agent coordination;
- the final controlled response to the user.

### The shared Agent contract and SDK own

- common message structures;
- lifecycle and status semantics;
- validation boundaries;
- common permission, escalation, logging, and error mechanisms;
- consistent communication between ForgeMaster and all specialist Agents.

### Hermes owns

- information-intelligence analysis;
- evidence-aware synthesis;
- source and version analysis;
- information-quality assessment;
- extraction of findings, decisions, actions, risks, gaps, and unresolved matters;
- recommendations when useful and authorized;
- testability analysis only when explicitly requested;
- detailed Test Design Handover when explicitly requested for a downstream testing Agent;
- Hermes-specific quality gates and specialist output.

Hermes does not select itself, bypass ForgeMaster, grant its own permissions, silently activate other Agents, or independently change WFG/GO state.

---

## 7. Technology and Governance Decisions

- Copilot is retired and must not be used for new Hermes or FlowFoundry development.
- Claude Code is the development environment for this work.
- The FlowFoundry backend and Agent SDK are Python only.
- Pydantic models should enforce structured contracts at runtime.
- Prompts may guide reasoning but must not be the only enforcement layer for permissions, lifecycle, WFG/GO, escalation, or output validity.
- Existing Hermes analytical content should be reused after review rather than rewritten without cause.
- Historical Copilot adapters and character-limit packaging are archival material only.
- No Agent may bypass ForgeMaster.

---

## 8. Planned Work Sequence

### Phase 1 — Document the direction

Create and approve this integration plan.

### Phase 2 — Define the Agent contract

Specify and approve:

- Agent identity and manifest;
- capability declaration;
- task envelope;
- result envelope;
- lifecycle states;
- progress events;
- clarification and escalation;
- permissions and tool requests;
- source, evidence, and deliverable references;
- errors and failure behavior;
- versioning and compatibility rules.

### Phase 3 — Implement the Python Agent SDK

Build the reusable code from the approved contract, including models, base interfaces, validators, lifecycle helpers, logging hooks, and contract tests.

### Phase 4 — Implement the Hermes runtime adapter

Connect the existing Hermes instructions, skills, tools, and governance to the SDK. Hermes-specific code should contain specialist behavior, not duplicate shared platform infrastructure.

### Phase 5 — Register Hermes with ForgeMaster

Add Hermes to the Agent Registry with its real capabilities, boundaries, prerequisites, supported actions, availability, and version.

### Phase 6 — Validate end-to-end behavior

Test at minimum:

- suitable and unsuitable routing;
- preferred-Agent validation;
- WFG preventing execution;
- GO releasing only the held request;
- valid task execution;
- invalid task rejection;
- structured-result validation;
- clarification flow;
- permission denial;
- tool failure;
- Agent failure and timeout;
- escalation to ForgeMaster;
- Test Design Handover to the downstream testing Agent;
- session isolation, logging, and audit traceability.

### Phase 7 — Establish the reusable Agent pattern

Use the proven Hermes integration as the reference implementation for future FlowFoundry specialist Agents.

---

## 9. Initial Success Criteria

The integration will be considered successful when:

- ForgeMaster can discover Hermes through the Agent Registry;
- ForgeMaster can determine whether Hermes is appropriate for a request;
- WFG prevents Hermes execution until authorized GO;
- ForgeMaster can send a validated structured task;
- Hermes can return a validated structured result;
- evidence, limitations, unresolved matters, and deliverables remain traceable;
- clarification and escalation return to ForgeMaster through defined messages;
- permissions and unavailable tools fail safely;
- Hermes cannot bypass ForgeMaster or expand its own authority;
- the same contract and SDK can support another specialist Agent without redesigning the integration foundation.

---

## 10. Current Status and Next Approval Gate

This planning document is complete. No Agent contract or SDK code has been implemented as part of this step.

The next activity is to define the **ForgeMaster ↔ specialist Agent contract**. That contract must be reviewed and approved before implementation of the Python Agent SDK begins.

