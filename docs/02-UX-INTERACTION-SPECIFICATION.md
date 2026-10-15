# FlowFoundry UX and Interaction Specification

**Version:** 4.00  
**Status:** Current first-page behavior

---

## 1. Experience Goal

The first page must help users begin without knowing the internal Agent architecture. It should answer four questions quickly:

1. What result do I want?
2. Which optional actions are useful?
3. What supporting context should I provide?
4. Do I want ForgeMaster to choose everything, or do I have a preferred Agent?

---

## 2. Header

The header contains:

- the modern FlowFoundry convergence logo without a tagline;
- Workspace, Activity, Agents, Governance, and About navigation labels;
- search and help controls;
- the current workspace-user area.

The FlowFoundry brand, Workspace selection, and About page are meaningful in the prototype. Activity, Agents, Governance, search, help, and user controls remain visual placeholders for future routes and functionality.

### 2.1 About FlowFoundry

The About page is the home route (`/`) and the first experience for new visitors. It provides a user-friendly product overview rather than a technical framework explanation. It explains the outcome-led journey, ForgeMaster coordination, specialist participation, visible workflow progress, WFG, and user oversight. It uses existing FlowFoundry and Agent artwork, remains responsive, and provides clear routes to the working interface at `/workspace`.

---

## 3. Left Navigation

The persistent desktop navigation contains:

- New workflow;
- Reset session;
- Start;
- History;
- Saved;
- recent-session examples;
- enterprise-workspace status.

Reset is intentionally near New workflow because it is a session-level action. On smaller screens, the current prototype hides the side navigation; a production mobile navigation pattern remains to be designed.

---

## 4. Introductory Guidance

The page introduction describes ForgeMaster’s role and presents four concise steps:

1. Describe the outcome.
2. Select useful actions.
3. Add supporting context.
4. Let ForgeMaster lead.

The guidance must remain informative but compact. It should not become decorative filler.

---

## 5. ForgeMaster Composer

### 5.1 Default Layout

The composer and Select actions panel sit side by side on wide screens. This keeps the connected choices close together without stretching the writing area across the entire viewport.

---

### 5.2 Prompt

The prompt accepts the user’s natural-language objective. The current placeholder is:

> Describe the outcome, problem, or question in your own words...

---

### 5.3 Expand and Reduce

The user can expand the prompt area when more writing space is needed. In expanded mode:

- the composer takes the full panel width;
- the prompt becomes taller;
- the actions panel is temporarily hidden;
- selected actions remain retained.

Reducing the composer restores the side-by-side layout.

---

### 5.4 Attach Context

Attach context opens the operating-system file picker and accepts multiple files. Selected `filename.extension` values appear as removable chips in the composer footer. The working-session Attach context control remains available in every workflow state and uses the same multi-file selection and removal pattern.

Files selected on the first page carry into the working-session route. Files added later from the ForgeMaster panel join the same workflow-level collection. The working-session page presents the complete collection only in a **Workflow Files** panel between the Workflow Plan and ForgeMaster Live Feed. The right ForgeMaster panel provides the Attach context action but does not duplicate the file list. Removing a file from Workflow Files updates the shared collection.

Selected `File` objects remain in shared browser memory during client-side navigation. When the local Python backend is available, submission copies validated files into a server-controlled per-session runtime directory and working-session additions use the same source endpoint. Refreshing the browser still clears the client-side list, source metadata is not durably persisted, and malware scanning, authentication, retention, and production storage are not implemented.

---

## 6. Action Selection

Actions are optional and multi-select. The current sample set is:

- Summarize;
- Review requirements;
- Create testable scenarios;
- Design test cases;
- Identify gaps;
- Compare documents.

The panel header displays both the number of available actions and the number currently selected. When selected:

- the action receives a clear selected state in the right panel;
- the selected count updates;
- a removable confirmation chip appears beneath the prompt;
- selection order does not affect execution order.

ForgeMaster determines dependencies and ordering after submission.

On desktop, the action panel has a native bottom-right vertical resize handle. Resizing increases the panel height without moving the action catalogue into a separate full-width mode. At smaller breakpoints, manual resizing is disabled and responsive stacking controls the layout.

---

## 7. WFG and GO

### 7.1 Activating WFG

Selecting WFG:

- changes the WFG control to an active visual state;
- displays **WFG active · waiting for GO**;
- changes the main submission label to **GO**.

---

### 7.2 Pressing GO

Pressing GO:

- releases the held request;
- turns WFG off automatically;
- removes the waiting indicator;
- returns the WFG control to its inactive state.

With the configured Python backend, Begin workflow or GO submits the complete request to ForgeMaster and carries the initial plan and eligible specialist result into `/session`. The later working-session lifecycle, conversation, and multi-step continuation controls remain demonstration behavior.

### 7.3 Working-session state presentation

- **Running** uses the violet status treatment and `forgemaster-running.png` while an Agent is executing.
- **Investigating** uses the amber attention treatment and `forgemaster-investigating.png` when a question, action, or decision requires user input.
- The triggering Agent is marked **Input Required**, while already completed Agents remain complete and the progress count remains accurate.
- The right ForgeMaster panel opens and enables user input during an attention state.
- After the user responds, the affected Agent resumes and ForgeMaster returns to **Running**.
- **Complete** uses the green status treatment and `forgemaster-happy.png` only after all participating Agents finish.
- Completed Agent rows use larger portraits and readable identity/output text. Each Agent output presents a labeled **Download Files** control using the transparent `Download_Files.png` asset.
- On wide screens, the working-session layout gives the ForgeMaster panel moderately more horizontal space than the earlier narrow sidebar. The conversation area expands through the available height, while the reply controls and selected attachment filenames remain grouped at the bottom of the panel.
- The ForgeMaster reply field is a 90-pixel multi-line composer (1.5 times the earlier height); Enter sends and Shift+Enter adds a new line. The conversation area yields the required vertical space.
- Hovering any current or future Agent portrait in the working-session selector displays that Agent's name through the shared portrait tooltip pattern.

---

## 8. Specialist Agent Cards

Every Agent card displays:

- a distinct portrait sourced from the six-image Agent sprite;
- availability status;
- role label;
- Agent name;
- short capability description;
- a compact selection or status control.

Current sample Agents are Axiom, Verity, Atlas, Loom, Scribe, and Sentinel. Their identities and icons are placeholders and may change.

---

## 9. Agent Selection Rules

- Available Agents can be selected.
- Busy Agents are visible but disabled.
- Unavailable Agents are visible but disabled.
- Only one preferred Agent can be selected at a time.
- The selected preference appears beneath the prompt.
- Clicking the filled **✓ Selected** control unselects that Agent and returns selection to ForgeMaster.
- Removing the preference beneath the prompt produces the same result.
- A selected Agent remains subject to ForgeMaster validation.

The selected card uses a visibly lavender surface, violet border and left marker, plus a filled violet **✓ Selected** control. Buttons should fit their text rather than stretching across the card.

---

## 10. Reset Behavior

Selecting Reset session displays a confirmation dialog. Confirming clears:

- prompt;
- selected actions;
- preferred Agent;
- WFG;
- expanded prompt state.

Cancelling leaves all state unchanged.

---

## 11. Responsive Behavior

### 11.1 Large Desktop

- The content area expands to use available width without becoming edge-to-edge.
- The composer and actions remain side by side.
- Agent cards use three columns.
- Text remains readable at 100% browser zoom.

---

### 11.2 Medium Width

- Introductory steps use two columns.
- Composer and actions stack.
- Agent cards use two columns.
- The desktop side navigation remains until the tablet breakpoint.

---

### 11.3 Small Width

- Desktop navigation is hidden.
- Guidance uses one column.
- Composer controls stack when necessary.
- Actions and Agent cards use one column.
- Agent buttons may use available width for touch usability.

---

## 12. Readability Requirements

- The page must be comfortably readable at 100% browser zoom.
- Descriptions must not be treated as fine print.
- Status labels and legends must remain legible.
- The interface should be compact, not miniature.
- Large screens should not create excessive empty margins around undersized content.
- Increased size should improve comprehension, not create oversized marketing-page typography.

---

## 13. Accessibility Expectations

The current prototype includes semantic buttons, labels, pressed states, disabled states, and accessible names for key icon controls. Production work should additionally verify:

- full keyboard navigation;
- visible focus states;
- colour contrast;
- screen-reader announcements for selection changes and WFG state;
- confirmation-dialog accessibility;
- touch-target size;
- reduced-motion support if animation is introduced.
