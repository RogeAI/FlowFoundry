# FlowFoundry — ForgeMaster Agent Deployment Guide

**Version:** 1.00
**Date:** 27 August 2026
**Status:** Deployment and implementation handover
**Related specification:** `ForgeMaster-Agent-Specification-v1.00.md`
**Target development environment:** Claude Code
**Backend constraint:** Python only

---

## 1. Purpose

This document explains how to turn the approved ForgeMaster design into a real, testable FlowFoundry control-plane Agent.

It defines:

- where the approved specification belongs;
- which parts become runtime instructions, Python domain logic, infrastructure, configuration, and tests;
- how ForgeMaster should be registered;
- how Claude Code should approach the work;
- required implementation phases and approval gates;
- acceptance, security, deployment, monitoring, and rollback requirements;
- the exact initial prompt to give Claude Code.

This guide does not itself implement ForgeMaster. It is the controlled handover for implementation.

---

## 2. Authoritative inputs

Claude Code must read the current FlowFoundry source and documentation before changing code.

### 2.1 Required reading order

1. `CLAUDE.md`
2. `README.md`
3. `docs/00-HANDOVER-INDEX.md`
4. `docs/01-PRODUCT-ARCHITECTURE.md`
5. `docs/02-UX-INTERACTION-SPECIFICATION.md`
6. `docs/03-DESIGN-SYSTEM-AND-CONTENT.md`
7. `docs/04-TECHNICAL-HANDOVER.md`
8. `docs/05-TEST-AND-ACCEPTANCE.md`
9. `docs/08-BACKLOG-AND-OPEN-QUESTIONS.md`
10. `docs/09-CLAUDE-CODE-CONTINUATION.md`
11. `docs/10-EXACT-BASELINE-INVENTORY.md`
12. `docs/agents/forgemaster/FORGEMASTER-AGENT-SPECIFICATION-v1.00.md`
13. this deployment guide

### 2.2 Authority order

When requirements conflict, use this order:

1. explicit current user decisions;
2. locked FlowFoundry product decisions;
3. approved ForgeMaster specification;
4. approved UX and technical handovers;
5. current runnable source as evidence of present behavior;
6. older prototypes and historical documents.

Current code is not automatically the intended final behavior. Where it conflicts with an approved requirement, document the conflict and propose a controlled migration.

---

## 3. Required document placement

Place the approved ForgeMaster files in the authoritative FlowFoundry repository:

```text
Solutions/FlowFoundry/
└── docs/
    └── agents/
        └── forgemaster/
            ├── FORGEMASTER-AGENT-SPECIFICATION-v1.00.md
            └── FORGEMASTER-DEPLOYMENT-GUIDE-v1.00.md
```

Update `docs/00-HANDOVER-INDEX.md` to link both documents after their placement is approved.

Do not overwrite historical handovers. Mark superseded implementation assumptions through the existing documentation and change-history process.

---

## 4. What the specification becomes

The complete Markdown specification is not the runtime prompt.

```text
Approved ForgeMaster specification
             |
             +-- concise runtime system instructions
             +-- Python domain objects and rules
             +-- application use cases
             +-- Agent Registry profile
             +-- policy and permission enforcement
             +-- tool gateway controls
             +-- API contracts
             +-- audit and History events
             +-- evaluations and acceptance tests
             +-- deployment configuration
```

### 4.1 Human-readable specification

The `.md` is the canonical design source used for review, implementation mapping, governance, and change control.

### 4.2 Runtime instructions

Create a concise, versioned ForgeMaster instruction artifact derived from the approved behavioral sections. Do not paste the full document into the model context.

The runtime instruction must contain stable behavioral rules, not volatile Agent rosters, availability, permissions, model names, or session data.

### 4.3 Dynamic context

Supply these at runtime from authoritative services:

