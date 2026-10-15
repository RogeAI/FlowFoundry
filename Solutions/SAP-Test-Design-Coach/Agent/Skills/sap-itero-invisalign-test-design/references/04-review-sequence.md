# Fixed review sequence

Review in this order so fundamental problems are found before wording polish:

1. **Test intent and scope** — Name, Objective, testability, and coherent scope.
2. **Preconditions** — true before Step 1; no misplaced execution actions.
3. **Parameters** — every used variable declared; line, header, conditional, and generated variables included; names consistent.
4. **Test Data** — variable-only content, stable matching key, and correct step-level structure.
5. **Steps** — executable, clear, properly granular, explicitly variable-driven, and one independent validation per step.
6. **Expected Results** — objective pass/fail, variable-aligned, and stable key explicit for line-level validation.
7. **Writing quality** — section structure, concise wording, consistent phrasing, and no unnecessary sections.
8. **SAP navigation and execution flow** — correct mode/transaction as confirmed, logical sequence, efficient navigation, generated-ID lifecycle, conditional flow.
9. **Business ambiguity** — unknown facts, contradictions, unsupported assumptions, or unclear scope.
10. **Final gate result** — Ready, Needs correction, Clarification required, or Not testable yet.

Report findings in test-case order even though the diagnostic review follows the sequence above.
