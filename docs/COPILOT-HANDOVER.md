# FlowFoundry → Copilot Studio: Handover & Cost Analysis Brief

**Purpose:** Give Copilot (or a Copilot Studio architect) enough context to evaluate whether FlowFoundry's agent-orchestration pattern can be rebuilt on Microsoft Copilot Studio, estimate costs, and identify gaps.

**Repository:** https://github.com/align-sap/sqa-ai-enterprise-app-automation

---

## 1. What FlowFoundry Is

FlowFoundry is an enterprise AI-agent orchestration workspace. A user describes what they want done in natural language, optionally selects actions and a preferred specialist agent, and a supervisory orchestrator called **ForgeMaster** triages, plans, and delegates execution to one or more specialist agents.

### Core Flow

```
User writes objective
  → selects actions (multi-select, optional)
  → picks preferred agent (optional, max 1)
  → toggles WFG (Wait for GO) if they want to review before execution
  → presses GO

ForgeMaster receives everything
  → triages the request
  → decides workflow type (single agent, chained, parallel, mixed, or self-only)
  → assigns agents and step order
  → supervises execution
  → returns result to user
```

### Key Rules

| Rule | Detail |
|---|---|
| ForgeMaster always triages | Even when the user picks a preferred agent, ForgeMaster decides whether to use it |
| WFG / GO | WFG holds execution; GO releases it and auto-deactivates WFG |
| Agent states | Available (selectable), Busy (visible but disabled), Unavailable (visible but disabled) |
| Actions | Multi-select; selection order ≠ execution order — ForgeMaster decides |
| History | One user objective = one History entry; agent steps nest inside it |
| One preferred agent | Only one can be selected; clicking "Selected" unselects it |

---

## 2. Architecture (Current)

```
┌─────────────────────────────────────────────────┐
│  Browser — React/TypeScript (vinext, port 3000)  │
│  Routes: / (about), /workspace, /session         │
└──────────────────┬──────────────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────────────┐
│  Python FastAPI backend (port 8000)              │
│                                                  │
│  ForgeMasterService  ──→  Claude Opus 5          │
│       ↓                   (Anthropic API)        │
│  RuntimeRegistry                                 │
│       ↓                                          │
│  HermesRuntime  ────→  Claude Opus 5             │
│  (+ future agents)      (Anthropic API)          │
└──────────────────────────────────────────────────┘
```

### What Each Component Does

| Component | Role | Current Implementation |
|---|---|---|
| **ForgeMaster** | Supervisory orchestrator — triages every request, decides workflow type, assigns agents | Python service calling Claude Opus 5 with a system prompt; returns a structured `WorkflowPlan` (JSON) |
| **RuntimeRegistry** | Maps agent IDs to runtime adapters | In-memory Python dict; currently only `hermes` → `AnthropicHermesGateway` |
| **Hermes** | Information-intelligence specialist — transforms raw information into structured analysis | Full agent spec with 6 skills, 7 rules, evidence classification system |
| **Other agents** | Axiom, Verity, Atlas, Loom, Scribe, Sentinel | Defined in UI with portraits; backend runtimes not yet wired |
| **Frontend** | Workspace UI — prompt composer, action selector, agent cards, session view | React/TypeScript, functional today |

### Adapter Pattern (Already Designed)

The Hermes agent already has a **Copilot adapter specification** at `Solutions/Hermes/Adapters/Copilot/`. This means the agent's skills, rules, and behavior have been translated into a format intended for GitHub Copilot. The same pattern applies to any orchestration platform.

---

## 3. What Copilot Studio Needs to Replace

### ForgeMaster (the orchestrator)

ForgeMaster currently sends this to Claude Opus 5:
- A system prompt defining its role and available agents
- The user's objective, selected actions, preferred agent, and WFG state
- It expects back a JSON plan: workflow type, step sequence, agent assignments, summary

**Copilot Studio equivalent:** A **primary orchestrator agent** that receives user input, reasons about which topic/agent to route to, and manages the conversation flow. Copilot Studio's built-in topic routing and multi-agent orchestration could handle this, but the triage logic (deciding between single, chained, parallel, or mixed workflows) would need to be expressed as agent instructions or a plugin.

### Specialist Agents

Each specialist is a scoped worker with:
- A defined mission and boundaries
- Skills (information-intelligence, source-analysis, quality-assessment, etc.)
- Rules (never invent facts, classify evidence, escalate when out of scope)
- Tools (search, document access, etc.)

**Copilot Studio equivalent:** Individual **Copilot agents** or **plugins**, each with their own instructions, knowledge sources, and actions. Hermes's 6 skills map to agent topics or separate agents.

### WFG / GO (Human-in-the-loop)

