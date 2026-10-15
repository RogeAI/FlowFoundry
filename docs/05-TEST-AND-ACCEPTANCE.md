# FlowFoundry Test and Acceptance Guide

**Version:** 4.00  
**Scope:** Current first-page prototype

---

## 1. Release Acceptance Summary

A release is acceptable when:

- the production build succeeds;
- automated smoke tests pass;
- the root page renders FlowFoundry metadata and primary content;
- all agreed prototype interactions behave correctly;
- the page remains readable at 100% zoom;
- responsive layouts do not create blocking overflow;
- no secrets, caches, generated dependencies, or temporary packages are included in the source archive.

---

## 2. Automated Checks

Run:

```bash
npm test
```

Expected automated coverage:

- worker returns HTML with status 200;
- page title identifies FlowFoundry;
- rendered content contains ForgeMaster and the main workflow label;
- current metadata does not contain the starter preview marker;
- build output contains the server entry point.

---

## 3. Prompt and Action Acceptance

| ID | Scenario | Expected result |
|---|---|---|
| UX-001 | Enter prompt text | Text remains visible in the composer |
| UX-002 | Select one action | Action receives selected state, count becomes 1, and a chip appears under the prompt |
| UX-003 | Select several actions | All selected states and chips appear; count matches total |
| UX-004 | Remove an action using its chip | Action deselects in the panel and the count decreases |
| UX-005 | Select actions in different orders | UI preserves selection, but no execution-order claim is made |
| UX-006 | Expand composer | Actions panel hides and prompt area becomes larger |
| UX-007 | Reduce composer | Side-by-side composer and actions return with state preserved |
| UX-008 | Inspect action header | Available count is 6 and selected count matches current selection |
| UX-009 | Drag desktop action-panel resize handle | Panel height changes while the composer/actions relationship remains intact |

---

## 4. WFG Acceptance

| ID | Scenario | Expected result |
|---|---|---|
| WFG-001 | Activate WFG | Active styling and waiting message appear; submission label becomes GO |
| WFG-002 | Press GO | WFG turns off automatically and waiting message disappears |
| WFG-003 | Toggle WFG off manually | Default submission label returns |
| WFG-004 | Reset while WFG is active | After confirmation, WFG is off |

The prototype does not yet validate execution or navigation after GO.

---

## 5. Agent Acceptance

| ID | Scenario | Expected result |
|---|---|---|
| AG-001 | View Agent directory | Every Agent shows portrait, status, role, name, description, and control |
| AG-002 | Select Available Agent | Agent receives selected state and preference appears under prompt |
| AG-003 | Select another Available Agent | New Agent replaces the previous preference |
| AG-004 | Remove preferred Agent | Preference disappears and no Agent remains selected |
| AG-005 | Attempt Busy selection | Control is disabled and no preference changes |
| AG-006 | Attempt Unavailable selection | Control is disabled and no preference changes |
| AG-007 | Inspect Agent control width | Control fits its text and does not stretch unnecessarily |
| AG-008 | Click ✓ Selected | Agent unselects, card returns to default, button returns to Select Agent, and preference disappears |

---

## 6. Reset Acceptance

| ID | Scenario | Expected result |
|---|---|---|
| RS-001 | Select Reset session | Confirmation appears |
| RS-002 | Cancel confirmation | All current state remains unchanged |
| RS-003 | Confirm reset | Prompt, actions, Agent preference, WFG, and expanded state clear |

---

## 7. Visual and Readability Acceptance

Check at 100% browser zoom:

- navigation labels are readable;
- introductory steps are readable;
- prompt and action labels are readable;
- Agent roles, names, descriptions, status, and buttons are readable;
- the availability legend is readable;
- selected and disabled states remain visually distinct;
- selected Agent cards have a clearly lavender surface and filled violet ✓ Selected control;
- the final logo is not cropped, stretched, blurred, or shown on an unintended background;
- the header logo column and sidebar grid align cleanly;
- the page uses a large desktop width without excessive empty margins;
- no element is enlarged to the point that the interface loses its compact enterprise character.
- the About page follows the established light enterprise visual system and uses existing FlowFoundry artwork without distortion;
- the About page explains the product in user-facing language and does not read as a technical framework description.

---

## 8. Responsive Acceptance

Recommended widths:

- Desktop: 1440 × 900 and a wider 1920-pixel viewport.
- Tablet: 768 × 1024.
- Mobile: 390 × 844.

Confirm:

- no horizontal document scrolling at supported widths;
- header content remains usable;
- guidance stacks correctly;
- composer and actions stack at medium width;
- Agent grid changes from three to two to one column;
- controls remain reachable and readable;
- hidden desktop navigation does not leave inaccessible critical session controls in a production implementation.
- the About hero, workflow illustration, steps, control overview, capability cards, and call to action stack without horizontal overflow.

### Home and workspace route acceptance

- `/` server-renders the About FlowFoundry page successfully.
- `/workspace` server-renders the workflow intake interface successfully.
- About is available from the start and working-session headers.
- Workspace and call-to-action links open `/workspace`; the About navigation returns to `/`.
- The page describes ForgeMaster as the persistent coordinator and supervisor, not a selectable specialist.
- Wait for GO is described as an execution hold controlled by the user.

---

## 9. Accessibility Checklist

- All interactive elements are keyboard reachable.
- Focus is visible.
- Pressed states are programmatically exposed.
- Disabled controls are programmatically disabled.
- Text and status contrast meet the selected accessibility target.
- Icon-only buttons have accessible names.
- Selected-action removal is understandable to screen-reader users.
- WFG changes are announced in a production implementation.
- Confirmation is keyboard and screen-reader accessible.
- Touch targets are sufficiently large.

---

## 10. Packaging Acceptance

The GitHub-ready archive must include:

- source code;
- package manifest and lockfiles;
- public assets;
- tests;
- documentation;
- `CLAUDE.md` and the Claude Code continuation guide;
- `.gitignore`;
- `vite.config.ts` and build configuration.

It must exclude:

- `.git/`;
- `node_modules/`;
- `.next/`;
- `.vinext/`;
- `.wrangler/`;
- `dist/`;
- `work/`;
- temporary credentials;
- local environment files;
- packaging archives.
