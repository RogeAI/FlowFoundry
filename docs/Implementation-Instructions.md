# Implementation Instructions

Practical step-by-step guide for working with this repository daily.

---

## How to add a new solution

### Step 1 — Decide the solution name

Use title-case kebab: `My-Solution`, `Testing-Mentor`, `CAIRON`.

### Step 2 — Create the minimum structure

A brand-new solution needs only three things:

```text
Solutions/
└── My-Solution/
    ├── README.md
    └── manifest.yaml
```

Do not create `Agent/`, `Skills/`, or `Adapters/` until you have content to put in them.

### Step 3 — Write README.md

Cover at minimum:

- What problem this solves
- Who the intended users are
- Current maturity level
- How to use it

### Step 4 — Write manifest.yaml

Copy the template from `Solutions/Hermes/manifest.yaml` and update every field.

### Step 5 — Add platform content

If starting with Copilot:

```text
Solutions/
└── My-Solution/
    ├── README.md
    ├── manifest.yaml
    └── Adapters/
        └── Copilot/
            ├── README.md
            └── copilot-adapter.md
```

If starting with a full agent:

```text
Solutions/
└── My-Solution/
    ├── README.md
    ├── manifest.yaml
    └── Agent/
        └── AGENT.md
```

---

## How to add a skill to an existing solution

### Step 1 — Create the skill folder

Inside the solution's `Agent/Skills/`:

```text
Agent/Skills/my-new-skill/
```

### Step 2 — Create SKILL.md

Use this structure:

```markdown
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

### Step 3 — Register the skill in AGENT.md

Add a routing entry in the skill routing section of `Agent/AGENT.md`:

```markdown
- Use [Skill Name](Skills/my-new-skill/SKILL.md) when ...
```

### Step 4 — Add supporting folders only if needed

```text
Agent/Skills/my-new-skill/
├── SKILL.md
├── References/     ← only if the skill has its own reference material
├── Examples/       ← only if example inputs/outputs help clarity
└── Scripts/        ← only if automation supports the skill
```

---

## How to add an instruction file

Instructions live in `Agent/Instructions/` and apply on every task.

### Step 1 — Create the file

```text
Agent/Instructions/my-rule.md
```

Use kebab-case. Write the rule clearly — no template required.

### Step 2 — Reference it in AGENT.md

Add a line in the instructions section:

```markdown
Follow [my rule](Instructions/my-rule.md) on every task.
```

---

## How to create a platform adapter

### For GitHub Copilot

1. Create the folder:

```text
Solutions/My-Solution/Adapters/Copilot/
```

2. Create `copilot-adapter.md` — a self-contained file with all agent behavior inlined. GitHub Copilot does not load multiple files at runtime, so everything the agent needs must be in one file.

3. Create `README.md` explaining:
   - What the adapter is
   - How to deploy it
   - That it is a compiled snapshot of `Agent/` and must be updated when the canonical agent changes

### For Claude Code

1. Create the folder:

```text
Solutions/My-Solution/Adapters/Claude-Code/
```

2. Create `CLAUDE.md` pointing Claude Code to the canonical agent files.

### Rule for all adapters

The adapter delivers the agent to the platform. It never independently maintains its own version of skills or instructions. When `Agent/` changes, the adapter must be updated to match.

---

## How to promote an asset to Shared

Promote only after two independent solutions genuinely use the same asset.

### Step 1 — Confirm genuine reuse

Both solutions must actively use it, not just theoretically benefit from it.

### Step 2 — Move the asset

```bash
git mv Solutions/Solution-A/Agent/Skills/my-skill/ Shared/Skills/my-skill/
```

### Step 3 — Update both solutions to reference the shared location

In each solution's `AGENT.md`, update the skill path:

```markdown
- Use [Skill Name](../../../Shared/Skills/my-skill/SKILL.md) when ...
```

### Step 4 — Update both READMEs

Note that the skill is now shared and where it lives.

---

## How to migrate a solution to a new maturity level

Update `manifest.yaml`:

```yaml
maturity: validated   # was: experimental
version: 0.2.0        # bump version
```

Update `README.md` — change the maturity line under current maturity.

Maturity stages in order:

```
Concept → Experimental → Prototype → Validated → Production → Deprecated
```

---

## How to move an experiment into Solutions

An experiment becomes a solution when it has:

- A clear purpose worth maintaining
- At least a working `AGENT.md` or instruction file
- A README that explains what it does

Steps:

1. Create the solution folder under `Solutions/`.
2. Move the relevant files from `Experiments/` using `git mv`.
3. Write `README.md` and `manifest.yaml`.
4. Set maturity to `Experimental` in the manifest.
5. Delete the experiment folder if now empty.

---

## Decision guide — where does a new file belong?

```
Is it part of one specific solution?
  Yes → Solutions/<Solution-Name>/

Is it reused by two or more solutions?
  Yes → Shared/

Is it an early trial or prototype?
  Yes → Experiments/

Is it study notes, courses, or reference reading?
  Yes → Learning/

Does it govern the entire repository?
  Yes → Docs/   or   .github/   or   .claude/

Is it a binary or superseded file?
  Yes → _archive/
```

---

## Common mistakes to avoid

| Mistake | Correct approach |
|---|---|
| Creating a new top-level folder for a platform (`Copilot/`, `Claude/`) | Put it in `Solutions/<Name>/Adapters/` |
| Duplicating an agent as a sibling folder per platform | One solution folder, multiple adapters inside it |
| Naming a folder `Governance/` | Use `Instructions/` |
| Putting `.docx` or `.zip` files in agent folders | Markdown only; binaries go in `_archive/` |
| Creating `Skills/` as a flat list of `.md` files | Each skill in its own subfolder with `SKILL.md` |
| Moving an asset to `Shared/` speculatively | Only after two solutions actively use it |
| Creating empty folders "for later" | Create folders only when content goes in them |
| Naming the agent file `AGENT_INSTRUCTIONS.md` | Always `AGENT.md` |

---

## Checklist for a new solution

- [ ] Folder created under `Solutions/` with correct title-case kebab name
- [ ] `README.md` written — purpose, users, maturity, how to use
- [ ] `manifest.yaml` created and all fields filled in
- [ ] `AGENT.md` created if the solution has routing logic
- [ ] `Instructions/` created if behavioral rules are split out
- [ ] Each skill in its own `Skills/skill-name/SKILL.md` folder
- [ ] Adapter created if deploying to a specific platform
- [ ] All file and folder names follow naming conventions
- [ ] No binary files in agent asset folders
- [ ] Internal links in `AGENT.md` verified to point to correct paths

---

## Checklist for updating an existing solution

- [ ] `manifest.yaml` version bumped
- [ ] `README.md` updated if capabilities, maturity, or architecture changed
- [ ] Any new skills registered in `AGENT.md` skill routing
- [ ] Adapter updated if canonical `Agent/` content changed
- [ ] Internal links checked after any file moves
