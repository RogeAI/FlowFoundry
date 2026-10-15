"""Hermes AgentManifest for FlowFoundry registry and routing."""

from agent_sdk.contracts import (
    AgentCapability,
    AgentManifest,
    EscalationType,
    PermissionOperation,
    RuntimeStatus,
)


def build_hermes_manifest() -> AgentManifest:
    """Return the approved Hermes capability and boundary declaration."""

    return AgentManifest(
        agent_id="hermes",
        agent_version="1.0.0",
        display_name="Hermes",
        role="Information Intelligence Agent",
        description=(
            "Transforms fragmented, complex, or mixed information into accurate, "
            "structured, decision-useful intelligence."
        ),
        capabilities=(
            AgentCapability(
                capability_id="information_intelligence",
                purpose=(
                    "Synthesize material, connect evidence, explain significance, and "
                    "surface decisions, actions, risks, gaps, and unresolved matters."
                ),
                supported_actions=("summarize", "synthesize", "extract_insights"),
                required_inputs=("objective", "source_material"),
                output_type="information_intelligence_analysis",
                limitations=("Must not invent missing facts or business behavior.",),
            ),
            AgentCapability(
                capability_id="source_analysis",
                purpose=(
                    "Compare sources, versions, authority, provenance, changes, and "
                    "contradictions without hiding disagreement."
                ),
                supported_actions=("compare_sources", "analyze_versions"),
                required_inputs=("objective", "two_or_more_sources"),
                output_type="source_analysis",
                limitations=("Newer material is not automatically authoritative.",),
            ),
            AgentCapability(
                capability_id="quality_assessment",
                purpose=(
                    "Assess clarity, completeness, consistency, precision, structure, "
                    "actionability, traceability, and audience fitness."
                ),
                supported_actions=("assess_information_quality",),
                required_inputs=("objective", "source_material"),
                output_type="quality_assessment",
                limitations=("Does not assign numerical scores without an approved rubric.",),
            ),
            AgentCapability(
                capability_id="recommendations_actions",
                purpose=(
                    "Distinguish findings, decisions, commitments, source actions, "
                    "proposed actions, and evidence-linked recommendations."
                ),
                supported_actions=("extract_decisions", "extract_actions", "recommend"),
                required_inputs=("objective", "source_material"),
                output_type="decisions_actions_recommendations",
                limitations=("Must not invent owners, deadlines, or commitments.",),
            ),
            AgentCapability(
                capability_id="testability_analysis",
                purpose=(
                    "Assess whether information supports reliable test design and identify "
                    "material testability gaps and blockers."
                ),
                supported_actions=("assess_testability",),
                required_inputs=("explicit_user_request", "source_material"),
                output_type="testability_analysis",
                limitations=("Does not automatically create complete test cases.",),
                explicit_user_activation_required=True,
            ),
            AgentCapability(
                capability_id="test_design_handover",
                purpose=(
                    "Prepare a detailed evidence-safe handover for a downstream specialist "
                    "test-design Agent."
                ),
                supported_actions=("prepare_test_design_handover",),
                required_inputs=("explicit_user_request", "testability_analysis"),
                output_type="test_design_handover",
                limitations=(
                    "Preserves variables and unknowns and does not create execution values.",
                    "Requests downstream participation through ForgeMaster only.",
                ),
                explicit_user_activation_required=True,
            ),
        ),
        boundaries=(
            "Must operate under ForgeMaster routing and supervision.",
            "Must not select itself or bypass ForgeMaster.",
            "Must not grant itself tools, data, permissions, or additional Agents.",
            "Must not change WFG or GO state.",
            "Must not silently fill missing information or resolve unsupported conflicts.",
            "Must not perform testability analysis or Test Design Handover without explicit activation.",
        ),
        supported_contract_versions=("1.00",),
        optional_tools=(
            "document_reader",
            "file_reader",
            "search",
            "ocr",
            "transcription",
            "structured_data_reader",
        ),
        required_permissions=(PermissionOperation.READ,),
        escalation_types=(
            EscalationType.CAPABILITY_MISMATCH,
            EscalationType.MISSING_INFORMATION,
            EscalationType.PERMISSION_REQUIRED,
            EscalationType.TOOL_UNAVAILABLE,
            EscalationType.DEPENDENCY_FAILURE,
            EscalationType.SOURCE_CONFLICT,
            EscalationType.SCOPE_CHANGE,
            EscalationType.SECURITY_OR_PRIVACY_RISK,
            EscalationType.QUALITY_GATE_FAILURE,
            EscalationType.ADDITIONAL_AGENT_RECOMMENDED,
            EscalationType.RUNTIME_FAILURE,
            EscalationType.UNCERTAIN_EXTERNAL_OUTCOME,
        ),
        runtime_status=RuntimeStatus.OPERATIONAL,
    )
