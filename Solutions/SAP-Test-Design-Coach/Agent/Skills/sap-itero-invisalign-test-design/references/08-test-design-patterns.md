# Reusable test-design patterns

Patterns guide structure, sequence, variables, and checks. They never supply scenario-specific transactions, fields, mappings, values, or business rules.

## Existing document validation

Flow: open/display existing object → identify it → navigate → validate.

Ask only:

- What transaction is used?
- What exactly must be validated?
- Are validations header-level, line-level, or both?

Do not ask whether the object exists; existence is inherent in this pattern.

## Create and capture generated document

Flow: start from source object → create → save → capture generated identifier → reuse it.

The identifier must be declared, generated, explicitly captured, and consistently reused.

## Variable line-item validation

Use `{Line_Item}` or another confirmed stable key plus the business variable in Parameters, Test Data, Step, and Expected Result.

## Header plus line-item mixed validation

Separate header validations from line-level validations. Never treat one header scalar as varying by line or collapse multiple line values into a document scalar.

## Conditional validation

Define the condition and additional validation using variables. If applicability is unknown, request business clarification.

## State-transition validation

Flow: verify objectively defined starting state → perform action → verify objectively defined ending state.

## Blocked/unblocked flow

Check the trigger, perform the action only when applicable, and verify the resulting state. Never assume blocking always exists.

## Output/document verification

Flow: open business document → access output → select output type → preview → validate availability plus header/document and line content separately.

## Integration-created object validation

Flow: open the upstream-created object in SAP → validate transferred or mapped data.

Ask which object, which display transaction, which fields prove correct population, header or line level, stable line key, and conditional mappings. Do not validate transmission itself unless explicitly in scope.

## Navigation within items

When the tester confirms that SAP supports navigation between items from Item Details, prefer that sequence over repeated returns to Item Overview. Keep `{Line_Item}` explicit while navigating.

## No invented scope

Recognizing an integration-created Sales Order pattern permits structural guidance only. It does not establish fields, mappings, transactions, expected values, or scope.
