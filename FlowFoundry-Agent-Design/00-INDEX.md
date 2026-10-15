# FlowFoundry Agent Design — Master Index

This folder is the authoritative design workspace for all FlowFoundry agents.
It holds agent profiles, shared foundation definitions, and key decisions.

---

## Structure

```
FlowFoundry-Agent-Design/
  00-INDEX.md                          ← this file
  Foundation/
    Skills/                            ← shared skills inherited by all agents
    Tools/                             ← shared tools available to all agents
    Guardrails/                        ← shared guardrails applied to all agents
  Agents/                              ← individual agent profile documents
  Decisions/                           ← backlog items and key decisions
```

---

## Foundation (Shared — All Agents Inherit)

| File | Description | Status |
|------|-------------|--------|
| Foundation/Skills/ | Shared skill definitions | Empty — pending |
| Foundation/Tools/ | Shared tool definitions | Empty — pending |
| Foundation/Guardrails/ | Shared guardrail policies | Empty — pending |
| [Foundation/Contracts/FLOWFOUNDRY-AGENT-CONTRACT-v1.00.md](Foundation/Contracts/FLOWFOUNDRY-AGENT-CONTRACT-v1.00.md) | ForgeMaster ↔ specialist Agent message, lifecycle, validation, and authority contract | Approved baseline — SDK implementation started |

---

## Agents

| Agent | Role | Portrait | Status |
|-------|------|----------|--------|
| Athena | The Testing Mentor | `public/Athena.png` | Active — profile pending |
| Hermes | Information Intelligence Agent | `public/Hermes.png` | [Integration direction documented](Agents/HERMES-FLOWFOUNDRY-INTEGRATION-PLAN.md) — contract pending |
| Themis | Test Cases Creator | `public/Themis.png` | Active — profile pending |
| Minerva | Test Strategy Advisor | `public/Minerva.png` | Active — profile pending |
| Agent 5 | TBD | Placeholder | Phase 2 — grayed out |
| Agent 6 | TBD | Placeholder | Phase 2 — grayed out |

---

## Decisions & Backlog

| File | Description |
|------|-------------|
| [Decisions/session-2026-08-25-decisions.md](Decisions/session-2026-08-25-decisions.md) | All decisions made in the 25 Aug 2026 working session — keep updated |
| [Decisions/forgemaster-interaction-handover.md](Decisions/forgemaster-interaction-handover.md) | ForgeMaster first-page interaction model — confirmed decisions |
| [Decisions/checklist-forgemaster-response-screen.md](Decisions/checklist-forgemaster-response-screen.md) | Design and build the ForgeMaster Response Screen — Outcome A & B |
| [Decisions/checklist-agent-registry-migration.md](Decisions/checklist-agent-registry-migration.md) | Migrate agent data out of page.tsx into a registry |

## ForgeMaster Robot Images

All images created using AI image generation. Save to `public/` manually.

| Filename | Pose | Use |
|---|---|---|
| `forgemaster-garcon.png` | Working assistant | First-page ForgeMaster identity |
| `forgemaster-default.png` | Standard — holding hammer | Processing/thinking modal |
| `forgemaster-confused.png` | Questioning — hands up, "?" | Outcome B modal |
| `forgemaster-happy.png` | Thumbs up — smiling | Outcome A and completed-session states |
| `forgemaster-running.png` | Active execution | Working-session Running state |
| `forgemaster-investigating.png` | Investigating | Working-session user-attention state |

### Candidate transparent image set — 11 October 2026

The seven application-neutral robot images now have one canonical home in the
[shared White-Cyan Robot asset set](../../../Knowledge-Base/Visual-Assets/Characters/White-Cyan-Robot/README.md).
They remain candidate FlowFoundry replacements only. The current interface
still uses the active ForgeMaster images listed above, and the final
state-to-image mapping requires approval before integration.