- current Agent Registry projection;
- capability and boundary declarations;
- readiness and availability;
- workflow and session context;
- selected actions and preferred Agent;
- WFG and approval state;
- tool grants and data restrictions;
- applicable policies;
- current contract versions.

### 4.4 Platform enforcement

Implement critical controls outside the model:

- WFG and GO;
- permission and approval checks;
- session isolation;
- valid state transitions;
- Agent and tool boundaries;
- secrets protection;
- consequential-action blocking;
- audit recording;
- bounded retry behavior;
- completion validation.

---

## 5. Current implementation assessment

The current backend is an early triage implementation, not the complete approved ForgeMaster.

### 5.1 Current useful foundations

- Python FastAPI backend;
- domain, application, and infrastructure directories;
- `Session`, `WorkflowPlan`, `WorkflowStep`, and Agent entities;
- a `BeginWorkflow` use case;
- a ForgeMaster triage service;
- one preferred-Agent field;
- WFG state and release behavior;
- basic workflow types;
- initial API and POM tests;
- one-objective History intent.

### 5.2 Gaps to address

The current implementation:

- embeds the Agent roster in the system prompt;
- directly imports and calls Anthropic from a domain service;
- hard-codes the model and runtime options;
- relies on free-form JSON parsing rather than a fully validated contract;
- falls back to a ready ForgeMaster-only plan when parsing fails;
- has only a small subset of required workflow states;
- does not implement plan versioning;
- does not implement assignment, escalation, validation, approval, or permission contracts;
- does not enforce assignment-specific tool access;
- does not provide complete audit and History records;
- does not implement a protected control-plane registry profile;
- does not distinguish ForgeMaster service health from workflow state;
- does not implement real specialist execution and supervision;
- does not implement the required security, readiness, and regression suite.

### 5.3 Specific behaviors requiring review

Claude Code must explicitly inspect and resolve these current behaviors:

1. `ForgeMasterService` lives in the domain layer but depends directly on the Anthropic SDK and environment configuration.
2. The prompt contains hard-coded specialist IDs and descriptions, creating a second Agent Registry.
3. A malformed model response becomes a `READY` ForgeMaster-only plan, which can conceal contract failure.
4. The triage message reports prior WFG state using an inverted expression after WFG may already have been released.
5. The current begin use case releases WFG automatically, so API semantics must clearly preserve the distinction between Begin workflow and GO.
6. Workflow states do not yet represent clarification, approval, delegation, supervision, replanning, validation, consolidation, blocking, or stopping.

Do not patch these independently without first producing the architecture and migration map described below.

---

## 6. Target architecture

Preserve the Python-only backend and REST separation. The following structure is recommended; Claude Code may refine filenames while preserving responsibilities.

```text
backend/
├── domain/
│   ├── forgemaster/
│   │   ├── entities.py
│   │   ├── contracts.py
│   │   ├── decisions.py
│   │   ├── guardrails.py
│   │   ├── permissions.py
│   │   ├── states.py
│   │   └── services.py
│   ├── entities/
│   ├── events/
│   └── repositories/
│
├── application/
│   └── forgemaster/
│       ├── intake_request.py
│       ├── triage_request.py
│       ├── plan_workflow.py
│       ├── request_approval.py
│       ├── dispatch_assignment.py
│       ├── supervise_workflow.py
│       ├── handle_escalation.py
│       ├── validate_result.py
│       └── close_workflow.py
│
├── infrastructure/
│   ├── ai/
│   │   ├── forgemaster_instructions.py
│   │   ├── forgemaster_prompt_builder.py
│   │   └── anthropic_forgemaster_adapter.py
│   ├── registry/
│   │   └── agent_registry.py
│   ├── policy/
│   │   ├── policy_evaluator.py
│   │   ├── permission_service.py
│   │   └── approval_service.py
│   ├── tools/
│   │   └── tool_gateway.py
│   ├── audit/
│   │   └── audit_repository.py
│   ├── repositories/
│   └── api/
│
└── tests/
    ├── unit/
    ├── integration/
    ├── contract/
    ├── security/
    ├── evaluations/
    └── regression/
```

