# AI-Knowledge Repository Guide

## 1. Purpose of this repository

The `AI-Knowledge` repository is the central location for AI-related engineering, experimentation, learning, reusable standards, and solution development.

It is not limited to one AI platform.

The repository supports solutions implemented through:

- Microsoft Copilot
- GitHub Copilot
- Claude Code
- Custom AI agents
- MCP-enabled agents
- API-driven AI solutions
- n8n automations
- Full-stack AI applications
- Future AI platforms and agent frameworks

The repository must not be organized primarily around a vendor such as Claude, Microsoft, GitHub, or OpenAI.

The primary architectural principle is:

> **Organize by solution and responsibility, not by AI platform.**

A solution may start as a simple instruction-based Copilot assistant and later evolve into a full agent or application without needing to be moved to a different area of the repository.

---

## 2. Core principles

### 2.1 Solution-first organization

Every meaningful AI capability belongs primarily to a solution.

Current solutions:

- Hermes
- SAP Test Design Coach

The platform used to execute the solution is secondary. Hermes may run through GitHub Copilot today and Claude Code tomorrow. It remains the same solution. Only its technical implementation changes.

---

### 2.2 Separate agent concepts clearly

The repository deliberately distinguishes between:

```
Instructions  →  How the agent behaves
Skills        →  How the agent performs specific procedures
Tools         →  What systems or capabilities the agent can access
References    →  What knowledge the agent can consult
Evaluations   →  How we verify the agent behaves correctly
```

These must not be mixed together without reason. The distinction becomes increasingly important as agents grow more sophisticated.

---

### 2.3 Platform neutrality

The canonical design of a solution must remain independent of any specific AI platform.

Platform-specific configuration belongs in adapters only:

```text
Solutions/Hermes/
├── Agent/       ← canonical, platform-neutral
└── Adapters/
    ├── Copilot/
    └── Claude-Code/
```

**Anti-pattern — do not do this:**

```text
Solutions/
├── Hermes-Generic/         ← wrong: same agent split by platform
└── Hermes-Copilot/         ← wrong: creates duplication and drift
```

An adapter contains only what a specific platform needs to load the agent. It never duplicates skills, instructions, or core logic. It is a compiled snapshot or thin wrapper, not a second agent.

---

### 2.4 Start locally, share later

Agent assets should begin inside the solution that owns them.

```text
Solutions/Hermes/Agent/Skills/document-analysis/
```

Do not move an asset to `Shared/` because it might theoretically be reusable.

> **Promote to `Shared/` only after at least two independent solutions genuinely need it.**

---

### 2.5 Grow the repository only when required

Do not create every theoretically possible folder from day one. Folders exist because there is something meaningful to place inside them.

Empty architecture is still empty.

---

## 3. Naming conventions

These rules apply to every folder and file in this repository.

### Folders

- Always use `kebab-case`
- No spaces, no underscores, no mixed case
- No vendor or platform names as top-level folders

```text
✅  information-intelligence
✅  sap-itero-invisalign-test-design
❌  SKILLS
❌  Governance
❌  HERMES - Generic
❌  sap-itero-invisalign-test-design-coach.agent
```

### Files

- Content files: `kebab-case.md`
- Reserved ALL_CAPS entry-point files: `README.md`, `AGENT.md`, `SKILL.md`, `CLAUDE.md`, `TOOLS.md`
- No binary files (`.docx`, `.zip`, `.pdf`) inside agent asset folders — Markdown only

```text
✅  evidence-discipline.md
✅  AGENT.md
✅  SKILL.md
❌  AGENT_INSTRUCTIONS.md
❌  evidence-discipline.docx
❌  README.zip
```

### What maps to what

| Old pattern seen in this repo | Correct name |
|---|---|
| `AGENTS/` | `Solutions/` |
| `HERMES - Generic/` | `Solutions/Hermes/` |
| `HERMES -Copilot-Edition/` | `Solutions/Hermes/Adapters/Copilot/` |
| `Governance/` | `Instructions/` |
| `SKILLS/` | `Skills/` |
| `AGENT_INSTRUCTIONS.md` | `AGENT.md` |
| `skill-name.md` (flat) | `skill-name/SKILL.md` (in its own folder) |

---

## 4. Top-level structure

```text
AI-Knowledge/
│
├── README.md
│
├── Solutions/       ← real AI capabilities
│
├── Shared/          ← assets reused across two or more solutions
│
├── Experiments/     ← prototypes and trials not yet promoted
│
├── Learning/        ← reference material, study notes, courses
│
├── Docs/            ← repository governance and guides
│
├── _archive/        ← binary files and superseded content
│
├── .github/         ← GitHub configuration
│
└── .claude/         ← Claude Code configuration
```

---

## 5. Solutions/

Contains every real AI capability in the repository.

```text
Solutions/
├── Hermes/
├── SAP-Test-Design-Coach/
├── Testing-Mentor/       ← future
├── Ares/                 ← future
└── CAIRON/               ← future
```

Each solution is self-contained. It holds everything required to understand, maintain, and operate that solution.

---

## 6. Standard agent solution structure

```text
Solutions/
└── Hermes/
    │
    ├── README.md
    ├── manifest.yaml
    │
    ├── Agent/
    │   ├── AGENT.md
    │   │
    │   ├── Instructions/
    │   │   ├── evidence-discipline.md
    │   │   ├── input-handling.md
    │   │   └── final-quality-gate.md
    │   │
    │   ├── Skills/
    │   │   ├── information-intelligence/
    │   │   │   └── SKILL.md
    │   │   └── source-analysis/
    │   │       └── SKILL.md
    │   │
    │   ├── Tools/
    │   │   └── TOOLS.md
    │   │
    │   ├── References/       ← add when needed
    │   └── Evaluations/      ← add when needed
    │
    └── Adapters/
        ├── Copilot/
        │   ├── README.md
        │   └── copilot-adapter.md
        └── Claude-Code/      ← add when needed
```

