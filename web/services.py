from .domain_gateway import domain_gateway


def prepare_local_workflow(
    *,
    objective: str,
    actions: list[str],
    preferred_agent: str | None,
    wfg_active: bool = False,
) -> dict:
    """Prepare a local plan through the existing FlowFoundry domain use cases."""
    return domain_gateway.prepare_workflow(
        objective=objective,
        actions=actions,
        preferred_agent=preferred_agent,
        wfg_active=wfg_active,
    )


def get_agent_cards() -> list[dict]:
    """Return the safe UI projection of the Python-owned Agent Registry."""
    return domain_gateway.agent_cards()


def build_local_session() -> dict:
    """Return the Python-owned plan used by the supervised local session simulation."""
    return {
        "status": "running",
        "classification": "Local Django simulation — no real Agent or external API execution.",
        "minimum_state_ms": 3500,
        "steps": [
            {
                "id": "athena",
                "name": "Athena",
                "role": "The Testing Mentor",
                "portrait": "Athena.png",
                "output": "Requirements reviewed. Found 3 ambiguities and 2 missing acceptance criteria. Recommendations prepared.",
            },
            {
                "id": "themis",
                "name": "Themis",
                "role": "Test Cases Creator",
                "portrait": "Themis.png",
                "output": "Test coverage drafted across the confirmed requirements, ambiguities, and acceptance criteria.",
            },
            {
                "id": "hermes",
                "name": "Hermes",
                "role": "Information Intelligence Agent",
                "portrait": "Hermes.png",
                "output": "Summary report assembled. Five findings were consolidated into actionable recommendations with priority rankings.",
            },
        ],
        "attention": {
            "agent_id": "hermes",
            "agent_name": "Hermes",
            "question": "Hermes needs clarification before completing the Master Document: which audience and level of detail should the final summary use?",
        },
    }


def resolve_local_attention(*, response: str) -> dict:
    normalized_response = response.strip()
    if not normalized_response:
        return {"status": "clarification", "message": "Please provide the audience and level of detail before the workflow continues."}
    session = build_local_session()
    return {
        "status": "resumed",
        "acknowledgement": "Thank you. I passed your response to Hermes, and the workflow is continuing.",
        "completion_message": "All Agents have finished. Your workflow is complete.",
        "final_output": session["steps"][-1]["output"],
    }