### 6.1 Domain layer

The domain must remain provider-independent and contain:

- workflow and assignment entities;
- state transitions;
- triage and routing decisions;
- approval and permission concepts;
- validation outcomes;
- escalation and failure types;
- guardrail identifiers;
- repository and provider interfaces.

The domain must not import Anthropic, HTTP frameworks, environment variables, or provider-specific response objects.

### 6.2 Application layer

The application layer coordinates use cases and transactions. It calls domain services and abstract interfaces but does not contain UI logic or provider-specific SDK calls.

### 6.3 Infrastructure layer

Infrastructure implements:

- Anthropic communication;
- prompt construction;
- persistent or temporary repositories;
- Agent Registry loading;
- policy and permission services;
- tool gateway;
- audit storage;
- FastAPI schemas and routes.

### 6.4 Frontend boundary

The React/TypeScript frontend receives only safe public fields and workflow state through REST. It does not own:

- operational Agent definitions;
- system instructions;
- tool permissions;
- policy decisions;
- secrets;
- completion validation;
- authoritative workflow state.

---

## 7. Required implementation artifacts

Claude Code must produce or update the following categories.

### 7.1 Documentation

- installed ForgeMaster specification;
- installed deployment guide;
- handover index entry;
- architecture decision describing the provider boundary;
- implementation mapping from specification sections and guardrails to code and tests;
- updated technical handover;
- updated test and acceptance documentation;
- change-history entry;
- unresolved-decision list.

### 7.2 Domain contracts

At minimum:

- submitted request;
- triage decision;
- versioned workflow plan;
- workflow step and dependency;
- specialist assignment;
- progress update;
- escalation;
- specialist result;
- ForgeMaster validation;
- approval request and response;
- permission grant;
- final outcome;
- audit event reference.

### 7.3 State models

Implement or map:

- WFG Hold;
- Intake;
- Clarification Required;
- Triage;
- Planning;
- Approval Required;
- Delegating;
- Supervising;
- Replanning;
- Validating;
- Consolidating;
- Completed;
- Blocked;
- Stopped.

Specialist task state must remain distinct from ForgeMaster workflow state and specialist availability.

### 7.4 Agent Registry

The server-side ForgeMaster entry must include:

- stable ID `forgemaster`;
- `control_plane` class;
- user-selectable `false`;
- mandatory triage `true`;
- persistent supervision `true`;
- profile and configuration versions;
- readiness and deployment state;
- capabilities and enabled skills;
- permitted control-plane tools;
- supported contract versions;
- compatibility metadata;
- health state.

The frontend receives only the approved public projection.

### 7.5 Runtime instructions

Create a concise versioned instruction artifact derived from the approved specification.

It must:

- identify ForgeMaster's control-plane role;
- preserve WFG and authority boundaries;
- require registry-based routing;
- prohibit invented Agents and capabilities;
- require bounded assignments;
- require validation before completion;
- require transparent escalation and limitations;
- avoid hard-coded Agent rosters;
- avoid hard-coded availability;
- avoid raw secrets and provider configuration;
- produce validated structured output.

### 7.6 Model adapter

The provider adapter must:

- implement a domain-defined interface;
- receive the versioned instruction and dynamic context;
- request a schema-constrained output where supported;
- validate response structure;
- classify timeout, provider, refusal, malformed-output, and capacity failures;
- avoid silently converting invalid responses into successful plans;
- expose safe diagnostic information;
- support controlled model configuration and substitution;
- preserve traceability to the active configuration bundle.

### 7.7 Policy, permission, and tool gateway

Implement execution-time checks for:

- WFG state;
- authenticated actor;
- assignment and Agent identity;
- tool and operation;
- target and data scope;
- purpose and duration;
- approval state;
- confidentiality restrictions;
- consequential-action classification;
- separation of duties;
- audit availability.

