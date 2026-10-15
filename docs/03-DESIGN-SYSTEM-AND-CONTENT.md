# FlowFoundry Design System and Content Guide

**Version:** 4.00  
**Status:** Approved first-page visual direction

---

## 1. Design Character

FlowFoundry should feel like a mature enterprise application: clear, restrained, trustworthy, information-dense, and easy to scan. It should not resemble a generic marketing page, a collection of decorative cards, or a hobby project.

The approved direction combines:

- a white enterprise navigation header;
- the modern purple/navy FlowFoundry convergence logo;
- light white and pale grey/lavender working surfaces;
- thin borders and subtle shadows;
- controlled rounding;
- compact but readable controls;
- violet used for primary action and selection;
- deep navy for primary typography;
- restrained copper as a small brand accent;
- colour used primarily for state and emphasis.

---

## 2. Brand Elements

### 2.1 Name

Use **FLOWFOUNDRY** or **FlowFoundry** according to context.

---

### 2.2 Tagline

> Forge the right flow.

---

### 2.3 ForgeMaster

ForgeMaster is written as one word with capital F and M.

---

### 2.4 Application Logo

The approved application logo is `public/flowfoundry-logo-modern-v1.png`.

- Native dimensions: `2095 × 677`.
- Format: transparent PNG.
- Structure: converging purple/navy paths, a small copper coordination point, purple `FLOW`, and navy `FOUNDRY`.
- Header rendering: maximum 220-pixel width with the native aspect ratio preserved.
- It must not be cropped, stretched, placed on a dark rectangle, or rendered with `object-fit: cover`.

The coin, rustic metal plate, one-sided bronze-flow lockup, diamond-F treatment, and split orange/black wordmark are retired. `public/og.png` remains the social-sharing image and is not the active header logo.

---

## 3. Colour Roles

| Role | Current direction | Purpose |
|---|---|---|
| Violet | `#6651D8` family | Primary actions, active navigation, selected controls, `FLOW` |
| Deep navy | `#151A3A` family | Main typography and `FOUNDRY` |
| Copper | `#BD6E32` family | Small logo coordination accent only |
| Lavender | Pale purple | Canvas, selection, guidance, and Agent-card states |
| White | Neutral surface | Panels, cards, inputs |
| Cool grey | Background and borders | Structure without visual heaviness |
| Green | Available and operational | Positive system state |
| Amber | Busy and WFG waiting | Attention without failure |
| Red | Unavailable and destructive actions | Unavailability and Reset semantics |

Colour must never be the only carrier of meaning. Status text and disabled behavior remain necessary.

---

## 4. Typography

The interface uses a modern sans-serif presentation. The current implementation loads Geist through the application layout and provides common sans-serif fallbacks. Section headings use compact uppercase enterprise treatment; page and Agent titles remain highly readable rather than metadata-sized.

Typography hierarchy:

- page title: clear but not marketing-sized;
- section title: strong scan anchor;
- control label: readable and concise;
- body and description: comfortably readable at 100% zoom;
- metadata: smaller but never microscopic;
- uppercase role labels: limited to short Agent-role metadata.

Avoid extensive all-caps copy, tiny explanatory notes, and weak grey text.

---

## 5. Layout

### 5.1 Header

The logo occupies the 240-pixel desktop header column and aligns with the 240-pixel sidebar below. There is no unnecessary vertical divider after the logo; the header bottom line and sidebar boundary remain clean and aligned.

---

### 5.2 Navigation

The left navigation is compact and persistent on desktop. Session-level actions appear near the top. Recent work appears below the main navigation.

---

### 5.3 Main Workspace

The workspace has a generous but bounded maximum width. On large monitors it should use available space without becoming edge-to-edge or leaving a narrow miniature application floating in the centre.

---

### 5.4 Composer

The prompt and actions share one ForgeMaster panel. The prompt is wider because it is the primary task. The action panel is compact. Expansion is user-controlled.

---

### 5.5 Agent Directory

Agent cards use a consistent grid and equal visual structure. The action control fits its label. Descriptions remain readable and do not stretch unnecessarily.

---

## 6. Icons and Agent Identity

The current source uses a generated six-portrait sprite rather than initials or generic role glyphs:

- Axiom: top-left portrait;
- Verity: top-centre portrait;
- Atlas: top-right portrait;
- Loom: bottom-left portrait;
- Scribe: bottom-centre portrait;
- Sentinel: bottom-right portrait.

The portraits remain prototype identities. The future Agent identity system should provide:

- a consistent illustration or icon family;
- a distinct but coherent image for every Agent;
- accessible alternative names when images carry meaning;
- assets that work at card, compact status, and workflow-panel sizes;
- documented replacement rules so Agent identity is not coupled to business logic.

---

## 7. Component States

### 7.1 Selected Action

- visible border and tinted background;
- checked icon;
- selected count update;
- removable chip under the prompt.

---

### 7.2 WFG

- amber active treatment;
- explicit waiting message;
- GO submission label;
- automatic return to inactive after GO.

---

### 7.3 Agent Availability

- Available: green status and active selection control.
- Busy: amber status and disabled message.
- Unavailable: red status and disabled message.

---

### 7.4 Selected Agent

- lavender card surface;
- violet border and left indicator;
- filled violet control;
- white **✓ Selected** label;
- the selected control toggles back to the unselected state when clicked.

---

### 7.4 Destructive Action

Reset uses restrained red styling and requires confirmation. It must remain discoverable without competing with New workflow.

---

## 8. Approved Interface Language

| Element | Current wording |
|---|---|
| Page title | Start a new workflow |
| Prompt label | What would you like to achieve? |
| Prompt placeholder | Describe the outcome, problem, or question in your own words... |
| Action heading | Select actions |
| Action helper | Optional · choose one or more |
| WFG status | WFG active · waiting for GO |
| Default submission | Begin workflow |
| Held submission | GO |
| Agent section | Specialist Agents |
| Agent helper | Choose a preferred starting Agent, or let ForgeMaster decide. |
| Availability | Available / Busy / Unavailable |
| Reset | Reset session |

---

## 9. Content Principles

- Explain outcome and consequence, not implementation detail.
- Keep ForgeMaster’s supervisory role explicit.
- Never imply that action-selection order is execution order.
- Describe direct Agent selection as a preference.
- Use **Agent** with a capital A when referring to a FlowFoundry specialist role.
- Avoid invented production capabilities in prototype copy.
- Label placeholders honestly in technical documentation, even when the UI demonstrates the future experience.
