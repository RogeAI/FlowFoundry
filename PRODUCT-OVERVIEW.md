# FlowFoundry

> Describe the outcome you want. FlowFoundry coordinates the right specialist
> Agents and keeps the work visible, supervised, and under your control.

## The 30-second explanation

FlowFoundry is a workspace for completing complex work with coordinated AI
Agents.

Instead of asking users to find the right Agent, decide the sequence, and manage
every handoff themselves, FlowFoundry begins with the outcome the user wants to
achieve. ForgeMaster—the supervisory orchestrator—reviews the request, decides
what expertise is needed, and coordinates one or more specialist Agents.

The user remains involved. They can provide source material, express a preferred
Agent, pause execution until they are ready, answer questions, and follow the
work through to a result.

## The problem FlowFoundry addresses

As organizations introduce more AI Agents, users can face a new kind of
complexity:

- Which Agent should I use?
- What happens when several specialties are needed?
- Who decides the order of work?
- How is context passed between Agents?
- What happens if an Agent is blocked or needs clarification?
- How can a user see what is happening and stay in control?

A catalogue of separate Agents does not solve these questions. It can simply
move the coordination burden from the organization to the user.

FlowFoundry is designed as an orchestration workspace rather than a collection
of unrelated chat tools.

## Who FlowFoundry is for

FlowFoundry is intended for:

- employees who want to achieve an outcome without learning an Agent catalogue;
- specialists who need focused Agents to work with shared context;
- managers who want visibility into how AI-supported work is progressing;
- teams that need repeatable handoffs between different forms of expertise; and
- organizations that want human control, governance, and traceability around
  multi-Agent work.

## The central idea

The user starts with an objective—not a technical workflow.

```text
User objective
      ↓
ForgeMaster understands and prepares the flow
      ↓
One or more specialist Agents perform focused work
      ↓
ForgeMaster supervises, handles escalations, and adapts
      ↓
The user receives a connected result
```

The effective relationship is always:

```text
User → ForgeMaster → Specialist Agent(s)
```

Choosing a preferred Agent does not bypass ForgeMaster. It tells ForgeMaster
where the user would like the work to begin, while preserving supervision and
the ability to identify missing expertise or prerequisites.

## How FlowFoundry works

### 1. Describe the desired outcome

The user explains what they want to achieve in natural language. They do not
need to translate the objective into an Agent-by-Agent plan.

### 2. Add useful context

The user can add source material, request useful actions, or identify one
preferred Agent when that helps.

### 3. Decide whether to begin now

If the user wants to prepare the request without starting the work, they can use
**Wait for GO**.

Wait for GO is a real hold state in the product model. Context and selections
can be prepared, but execution does not begin until the user gives GO.

### 4. ForgeMaster prepares the workflow

ForgeMaster reviews the objective and decides whether it should:

- handle the request directly;
- ask the user for clarification;
- assign one specialist Agent;
- arrange several Agents in sequence; or
- coordinate Agents working in parallel or through a mixed flow.

### 5. Specialist Agents perform focused work

Each specialist works within a declared area of expertise. Agents do not form
uncontrolled chains themselves; they escalate to ForgeMaster when another skill,
a decision, or new information is required.

### 6. The user follows one connected session

The objective, plan, participating Agents, questions, progress, and outputs stay
connected in one workspace. The history is organized around the user’s objective,
not as a confusing list of internal Agent interactions.

## What ForgeMaster does

ForgeMaster is the supervisory layer of FlowFoundry.

It is responsible for:

- understanding the outcome;
- performing the initial triage;
- checking whether clarification is needed;
- selecting and sequencing suitable specialists;
- keeping the overall context together;
- receiving Agent escalations;
- adapting the plan when circumstances change; and
- remaining present throughout the session.

Its guiding principle is:

> Observe continuously. Intervene selectively.

ForgeMaster is not intended to perform every task itself. Its value is knowing
when to act, when to delegate, and when to return to the user.

## A simple example

A user asks:

> Review these requirements and prepare a test-ready plan.

FlowFoundry may respond by coordinating a sequence such as:

1. one specialist examines and organizes the source material;
2. another checks requirement quality and identifies uncertainties;
3. another prepares the test-focused output; and
4. ForgeMaster keeps the work connected, handles questions, and presents the
   resulting plan as one session.

The user does not need to design this chain. They can still see the proposed
flow, respond when input is required, and keep control of execution.

## What FlowFoundry offers to users and managers

### Start with business language

Users describe the outcome they need rather than navigating a technical Agent
architecture.