Denied operations must fail closed and return an actionable classification.

### 7.8 Audit and History

Implement one top-level History record per user objective, with nested material workflow events.

Record configuration versions, plan versions, Agents, assignments, permission references, tool outcomes, approvals, escalations, validation, and closure without storing credentials or private chain-of-thought.

---

## 8. Implementation phases and approval gates

Do not implement the complete Agent in one uncontrolled change.

### Phase 0 — Placement and architecture audit

**Work:**

- place both approved documents;
- read the required source and documentation;
- map current code to the specification;
- identify conflicts, gaps, and migration risks;
- propose the target file structure;
- produce a guardrail-to-enforcement matrix;
- produce a phased implementation plan.

**Do not change runtime behavior in this phase.**

**Approval gate:** Product and technical review of the map and plan.

### Phase 1 — Pure domain foundation

**Work:**

- introduce provider-independent contracts;
- implement workflow and assignment states;
- implement transition validation;
- implement plan versioning;
- introduce failure, escalation, approval, and validation types;
- preserve current public behavior through compatibility adapters where needed.

**Approval gate:** Unit and contract tests pass; no Anthropic dependency exists in the new domain components.

### Phase 2 — Registry and configuration

**Work:**

- create the Python-owned registry;
- register ForgeMaster as control plane;
- move specialist roster data out of prompts;
- create safe public projections;
- version ForgeMaster configuration and instructions;
- retain frontend compatibility through REST.

**Approval gate:** Registry and API tests pass; private fields cannot reach the browser.

### Phase 3 — Model boundary and structured triage

**Work:**

- move Anthropic calls into infrastructure;
- create a provider interface;
- add the concise runtime instruction;
- inject dynamic registry and session context;
- implement schema validation;
- implement safe failure for malformed and unavailable model responses;
- remove the silent successful fallback.

**Approval gate:** Deterministic adapter, malformed-output, timeout, and routing tests pass.

### Phase 4 — WFG, approval, and permission enforcement

**Work:**

- make Begin workflow and GO semantically distinct;
- enforce WFG before triage and execution;
- implement scoped approval records;
- implement assignment-specific permissions;
- add the tool gateway policy checks;
- add consequential-action controls;
- add bounded retries.

**Approval gate:** WFG and permission denial-path tests pass at the backend boundary.

### Phase 5 — Delegation, supervision, and escalation

**Work:**

- implement bounded assignments;
- implement specialist progress and results;
- implement escalation handling;
- implement plan revision and recovery;
- implement supporting-Agent disclosure and approval rules;
- preserve one objective as one workflow and History item.

**Approval gate:** Single, chained, parallel, mixed, escalation, and recovery scenarios pass.

### Phase 6 — Validation, consolidation, and closure

**Work:**

- implement acceptance checking;
- separate task completion from validated completion;
- implement correction and evidence requests;
- implement multi-Agent consolidation;
- implement accurate terminal outcomes;
- release temporary permissions on closure.

**Approval gate:** False-completion, conflicting-evidence, partial-result, and uncertain-outcome tests pass.

### Phase 7 — Observability, History, and user experience

**Work:**

- implement material workflow events;
- implement configuration and plan traceability;
- implement protected audit records;
- expose appropriate History and progress projections;
- preserve private prompts, reasoning, credentials, and restricted metadata;
- update the UI only after backend contracts stabilize.

**Approval gate:** User-visible History, audit integrity, privacy, and frontend contract tests pass.

### Phase 8 — Security evaluation and restricted pilot

**Work:**

- run prompt-injection and authority-escalation tests;
- verify session isolation and external transmission controls;
- verify safe failure and emergency restriction;
- establish monitoring, alerts, rollback, and incident ownership;
- define pilot scope, users, tools, and limits;
- create the immutable release bundle.

