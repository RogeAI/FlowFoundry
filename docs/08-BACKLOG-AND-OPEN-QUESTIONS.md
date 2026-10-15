# FlowFoundry Backlog and Open Questions

**Version:** 4.00  
**Status:** Remaining production questions after the two-page interaction prototype

---

## 1. Recommended Next Design Sequence

1. Connect the working-session states to real backend events.
2. Generalize questions, actions, and decisions beyond the current Hermes demonstration.
3. History and session continuation.
4. Files and context management.
5. Real Agent registry and capacity behavior.
6. Execution backend and provider integrations.

Review one major topic at a time and lock decisions before moving to the next.

---

## 2. Working-Session Page

The current prototype now demonstrates:

- visible participating Agents and accurate completed-Agent counts;
- sequential Athena-to-Hermes execution;
- Running, Investigating, Paused, and Complete status vocabulary;
- an Agent-specific clarification interruption;
- automatic opening of the ForgeMaster response panel;
- resumption after user input;
- final outputs and Master Document presentation.

Still define production behavior for parallel execution, generalized action and decision requests, retries, backend-driven replanning, and persisted resume.

---

## 3. ForgeMaster Triage

Open questions:

- When does ForgeMaster ask a clarifying question rather than infer intent?
- How are selected actions validated against the prompt and attachments?
- When may ForgeMaster override an Agent preference?
- How is the proposed workflow explained before execution?
- Does the user approve high-cost or high-impact workflows?
- Does ForgeMaster always synthesize the final response?

---

## 4. Busy and Unavailable Agents

The current prototype disables selection. Production rules still need decisions:

- queue versus immediate alternative;
- estimated wait;
- automatic substitution;
- user override;
- priority tiers;
- partial degradation;
- provider-specific versus Agent-wide capacity;
- status refresh frequency.

---

## 5. History and Saved Work

Define:

- History record schema;
- session title generation;
- search and filters;
- nested Agent execution details;
- draft versus started session;
- rename, archive, delete, export, and share;
- saved prompts versus saved results;
- retention and privacy;
- reset behavior relative to History.

---

## 6. Attachments and Context

Define:

- supported file types and size limits;
- upload progress and cancellation;
- file preview and removal;
- source attribution;
- access by participating Agents;
- versioning and replacement;
- malware and content scanning;
- storage, retention, and deletion;
- context-window limits and summarization.

---

## 7. Agent Registry

Replace in-source sample data with a managed registry containing:

- stable Agent identifier;
- display name and visual identity;
- role and capability description;
- supported actions;
- required inputs;
- tools and model configuration;
- availability and capacity signals;
- escalation rules;
- version and owner;
- permissions and tenant visibility.

---

## 8. Orchestration Backend

Define:

- ForgeMaster planning contract;
- execution graph representation;
- sequential and parallel scheduling;
- idempotency and retries;
- timeouts and cancellation;
- intermediate artifacts;
- context transfer between Agents;
- result synthesis;
- cost and token accounting;
- tracing and audit;
- human approval points.

---

## 9. Authentication and Authorization

Define:

- workspace identity;
- roles and permissions;
- ownership of sessions and attachments;
- Agent and tool access policy;
- administrative configuration;
- external collaborator access;
- audit access;
- organization and tenant boundaries.

---

## 10. Production Quality

Required future work includes:

- complete accessibility verification;
- browser and device matrix;
- performance budgets;
- telemetry and error reporting;
- security threat model;
- privacy and retention policy;
- content safety;
- disaster recovery;
- uptime and queue monitoring;
- internationalization;
- legal and licence review.

---

## 11. Current Prototype Limitations

- No real submission behavior.
- No Agent execution.
- No model or tool integration.
- No upload behavior.
- No persistence.
- No functional History or Saved pages.
- No real availability service.
- Working-session behavior is simulated rather than backend-driven.
- No production mobile navigation.
- Prototype Agent portraits and sample Agent data.

These limitations are deliberate and documented; they should not be mistaken for defects in the approved first-page concept.
