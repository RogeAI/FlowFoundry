# Test Data and variable rules

## Variables-only rule

Authored test cases use variables only. Do not ask for or hard-code actual Sales Order numbers, line numbers, Materials, Item Categories, pricing conditions, statuses, or other runtime values. The tester supplies actual values only during execution.

## Parameters declaration rule

Every variable appearing anywhere in the test case must be declared and described in Parameters, including variables used in:

- Steps;
- Test Data;
- Expected Results;
- header-level validations;
- line-level validations;
- conditional logic;
- generated identifiers.

Example:

| Parameter | Meaning |
|---|---|
| `{Sales_Order_Number}` | Existing Sales Order under test |
| `{Line_Item}` | Confirmed stable SAP line-item identifier |
| `{Material}` | Expected Material for the applicable line item |
| `{Item_Category}` | Expected Item Category for the applicable line item |
| `{Alternative_SO}` | Expected header-level Alternative SO value |

## Line-level Test Data

Use variables, including the stable matching variable:

| Line_Item | Material |
|---|---|
| `{Line_Item}` | `{Material}` |

Both variables must also appear in the Step and Expected Result.

## Stable matching rule

Line-level validation requires a confirmed stable identifier. Prefer `{Line_Item}` when confirmed. If no stable key is known, ask; do not guess.

Mandatory Step:

> For every applicable line item, select `{Line_Item}` and verify that Material equals `{Material}`.

Mandatory Expected Result:

> For every applicable line item, `{Line_Item}` displays Material = `{Material}`.

## Independent Test Data structures

Use one Test Data structure per independent validation rule—Material, Item Category, Plant, and similar fields get separate structures unless they truly form one inseparable business rule. Avoid giant tables assembled merely for convenience.

## Header values

Do not force header variables into line-level tables. Example:

- Step: Navigate to Header Details → Additional Data B and verify Alternative SO equals `{Alternative_SO}`.
- Test Data: `{Alternative_SO}`
- Expected Result: Alternative SO = `{Alternative_SO}`.

## Generated identifiers

For a variable such as `{Billing_Document_Number}`:

1. declare it in Parameters;
2. generate it in an execution step;
3. explicitly capture it;
4. consistently reuse the same variable later.

## Conditional variables

Conditions remain variable-driven, for example:

> If `{Product_Hierarchy}` meets `{Trigger_Product_Hierarchy}`, open Profitability Segment.

Do not invent the trigger's runtime value during authoring.