Not every solution needs every folder. This is the maximum normal structure, not the mandatory minimum.

---

## 7. AGENT.md

`AGENT.md` defines the agent's identity and orchestration logic.

It answers:

- Who am I and what is my purpose?
- What am I responsible for and what am I not?
- Which instruction files govern my behavior?
- Which skills can I use and when?
- Which tools may I access?
- How should I validate my output?

**When to split into Instructions/:**

Start with everything in `AGENT.md`. Split into `Instructions/` only when the file becomes hard to navigate or when you need to selectively load rules in specific contexts.

---

## 8. Instructions/

Instructions define persistent behavioral rules that apply on every task.

The distinction from `AGENT.md`:

- `AGENT.md` = identity, routing, output behavior (the orchestration layer)
- `Instructions/` = detailed, referenceable behavioral rules

`Governance/` is not a valid folder name here. Any folder named Governance, Rules, or Standards inside an agent maps to `Instructions/`.

---

## 9. Skills/

A skill represents a defined procedure the agent can execute.

Each skill lives in its own folder:

```text
Skills/
└── requirement-analysis/
    ├── SKILL.md
    ├── References/     ← skill-specific reference material
    ├── Examples/       ← sample inputs and outputs
    └── Scripts/        ← any automation supporting the skill
```

Recommended `SKILL.md` sections:

```
# Skill Name
## Purpose
## When to use
## When not to use
## Required inputs
## Procedure
## Decision rules
## Validation rules
## Expected output
## Constraints
## References
```

---

## 10. Adapters/

An adapter contains only what a specific platform needs to load the canonical agent.

For **GitHub Copilot**: a single self-contained `.md` file with all behavior inlined, because Copilot does not load multiple files dynamically. This file is a compiled snapshot of `Agent/` — it must be updated when the canonical agent changes.

For **Claude Code**: a `CLAUDE.md` file that tells Claude Code where the agent files live and how to load them.

The adapter never duplicates skills or core logic independently. It is a delivery mechanism, not a second agent.

---

## 11. Shared/

```text
Shared/
├── Agent-Standards/     ← shared behavioral standards
├── Skills/              ← skills used by two or more solutions
├── SQA-Standards/       ← testing and quality standards
├── Prompt-Patterns/     ← reusable prompt structures
├── Evaluation-Standards/
└── Templates/           ← document and solution templates
```

Promote an asset here only after two independent solutions genuinely need it.

---

## 12. Experiments/

```text
Experiments/
├── n8n/
├── Copilot/
├── Claude-Code/
├── MCP/
├── APIs/
├── Models/
└── Prototypes/
```

Experiments stay separate until deliberately promoted into `Solutions/`. A promotion is a conscious decision, not an automatic consequence of maturity.

---

## 13. Learning/

```text
Learning/
├── AI-Fundamentals/
├── AI-Agents/
├── Claude-Code/
├── Copilot/
├── Git-GitHub/
├── MCP/
├── n8n/
├── APIs/
├── Prompt-Engineering/
└── AI-Automation/
```

Learning material is never executable. It is study notes, course summaries, and reference reading. It must remain separate from `Solutions/`.

---

## 14. manifest.yaml

Every established solution should contain a machine-readable manifest.

```yaml
name: hermes
description: >
  Platform-neutral AI agent for transforming raw and mixed
  information into structured intelligence and useful outputs.
solution_type: agent
maturity: experimental
version: 0.1.0
platforms:
  github-copilot: true
  claude-code: false
  standalone: true
components:
  instructions: true
  skills: true
  tools: true
  references: false
  evaluations: false
application:
  frontend: false
  backend: false
  api: false
owner: Roger
```

Maturity stages: `Concept` → `Experimental` → `Prototype` → `Validated` → `Production` → `Deprecated`

---

## 15. Minimum structure for a new solution

A brand-new Copilot-only solution needs only:

```text
Solutions/
└── My-Solution/
    ├── README.md
    ├── manifest.yaml
    └── Adapters/
        └── Copilot/
            └── instructions.md
```

Add `Agent/` when the solution grows to have skills, instructions, and routing logic worth separating.

---

## 16. Where does a new file belong?

```
Does it belong to one specific solution?
  Yes → Solutions/<Solution-Name>/

Is it reusable across two or more solutions?
  Yes → Shared/

Is it experimental or a prototype?
  Yes → Experiments/

Is it learning or reference material?
  Yes → Learning/

Does it govern the entire repository?
  Yes → Docs/ or .github/ or .claude/
```

---

## 17. Full repository rules

1. Organize by solution, not by vendor or platform.
2. A solution keeps the same location as it grows.
3. Instructions, Skills, Tools, References, and Evaluations are separate architectural concepts.
4. `AGENT.md` defines identity and routing — not every detailed procedure.
5. Skills describe procedures. Tools provide capabilities. References provide knowledge.
6. Evaluations verify agent behavior.
7. Platform-specific files belong in adapters only.
8. Adapters never duplicate skills or core agent logic.
9. Assets begin solution-specific and move to `Shared/` only after proven reuse by two solutions.
10. Experiments remain separate from formal solutions.
11. Learning material remains separate from executable solution assets.
12. Every established solution has a `README.md` and eventually a `manifest.yaml`.
13. All folder names are kebab-case. No spaces, no underscores.
14. All agent asset files are Markdown. No binary files in agent folders.
15. Do not create folders or governance artifacts until they are actually needed.
16. The repository supports a solution evolving from a simple prompt to a complete AI application without requiring reorganization.
