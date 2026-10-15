# Skill: Test Design Handover

## Trigger and purpose

Use only when the user explicitly asks for testability analysis **for downstream test design**, preparation for a test-case agent, or a Test Design Handover. Produce an intentionally detailed, operational handover so the downstream specialist does not need to rediscover the source analysis.

Hermes analyzes, validates, structures, and prepares. The downstream agent performs guided test design or creates test cases.

## Required handover content

Include applicable sections and explicitly mark material unknowns:

1. Handover purpose
2. Scope analyzed and sources
3. Overall testability status
4. Verified functional behavior
5. Business rules
6. Conditions and preconditions
7. Expected outcomes
8. Data requirements and variables
9. Roles and permissions
10. Interfaces and dependencies
11. State or lifecycle behavior
12. Alternate, negative, and exception behavior
13. Observable validation points
14. Candidate test conditions
15. Known test-design risks
16. Contradictions
17. Unresolved questions
18. Missing information
19. Test-design blockers
20. Test-execution blockers
21. Explicit assumptions, if any
22. Information that must not be assumed
23. Recommended clarification questions
24. Test-design readiness conclusion

## Handover rules

- Preserve evidence classifications and useful source provenance.
- Preserve variables instead of fabricating runtime values, and define what each variable represents.
- Do not silently repair gaps, resolve contradictions, or turn proposals into requirements.
- Candidate conditions are not complete test cases.
- Make blockers and their impact explicit.
- Classify an execution issue as a confirmed blocker only when evidence establishes that it is unavailable or prevents execution. Treat unspecified environment, access, data, credentials, interfaces, controls, and observability as potential execution prerequisites requiring confirmation.
- Ensure the handover is detailed enough for another agent, even when a human-facing summary would be shorter.

End with this downstream instruction, adapted only as needed for the task:

> Use only verified information in this handover and additional information supplied by the tester. Do not invent missing business rules, expected values, system behavior, or execution data. Where information remains unresolved, ask focused questions before creating the affected test design.

