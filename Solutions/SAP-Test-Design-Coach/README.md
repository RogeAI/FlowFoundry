# SAP - iTero - Invisalign - Test Design Coach and Quality Gate

GitHub-ready agent package for coaching, incrementally building, and quality-gating reusable SAP, iTero, and Invisalign test cases.

## Package structure

```text
.github/
├── agents/
│   └── sap-itero-invisalign-test-design-coach.agent.md
└── skills/
    └── sap-itero-invisalign-test-design/
        ├── SKILL.md
        └── references/
            ├── 01-mission-and-boundaries.md
            ├── 02-quality-gate.md
            ├── 03-guided-creation.md
            ├── 04-review-sequence.md
            ├── 05-test-case-writing-standard.md
            ├── 06-test-data-and-variables.md
            ├── 07-clarification-and-stop-rules.md
            ├── 08-test-design-patterns.md
            └── 09-correction-and-reporting.md
```

The `docx/` directory contains a complete Word version of every Markdown document, plus a consolidated handbook:

- `SAP-iTero-Invisalign-Test-Design-Coach-Complete-Package.docx`

The modular DOCX files mirror the Markdown package components so they can be reviewed, shared, or maintained independently.

## Non-negotiable rules

- Authored test cases contain variables only. Testers supply actual values only during execution.
- Every variable used anywhere in a test case, including every line-level variable, is declared and described in **Parameters**.
- Every line-level Step and its Expected Result explicitly reference the confirmed stable matching variable, such as `{Line_Item}`.
- Every finding identifies an exact location.
- The agent corrects test-design and writing problems, but never invents missing business knowledge.
- A test is **Ready** without populated execution values when its reusable variable-driven design is complete.

## Installation

Copy the package's `.github` directory into the root of the target repository and commit the files. Select the custom agent in GitHub Copilot when performing test-design work.

## Scope

This package contains the agreed behavioral and test-design standard. Scenario-specific business sources and approved examples may be added separately; they must not override the non-negotiable rules above.
