# Skill: Testability Analysis

## Trigger and boundary

Use this skill **only when the user explicitly requests testability analysis**. Hermes assesses and prepares information; it does not automatically create complete test cases, detailed test steps, or execution scripts. Those require a separate explicit request.

## Status

- **Testable:** Enough information exists to design meaningful tests for the stated behavior.
- **Partially testable:** Some behavior can be tested, but material information is unclear or missing.
- **Not yet testable:** Critical information prevents reliable test design.

## Assessment

As relevant, assess expected behavior, conditions, inputs, results, business rules, acceptance criteria, alternatives, exceptions, dependencies, interfaces, data, roles/permissions, state/lifecycle behavior, constraints, external control, and observable validation points.

Classify material gaps precisely:

- behavior gap
- expected-result gap
- condition gap
- rule gap
- data gap
- dependency gap
- exception gap
- observability gap

Separate a **test-design blocker** (the tester cannot determine what to test or expect) from a **test-execution blocker** (the test can be designed but environment, access, deployment, dependency, or data prevents execution).

Classify an execution issue as a confirmed blocker only when evidence establishes that it is unavailable or prevents execution. If availability is merely not specified, list it as a potential execution prerequisite requiring confirmation.

## Defensive rules

- Flag ambiguous language only when it permits materially different expected results.
- Never choose between conflicting requirements without evidence of precedence.
- Never invent expected values.
- Separate test-design variables from execution values. Missing concrete data does not prevent design when valid placeholders such as `{Customer_ID}` or `{Expected_Status}` can be defined.
- Assess alternative and error behavior only when material to the function.
- Poor writing does not automatically mean poor testability.
- Missing information is a testability gap only when it affects the ability to determine or verify expected behavior.

## Suggested output

Adaptively include: overall status, what can be tested, what cannot yet be reliably tested, classified gaps, design blockers, execution blockers, focused clarification questions, candidate test conditions, and useful recommendations.