WFG holds execution until the user explicitly releases it.

**Copilot Studio equivalent:** Built-in — Copilot Studio supports human-in-the-loop approval steps, adaptive cards with confirm/cancel, and Power Automate approval flows.

---

## 4. Cost Comparison — What Copilot Needs to Evaluate

### Current Cost Model (Claude / Anthropic API)

Every interaction = token-based billing:

| Call | Model | Estimated Tokens | Approx. Cost per Call |
|---|---|---|---|
| ForgeMaster triage | Claude Opus 5 | ~2,000 in + ~500 out | ~$0.04–$0.08 |
| Specialist execution (e.g., Hermes) | Claude Opus 5 | ~3,000 in + ~2,000 out | ~$0.12–$0.25 |
| **Typical single interaction** | | | **~$0.15–$0.35** |

At scale:
- 10 users × 20 interactions/day = 200 calls/day
- **~$30–$70/day → $600–$1,400/month** (API costs alone, no infrastructure)
- Adding parallel/chained workflows multiplies specialist calls

*Note: These are estimates based on published Anthropic pricing. Actual costs depend on prompt length, response length, and caching.*

### Copilot Studio Cost Model

Align likely already has Microsoft 365 E3/E5 licenses. The cost question for Copilot Studio is:

| Item | Question for Copilot to Answer |
|---|---|
| **Copilot Studio licensing** | Is Copilot Studio included in Align's current M365/Copilot licensing, or does it require additional per-user or per-tenant licensing? |
| **Message consumption** | Copilot Studio charges per "message" — how many messages does a ForgeMaster triage + specialist execution consume? |
| **AI Builder credits** | If using GPT-4o or custom AI models via Copilot Studio, are AI Builder credits needed? How many per interaction? |
| **Power Automate** | If WFG/GO uses Power Automate approvals, is that covered or additional? |
| **Connectors / premium actions** | Accessing external data (SharePoint, DevOps, SAP) — premium connector costs? |
| **Breakeven point** | At what usage level does Copilot Studio become cheaper than per-token API billing? |

### The Core Cost Argument

| Factor | Anthropic API | Copilot Studio |
|---|---|---|
| Per-interaction cost | $0.15–$0.35+ per call | Potentially covered by existing licensing |
| Scales with usage | Linear — more users = more cost | Flat or stepped (licensing-based) |
| Infrastructure | Self-hosted backend (FastAPI) | Microsoft-managed |
| Security / compliance | External API, key management | Inside Microsoft tenant |
| Model quality | Claude Opus 5 (top-tier reasoning) | GPT-4o (very capable, different strengths) |
| Customization | Full control | Within Copilot Studio framework |

---

## 5. What to Ask Copilot

When presenting this to Copilot or a Copilot Studio architect, ask:

1. **Can Copilot Studio's multi-agent orchestration replicate ForgeMaster's triage pattern?** (Receive objective → reason about workflow type → assign agents → supervise)

2. **What is the real cost per interaction** for an orchestrator agent that calls 1–3 specialist agents per user request, given Align's current licensing?

3. **Can Copilot agents enforce FlowFoundry's rules?** (Evidence classification, never-invent-facts, escalation-on-uncertainty, structured JSON output)

4. **What's the integration path for SAP, DevOps, and SharePoint data** that FlowFoundry's specialist agents would need?

5. **Is the model quality sufficient?** ForgeMaster needs to reason about ambiguous requests and produce structured execution plans. Hermes needs to classify evidence and detect contradictions. Can GPT-4o handle this reliably?

6. **What's the migration effort?** FlowFoundry has a working frontend, 6 agent specifications, and an adapter pattern. What reuse is possible vs. what must be rebuilt?

---

## 6. Repository Map (What to Look At)

| Path | What's There |
|---|---|
| `docs/01-PRODUCT-ARCHITECTURE.md` | Full product spec, locked decisions, workflow types |
| `docs/02-UX-INTERACTION-SPECIFICATION.md` | UI behavior, states, responsive layout |
| `Solutions/Hermes/Agent/AGENT.md` | Complete Hermes agent spec (skills, rules, tools) |
| `Solutions/Hermes/Adapters/Copilot/` | Hermes adapted for Copilot (proof the pattern works) |
| `backend/domain/services/forge_master.py` | ForgeMaster triage logic and prompt |
| `backend/infrastructure/runtime_registry.py` | How agents are registered and dispatched |
| `backend/agents/hermes.py` | Hermes runtime wiring |
| `app/workspace/page.tsx` | Workspace UI (agent cards, actions, composer) |
| `CLAUDE.md` | Development rules and constraints |

---

*Document version: 2026-09-06. Source: FlowFoundry v4.00 baseline.*