### Use specialist expertise without managing every handoff

FlowFoundry can bring together different Agents while ForgeMaster maintains the
overall plan and context.

### Keep work visible

The workspace is designed to show which Agents are involved, what stage the work
has reached, and when the user needs to respond.

### Preserve human control

Users can hold execution with Wait for GO, answer clarification questions, and
see when ForgeMaster changes the plan.

### Organize work around outcomes

One objective remains one connected session, even when several Agents
contribute. This gives users and managers a clearer view of progress and result.

### Create a foundation for governance

A persistent supervisory layer provides a place to enforce approval,
availability, policy, audit, and validation rules as the platform matures.

## Ways of working supported by the product model

FlowFoundry is designed to support several kinds of workflow:

| Workflow | What it means to the user |
|---|---|
| ForgeMaster-only | The request is simple enough to handle without a specialist |
| Single specialist | One focused Agent performs the work under supervision |
| Sequential specialists | Several Agents contribute in a required order |
| Parallel specialists | Independent work can happen at the same time |
| Mixed workflow | Sequential and parallel work are combined around one objective |

The user does not need to choose the workflow type. ForgeMaster prepares it from
the outcome, context, dependencies, and available capabilities.

## The user experience

The FlowFoundry experience is designed around four questions:

1. **What do you want to achieve?**
2. **What context or actions will help?**
3. **Are you ready to begin?**
4. **What is happening now, and is your input needed?**

The workspace includes:

- an outcome-focused request area;
- optional source attachments;
- optional requested actions;
- one preferred specialist selection;
- visible Agent availability;
- Wait for GO and GO controls;
- ForgeMaster’s proposed flow;
- participating Agent and progress information; and
- clarification and result states within the same session.

## What FlowFoundry is not

FlowFoundry is not intended to be:

- a directory of disconnected chatbots;
- a system where the user must understand every Agent before starting;
- an uncontrolled network in which Agents create their own chains;
- a black box that hides who is working or why; or
- a replacement for user decisions when clarification or approval is required.

## Current product status

FlowFoundry currently provides a functional product prototype and a defined
orchestration model.

| Demonstrated in the current baseline | Still required for a production platform |
|---|---|
| Outcome-first workflow composition | Production authentication and authorization |
| Optional actions and preferred Agent | Durable multi-user sessions and history |
| Wait for GO and GO behavior | Complete live multi-Agent orchestration |
| ForgeMaster triage and supervision model | Production file scanning and retention |
| Agent availability and selection states | Queueing, capacity, and retry operations |
| Initial local backend workflow path | Full governance and audit operations |
| Simulated working-session progress and clarification | Monitoring, deployment, support, and recovery model |
| Product, interaction, and visual specifications | Validated end-to-end external integrations |

The current application should be presented as a strong product and interaction
baseline—not as a completed enterprise production service.

## Product direction

The longer-term direction is a governed workspace in which organizations can add
specialist Agents with clear capabilities, let ForgeMaster assemble appropriate
flows, and give users one understandable place to guide and follow the work.

As FlowFoundry grows, the product must retain three qualities:

1. **Simple for the user** — begin with the outcome.
2. **Controlled for the organization** — route work through explicit boundaries.
3. **Visible for everyone involved** — show the flow, decisions, and progress.

## Presentation-ready storyline

This README can be translated into a concise presentation using the following
sequence:

1. **The challenge** — more Agents can create more coordination complexity.
2. **The idea** — FlowFoundry begins with an outcome and prepares the workflow.
3. **Who it helps** — users, specialists, managers, and governed organizations.
4. **The operating model** — User → ForgeMaster → Specialist Agent(s).
5. **How it works** — describe, add context, hold or release, coordinate, follow.
6. **Why ForgeMaster matters** — triage, supervision, escalation, and adaptation.
7. **The value** — simplicity, specialist expertise, visibility, and control.
8. **Current maturity** — functional prototype and defined product model, with
   production capabilities still to be built.
9. **The vision** — one governed workspace for coordinated AI work.

## Further reading

This page explains FlowFoundry for users and managers. Product and implementation
owners should continue with:

- [`docs/00-HANDOVER-INDEX.md`](docs/00-HANDOVER-INDEX.md) for the authoritative
  documentation map;
- [`docs/01-PRODUCT-ARCHITECTURE.md`](docs/01-PRODUCT-ARCHITECTURE.md) for locked
  product decisions; and
- [`CLAUDE.md`](CLAUDE.md) for implementation working rules.