**Approval gate:** No unresolved Critical issue and no applicable unresolved High issue.

### Phase 9 — Production-readiness decision

**Work:**

- evaluate pilot evidence;
- calibrate quantitative thresholds;
- resolve or formally accept remaining limitations;
- verify documentation, monitoring, rollback, and governance;
- approve or reject production readiness.

Production status must not be inferred from code completion.

---

## 9. Testing and evaluation matrix

### 9.1 Unit tests

Cover:

- contract validation;
- state transitions;
- plan versioning;
- capability matching rules;
- approval validity;
- permission scope;
- retry limits;
- failure classification;
- validation outcomes;
- History nesting.

### 9.2 Integration tests

Cover:

- API to application to domain flow;
- registry loading and public projection;
- model adapter success and failure;
- WFG and GO enforcement;
- permission gateway denial;
- audit event creation;
- tool result verification;
- workflow recovery after interruption.

### 9.3 Behavioral evaluations

Cover:

- ForgeMaster-only work;
- suitable and unsuitable preferred Agents;
- bounded supporting Agents;
- no suitable Agent;
- conflicting actions;
- missing prerequisites;
- meaningful user corrections;
- focused clarification;
- transparent disagreement;
- partial and blocked outcomes.

### 9.4 Security tests

Cover:

- prompt injection through user text, attachments, retrieval, tools, and specialists;
- attempted WFG bypass;
- impersonated approval;
- cross-session access;
- permission transfer;
- secret exposure;
- unauthorized external transmission;
- registry tampering;
- audit failure;
- provider and dependency failure.

### 9.5 Completion and recovery tests

Cover:

- specialist reports Completed without evidence;
- conflicting specialist results;
- tool timeout with uncertain external outcome;
- deterministic repeated failure;
- user stop during execution;
- capacity limitation;
- invalid model response;
- unavailable independent verification;
- service restart during an active workflow.

### 9.6 Required baseline commands

Preserve the repository's approved validation commands:

```text
pnpm run build
pnpm test
pnpm run lint
```

Run the Python test suites defined for the backend and POM package. Claude Code must report exact commands, results, skipped tests, and environmental limitations.

---

## 10. Guardrail implementation matrix

Claude Code must create a traceable matrix with one row for every `FM-Gxxx` guardrail.

Required columns:

| Column | Meaning |
|---|---|
| Guardrail ID | Stable identifier from the specification |
| Requirement | Concise approved rule |
| Enforcement class | Behavioral, Platform-enforced, or Both |
| Owning component | Domain, application, policy, gateway, API, UI, or operations |
| Implementation location | Exact file or configuration reference |
| Positive test | Evidence that permitted behavior succeeds |
| Denial-path test | Evidence that prohibited behavior is blocked |
| Observable result | State, event, error, or audit evidence |
| Failure behavior | Safe behavior if enforcement is unavailable |
| Status | Planned, Implemented, Tested, Accepted, or Blocked |

No Platform-enforced or Both guardrail may be marked complete without a denial-path test.

---

## 11. Configuration and environment

### 11.1 Configuration bundle

Every deployed ForgeMaster must reference an immutable bundle containing:

- specification version;
- runtime-instruction version;
- contract version;
- policy and guardrail version;
- Agent Registry version;
- model and relevant settings;
- skill and tool versions;
- permission configuration;
- evaluation-suite version;
- environment and release metadata;
- readiness and approvals.

### 11.2 Secrets and environment variables

- Keep secrets outside source control.
- Do not place API keys in prompts, registry entries, tests, logs, or documentation.
- Validate required configuration at service startup.
- Fail clearly when required provider configuration is missing.
- Use test doubles for deterministic tests.

### 11.3 Environments

Maintain distinct development, test, pilot, and production configurations.

Pilot and production must not inherit broad development permissions or test credentials.

---

## 12. Deployment procedure

### 12.1 Pre-deployment

