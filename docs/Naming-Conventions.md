# Naming Conventions

These rules apply to every folder and file in this repository without exception.

---

## Folders

### Rule: always kebab-case

All folder names use lowercase kebab-case.

```text
✅  solutions
✅  hermes
✅  sap-test-design-coach
✅  information-intelligence
✅  sap-itero-invisalign-test-design

❌  AGENTS
❌  HERMES - Generic
❌  HERMES -Copilot-Edition
❌  Governance
❌  SKILLS
❌  sap-itero-invisalign-test-design-coach.agent
```

### Rule: no spaces, no dots, no underscores in folder names

Spaces and dots break path handling in scripts, CI, and many AI platforms.

```text
✅  test-design-handover
❌  test design handover
❌  test_design_handover
❌  test.design.handover
```

### Rule: no platform names as top-level folders

The top level of the repository is organized by responsibility, not by vendor.

```text
✅  Solutions/
✅  Shared/
✅  Experiments/
✅  Learning/

❌  Claude/
❌  Copilot/
❌  OpenAI/
❌  Microsoft/
```

Platform names are allowed only inside `Adapters/` and `Experiments/`.

---

## Files

### Rule: content files use kebab-case

```text
✅  evidence-discipline.md
✅  input-handling.md
✅  final-quality-gate.md
✅  copilot-adapter.md

❌  EvidenceDiscipline.md
❌  evidence_discipline.md
❌  EVIDENCE-DISCIPLINE.md
```

### Rule: entry-point files use ALL_CAPS

A small set of reserved filenames use ALL_CAPS because they are structural entry points, not content files.

| Filename | Purpose |
|---|---|
| `README.md` | Human-readable introduction to the folder |
| `AGENT.md` | Agent identity, routing, and orchestration |
| `SKILL.md` | Skill definition and procedure |
| `TOOLS.md` | Tool integration principles |
| `CLAUDE.md` | Claude Code configuration |

These names are fixed. Do not vary them.

```text
✅  AGENT.md
✅  SKILL.md
✅  README.md

❌  AGENT_INSTRUCTIONS.md
❌  agent.md
❌  Agent-Instructions.md
❌  skill.md
```

### Rule: no binary files in agent asset folders

All agent instructions, skills, references, and governance files must be Markdown.

```text
✅  evidence-discipline.md
✅  SKILL.md

❌  evidence-discipline.docx
❌  SKILL.pdf
❌  README.zip
```

Binary files belong in `_archive/` only.

---

## Solution folder names

Solution folders use title-case kebab-case — each word capitalized, words separated by hyphens.

```text
✅  Hermes
✅  SAP-Test-Design-Coach
✅  Testing-Mentor
✅  CAIRON

❌  hermes
❌  sap-test-design-coach
❌  testing_mentor
```

This distinguishes solution names (proper nouns) from component folders (common nouns).

---

## Quick reference

| Context | Convention | Example |
|---|---|---|
| Top-level area | Title-case | `Solutions/`, `Shared/` |
| Solution name | Title-case kebab | `Hermes`, `SAP-Test-Design-Coach` |
| Component folder | Title-case | `Agent/`, `Skills/`, `Instructions/`, `Adapters/` |
| Skill folder | kebab-case | `information-intelligence/` |
| Content file | kebab-case | `evidence-discipline.md` |
| Entry-point file | ALL_CAPS | `AGENT.md`, `SKILL.md`, `README.md` |
| Adapter folder | Title-case | `Copilot/`, `Claude-Code/` |

---

## Common mistakes from this repository's history

| What was used | What it should be |
|---|---|
| `AGENTS/` | `Solutions/` |
| `HERMES - Generic/` | `Solutions/Hermes/` |
| `HERMES -Copilot-Edition/` | `Solutions/Hermes/Adapters/Copilot/` |
| `Governance/` | `Instructions/` |
| `SKILLS/` | `Skills/` |
| `AGENT_INSTRUCTIONS.md` | `AGENT.md` |
| `skill-name.md` (flat file) | `skill-name/SKILL.md` (own folder) |
| `.docx` files in agent folders | `.md` files only |
| `README.zip` in agent folders | `_archive/` |
