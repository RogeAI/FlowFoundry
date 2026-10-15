# Hermes

Platform-neutral information intelligence agent. Transforms fragmented, complex, or mixed material into accurate, structured, decision-useful intelligence — summarizing, connecting evidence, exposing uncertainty, and extracting decisions and actions without inventing facts.

## Purpose

Turn raw information into intelligence. Hermes works on documents, tickets, emails, notes, transcripts, screenshots, and structured data. It surfaces what matters, how facts connect, what conflicts, what is missing, and which decisions or actions deserve attention.

## Problem being solved

Information presented to AI is often messy, incomplete, fragmented, or spread across multiple sources. Generic AI responses flatten nuance, invent missing facts, or fail to distinguish what is known from what is assumed. Hermes applies rigorous evidence discipline and structured analytical skills to produce outputs that are accurate, appropriately qualified, and genuinely useful.

## Intended users

Software quality engineers, test architects, business analysts, and project leads who need to analyze and synthesize information from multiple sources as part of their daily work.

## Current maturity

Experimental — actively in use, stable core behavior, skills and governance rules established.

## Architecture

```text
Hermes/
├── Agent/
│   ├── AGENT.md              ← identity, routing, output behavior
│   ├── Instructions/         ← persistent behavioral rules
│   ├── Skills/               ← task-specific analytical capabilities
│   └── Tools/                ← tool integration principles
└── Adapters/
    └── Copilot/              ← archived historical configuration; not active
```

## Agent

`Agent/AGENT.md` is the primary instruction file. It defines Hermes's identity, non-negotiable behavior, skill routing, output behavior, and personality.

## Instructions

Persistent rules that apply on every task, regardless of which skill is active:

| File | Responsibility |
|---|---|
| `evidence-discipline.md` | Evidence classifications and operating rules |
| `input-handling.md` | How to accept and handle imperfect or mixed input |
| `final-quality-gate.md` | Pre-delivery verification checklist |

## Skills

Task-specific capabilities loaded as needed:

| Skill | When to use |
|---|---|
| `information-intelligence` | Synthesis, insights, gaps, decisions, risks, uncertainty |
| `source-analysis` | Multiple sources, versions, provenance, conflicts |
| `quality-assessment` | Reviewing clarity, completeness, fitness for purpose |
| `recommendations-actions` | Extracting commitments, proposing next steps |
| `testability-analysis` | Only when explicitly requested by the user |
| `test-design-handover` | Only when explicitly requested for downstream test design |

## Tools

`Agent/Tools/TOOLS.md` describes optional tool and integration behavior. Hermes works without tools when the user supplies material directly.

## Supported platforms

| Platform | Status | Location |
|---|---|---|
| FlowFoundry | Active integration | `backend/agents/hermes.py` and `backend/agent_sdk/` |
| Claude Code | Active development environment | Repository `CLAUDE.md` |
| GitHub Copilot | Retired | Historical files only under `Adapters/Copilot/` |
| Standalone | Possible | Use `Agent/AGENT.md` directly |

## Known limitations

- Hermes does not automatically create complete test cases; that requires explicit handover to a test-design agent.
- Tool behavior depends entirely on what the host environment provides.
- Testability analysis is dormant unless explicitly requested.

## Integration status

- Agent Contract v1.00 manifest registered in the Python backend
- Runtime adapter implemented with authorized source reading, hash verification,
  selective skill loading, structured model output, and validated Agent results
- Anthropic model gateway implemented with explicit environment configuration,
  prompt-injection separation, strict JSON parsing, and safe provider failures
- Internal ForgeMaster-controlled specialist dispatcher and lazy Hermes runtime
  registration implemented
- Session-isolated source ingestion and ForgeMaster workflow-to-AgentTask construction
  implemented, including a tested DOCX handoff to the Hermes runtime
- Browser intake and working-session file controls connected to the backend source,
  WFG, ForgeMaster begin-workflow, and safe result/error paths

## Roadmap

- Add durable metadata persistence, authentication, malware scanning, and retention policy
- Add live multi-step continuation, progress, clarification, and cancellation semantics
- Evaluation suite (happy path, negative, edge cases)
- Regression tests for instruction changes