Confirm:

- the approved specification version;
- completed implementation mapping;
- passing required tests;
- no unresolved Critical issues;
- applicable High issues are resolved;
- registry and contract compatibility;
- secrets and environment configuration;
- database or state migration readiness where applicable;
- monitoring and alerts;
- rollback bundle;
- incident owner;
- release approval.

### 12.2 Restricted deployment

Deploy first with:

- limited users;
- limited Agents;
- read-only or reversible tools where possible;
- conservative permissions;
- bounded workflow size;
- bounded timeouts and retries;
- enhanced monitoring;
- an immediate pause and rollback mechanism.

### 12.3 Smoke tests

After deployment, verify:

- service health;
- registry loading;
- safe public profile projection;
- WFG hold;
- GO release;
- simple ForgeMaster-only triage;
- preferred-Agent validation;
- malformed model-response handling;
- permission denial;
- audit event creation;
- accurate History state;
- rollback readiness.

### 12.4 Promotion

Promote only after controlled evidence confirms the intended deployment scope. Record the promoted configuration bundle and approval.

---

## 13. Monitoring and operational controls

Monitor:

- workflow volumes and states;
- clarification and approval frequency;
- preferred-Agent corrections;
- Agent participation and failures;
- tool latency, denial, and failure;
- retries and replanning;
- completion-validation rejection;
- guardrail denials;
- capacity and provider errors;
- user stops and corrections;
- configuration mismatch;
- audit-event loss;
- suspected false completion;
- security alerts.

Critical conditions may automatically pause dispatch, revoke access, disable a tool or capability, or roll back the bundle.

Monitoring must not store credentials or unnecessary private content.

---

## 14. Rollback and incident response

### 14.1 Rollback package

Maintain:

- previous known-good configuration bundle;
- compatible code and schema state;
- rollback steps;
- active-workflow handling rules;
- validation checks;
- responsible decision-makers;
- user-notification rules.

Rollback must restore a complete compatible bundle, not only an older prompt.

### 14.2 Active workflows

During rollback:

- stop or pause affected dispatch;
- preserve durable workflow state;
- identify completed and uncertain external actions;
- do not blindly retry consequential operations;
- migrate only when compatibility is proven;
- inform users when outcome or route is materially affected.

### 14.3 Security incident

Authorized responders may revoke credentials, disable tools, pause Agents, restrict context, preserve evidence, and roll back. ForgeMaster may coordinate but must not erase evidence or independently close the incident.

---

## 15. Required Claude Code outputs

For every phase, Claude Code must provide:

1. the exact scope completed;
2. files created or changed;
3. approved requirements implemented;
4. guardrails mapped;
5. tests added or updated;
6. commands run and exact results;
7. unresolved risks or decisions;
8. compatibility impact;
9. documentation updates;
10. recommended next phase.

Claude Code must not claim completion when tests were skipped, enforcement is absent, or behavior remains unverified.

---

## 16. Initial prompt to give Claude Code

Use the following prompt for the first implementation session.

