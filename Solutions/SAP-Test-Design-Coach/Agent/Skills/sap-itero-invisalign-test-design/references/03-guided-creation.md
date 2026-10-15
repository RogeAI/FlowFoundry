# Guided creation

## Interaction principles

- Do not ask everything at once.
- Ask one focused question or a small related group.
- Explain the design decision that depends on the answer.
- Author only what tester input or an approved source supports.
- Make progress on supported sections even when one local issue is blocked.

## Creation sequence

1. Understand the scenario: business object/process, whether it already exists or is created in the test, and the starting transaction/state.
2. Identify validation scope: fields/rules, header versus line level, and conditional validations.
3. Determine line handling: variable number of lines and confirmed stable matching key.
4. Define every required variable in Parameters; do not request execution values.
5. Build progressively: Name and Objective, Preconditions, Parameters, then one validation pattern at a time.
6. Assemble a full draft only when enough information is confirmed.
7. Apply the full Quality Gate before presenting any draft.

## Progressive response format

### Current understanding

List only confirmed facts and state relevant assumptions that are not being made.

### Proposed test-case section

Show only the section currently supported.

### Next clarification

Ask the smallest focused question that unlocks the next design decision.

## Example

### Current understanding

- Existing interface-created Sales Order.
- Start in VA03.
- `{Line_Item}` is the confirmed stable key.
- Validate line-level `{Material}` and header-level `{Alternative_SO}`.

### Proposed Parameters

- `{Sales_Order_Number}` — existing Sales Order under test.
- `{Line_Item}` — stable SAP line-item identifier.
- `{Material}` — expected Material for the applicable line.
- `{Alternative_SO}` — expected header value.

### Next clarification

Where is `{Material}` displayed in VA03? This determines the executable navigation for its validation step.
