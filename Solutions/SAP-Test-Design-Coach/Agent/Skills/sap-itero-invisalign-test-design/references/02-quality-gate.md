# Quality Gate

## Gate results

Return exactly one primary result:

- **Ready** — the reusable, variable-driven test design is structurally and logically complete.
- **Needs correction** — the business scenario is sufficiently understood, but correctable design, writing, structure, or sequence problems remain.
- **Clarification required** — missing business knowledge affects part or all of the design.
- **Not testable yet** — supplied information does not define a meaningful, objective test condition.

## Four mandatory dimensions

1. **Testability** — intent, scope, expected behavior, conditions, and observable outcomes are sufficiently defined.
2. **Test design** — Preconditions, Parameters, Test Data, steps, stable matching, generated identifiers, and header/line handling are sound.
3. **Test-case writing quality** — structure and wording are clear, concise, consistent, executable, and unambiguous.
4. **Execution sequence** — the test is logically ordered and navigationally efficient.

## Required checks

- Name states business object/process, scenario/action, and primary validation/outcome.
- Objective explains what the test proves.
- Preconditions are true before Step 1.
- Every variable used anywhere is declared and described in Parameters.
- Test cases and Test Data contain variables, never authored runtime values.
- Every line-level validation has a confirmed stable matching variable.
- Both Step and Expected Result explicitly name that stable variable and the business variable.
- Step, Test Data, and Expected Result use consistent variables.
- Independent rules are separated into independently failing validation steps.
- Expected Results are objective and observable.
- Header and line fields are structurally separated.
- Navigation and execution order are workable and efficient.
- Conditional behavior is explicit and variable-driven.
- Generated identifiers are declared, generated, explicitly captured, and consistently reused.
- No unsupported business behavior or scope has been invented.

## Ready rule

A test is **Ready** even when actual execution values are not populated. Readiness assesses reusable test design. The tester supplies actual values only during execution.

## Ready response

Keep it short: state **Gate result: Ready** and confirm the material checks. Never create an artificial execution-data failure because runtime values are absent.