```text
We are starting the controlled implementation of ForgeMaster for FlowFoundry.

The backend must remain Python-only. Preserve the React/TypeScript frontend over REST and the existing Domain-Driven Design direction. Do not introduce a second backend language or a frontend-owned operational Agent Registry.

First read, in order:
1. CLAUDE.md
2. README.md
3. docs/00-HANDOVER-INDEX.md
4. docs/01-PRODUCT-ARCHITECTURE.md
5. docs/02-UX-INTERACTION-SPECIFICATION.md
6. docs/03-DESIGN-SYSTEM-AND-CONTENT.md
7. docs/04-TECHNICAL-HANDOVER.md
8. docs/05-TEST-AND-ACCEPTANCE.md
9. docs/08-BACKLOG-AND-OPEN-QUESTIONS.md
10. docs/09-CLAUDE-CODE-CONTINUATION.md
11. docs/10-EXACT-BASELINE-INVENTORY.md
12. docs/agents/forgemaster/FORGEMASTER-AGENT-SPECIFICATION-v1.00.md
13. docs/agents/forgemaster/FORGEMASTER-DEPLOYMENT-GUIDE-v1.00.md

Treat the ForgeMaster specification as the approved canonical human-readable design. Do not paste the complete document into the runtime system prompt. Derive a concise, versioned runtime instruction and enforce critical controls in Python.

For this first phase, perform Phase 0 only: placement and architecture audit.

Do not change runtime behavior yet.

Produce:
- confirmation of the authoritative source tree and documents read;
- an exact current-state architecture map;
- a gap analysis against every major ForgeMaster specification section;
- a list of conflicts and risks in the current implementation;
- a proposed target Python file and package structure;
- a migration plan that preserves locked FlowFoundry behavior;
- a guardrail-to-enforcement-and-test matrix for every FM-Gxxx identifier;
- a phased implementation plan with approval gates;
- focused questions for decisions that cannot be safely inferred.

Pay particular attention to:
- the direct Anthropic dependency in the current domain service;
- the hard-coded Agent roster in the prompt;
- malformed-response fallback behavior;
- WFG and GO semantics;
- the current WFG-state message construction;
- missing contracts, states, approval, permission, validation, audit, and recovery behavior;
- one objective as one top-level History item;
- ForgeMaster as a non-selectable control-plane Agent;
- safe frontend projection from a Python-owned registry.

Challenge weak or risky architecture rather than accepting it automatically. Distinguish current behavior, approved requirements, proposals, and open decisions. Do not invent business rules or claim that unimplemented capabilities exist.

Stop after delivering the Phase 0 audit and plan. Wait for explicit approval before implementing Phase 1.
```

---

## 17. Prompts for later phases

After Phase 0 is approved, use one phase per Claude Code instruction.

### 17.1 Phase 1 instruction pattern

```text
Implement only Phase 1 — Pure domain foundation — from the approved ForgeMaster deployment guide and the approved Phase 0 plan.

Preserve current user-visible behavior. Keep provider SDKs and environment access out of the domain layer. Add or update unit and contract tests. Update the implementation mapping and guardrail matrix. Run the required relevant validation and report exact results.

Stop after Phase 1 and wait for approval before continuing.
```

Replace the phase number and scope only after the preceding phase is approved.

---

## 18. Completion definition

ForgeMaster deployment is complete only when:

- approved documents are installed and indexed;
- implementation matches the approved specification;
- runtime instructions are concise and versioned;
- dynamic registry and session context replace hard-coded roster content;
- critical controls are enforced outside the model;
- all applicable guardrails map to implementation and tests;
- contract, orchestration, security, recovery, and communication evaluations pass;
- audit, monitoring, pause, and rollback mechanisms operate;
- the immutable configuration bundle is registered;
- pilot evidence supports the approved deployment scope;
- readiness is formally approved;
- no required work is misrepresented as complete.

Code completion alone is not Agent deployment completion.

---

## 19. Open deployment decisions

Before later deployment phases, explicitly decide:

- model provider, model, and model settings;
- persistent storage technology;
- authentication and authorization service;
- approval-record mechanism;
- tool gateway implementation;
- audit storage and retention;
- queue, timeout, retry, and cost limits;
- capacity and availability service;
- initial specialist catalogue;
- initial tool catalogue;
- pilot users and permitted workflows;
- hosting environment;
- named product, technical, security, evaluation, and incident owners;
- quantitative readiness thresholds.

These are not authorized merely by approving this guide.

---

## 20. Change history

| Version | Date | Status | Summary |
|---|---|---|---|
| 1.00 | 27 August 2026 | Deployment handover created | Defined placement, architecture mapping, phased Claude Code implementation, tests, deployment, rollback, and exact starting prompt. |
