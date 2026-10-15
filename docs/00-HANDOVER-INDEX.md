# FlowFoundry Handover Package

**Package version:** 4.00  
**Baseline date:** 20 August 2026  
**Product:** FlowFoundry  
**Supervisory orchestrator:** ForgeMaster  
**Implementation status:** Functional first-page prototype  
**Live baseline:** localhost only (no external deployment configured)

This package is the authoritative handover for the exact current FlowFoundry first-page concept, source, and prototype. It replaces the Version 3 package and incorporates the final enterprise redesign, modern logo, Agent portraits, selection/unselection behavior, resizable action panel, and all current interaction refinements.

---

## 1. Package Contents

| Document | Purpose |
|---|---|
| [`../PRODUCT-OVERVIEW.md`](../PRODUCT-OVERVIEW.md) | Plain-language FlowFoundry purpose, user journey, value, current maturity, and presentation storyline |
| [`../FLOWFOUNDRY-COMPLETE-HANDOVER-v4.00.md`](../FLOWFOUNDRY-COMPLETE-HANDOVER-v4.00.md) | Consolidated complete handover for direct reading or upload |
| [01-PRODUCT-ARCHITECTURE.md](01-PRODUCT-ARCHITECTURE.md) | Product purpose, ForgeMaster control model, workflow types, capacity model, History, and locked decisions |
| [02-UX-INTERACTION-SPECIFICATION.md](02-UX-INTERACTION-SPECIFICATION.md) | Current first-page behavior, WFG/GO, reset, actions, Agent selection, and responsive interaction rules |
| [03-DESIGN-SYSTEM-AND-CONTENT.md](03-DESIGN-SYSTEM-AND-CONTENT.md) | Enterprise visual direction, typography, colour, layout, icons, and approved interface language |
| [04-TECHNICAL-HANDOVER.md](04-TECHNICAL-HANDOVER.md) | Application structure, current implementation, local setup, build, known prototype boundaries, and deployment model |
| [05-TEST-AND-ACCEPTANCE.md](05-TEST-AND-ACCEPTANCE.md) | Acceptance criteria, manual checks, accessibility expectations, and release checklist |
| [06-DECISION-LOG-AND-CHANGE-HISTORY.md](06-DECISION-LOG-AND-CHANGE-HISTORY.md) | Naming changes, design iterations, behavior changes, and decision provenance |
| [07-GITHUB-AND-DEPLOYMENT-GUIDE.md](07-GITHUB-AND-DEPLOYMENT-GUIDE.md) | Safe upload to GitHub, repository hygiene, local commands, and later deployment options |
| [08-BACKLOG-AND-OPEN-QUESTIONS.md](08-BACKLOG-AND-OPEN-QUESTIONS.md) | Unimplemented screens, unresolved product rules, technical work, and recommended next sequence |
| [09-CLAUDE-CODE-CONTINUATION.md](09-CLAUDE-CODE-CONTINUATION.md) | Exact VS Code setup, Claude Code starting prompt, source ownership, reproduction rules, and common mistakes |
| [10-EXACT-BASELINE-INVENTORY.md](10-EXACT-BASELINE-INVENTORY.md) | Frozen technology, asset, source-tree, and reproduction inventory |
| [`../CLAUDE.md`](../CLAUDE.md) | Automatic repository-level guidance for Claude Code |

---

## 2. Authority and Interpretation

The documents distinguish among:

- **Locked product decisions:** agreed concepts that should not be changed accidentally.
- **Current prototype behavior:** what the code demonstrates today.
- **Design direction:** the approved first-page visual and interaction baseline.
- **Open decisions:** important matters that still require deliberate product design.
- **Implementation placeholders:** visible controls or sample data that are not production services.

When a conflict exists, use this order:

1. Explicit locked decisions in the product architecture.
2. The UX interaction specification.
3. The exact baseline inventory and current source code.
4. Older Version 1, Version 2, or Version 3 handovers.

---

## 3. Current Baseline in One Paragraph

FlowFoundry is an enterprise workspace in which a user describes a desired outcome, optionally selects several actions and a preferred specialist Agent, and then lets ForgeMaster determine and supervise the appropriate execution flow. ForgeMaster is the persistent control plane: it performs initial triage, observes throughout the session, receives escalations, manages Agent participation, and replans when needed. WFG is a real execution hold; GO releases the request and automatically turns WFG off. History represents the user’s overall session, not separate entries for every internal Agent.

---

## 4. Delivery Artifacts

The Version 4 delivery includes:

- the GitHub-ready source archive;
- the documentation archive;
- the combined handover archive;
- the live private Site URL;
- the Git commit identifying the frozen baseline;
- SHA-256 checksums;
- an independent extracted-package validation record;
- a ready-to-paste Claude Code continuation prompt.

Generated dependencies, local caches, temporary packaging files, and deployment build output are intentionally excluded from the source archive.

---

## 5. Recommended Reading Order

1. Product Architecture
2. UX Interaction Specification
3. Claude Code and VS Code Continuation Guide
4. Technical Handover
5. Test and Acceptance
6. Exact Baseline Inventory
7. Backlog and Open Questions

The design system and decision log can be consulted whenever visual or historical context is needed.
