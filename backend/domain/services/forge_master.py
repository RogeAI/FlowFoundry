import json
import os

import anthropic

from domain.entities.agent import Agent
from domain.entities.session import Session
from domain.entities.workflow import WorkflowPlan, WorkflowStep, WorkflowType, WorkflowStatus


TRIAGE_SYSTEM_PROMPT = """You are ForgeMaster, the supervisory orchestrator for FlowFoundry.

Your role:
- Perform initial triage on every user request
- Remain continuously supervising throughout the session
- Determine the optimal workflow type and Agent assignments
- You always supervise, even when the user pre-selects a preferred Agent

Available workflow types:
- ForgeMasterOnly: You handle it directly, no specialist needed
- SingleAgent: One specialist Agent is sufficient
- Chained: Multiple Agents in sequence, dependencies matter
- Parallel: Multiple Agents can work simultaneously
- Mixed: Combination of sequential and parallel work

Respond ONLY with a valid JSON object matching this schema:
{
  "workflow_type": "ForgeMasterOnly|SingleAgent|Chained|Parallel|Mixed",
  "steps": [
    {
      "agent_id": "registered available Agent ID or null",
      "description": "what this step does",
      "depends_on": []
    }
  ],
  "summary": "one sentence: what ForgeMaster will do and why",
  "clarification_needed": false,
  "clarification_question": null
}

Use only the registered Agent roster appended below. Never invent an Agent ID.
"""


class ForgeMasterService:
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def triage(
        self,
        session: Session,
        available_agents: list[Agent],
    ) -> WorkflowPlan:
        available_ids = [a.id for a in available_agents if a.is_available()]

        user_message = self._build_triage_message(session, available_ids)
        system_prompt = self._build_system_prompt(available_agents)

        response = self._client.messages.create(
            model="claude-opus-5",
            max_tokens=4096,
            thinking={"type": "adaptive", "display": "summarized"},
            output_config={"effort": "high"},
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = ""
        for block in response.content:
            if block.type == "text":
                raw = block.text
                break

        return self._parse_plan(raw, session.id, set(available_ids))

    def _build_system_prompt(self, agents: list[Agent]) -> str:
        roster = "\n".join(
            f"- {agent.id}: {agent.role} — {agent.description} "
            f"[status: {agent.status.value}]"
            for agent in agents
        )
        return f"{TRIAGE_SYSTEM_PROMPT}\n\nRegistered Agent roster:\n{roster}"

    def _build_triage_message(self, session: Session, available_ids: list[str]) -> str:
        actions = [a.label for a in session.selected_actions]
        preferred = session.selected_agent_id or "none"
        return (
            f"User objective: {session.prompt or '(no prompt provided)'}\n"
            f"Selected actions: {', '.join(actions) if actions else 'none'}\n"
            f"User preferred agent: {preferred}\n"
            f"Currently available agents: {', '.join(available_ids) if available_ids else 'none'}\n"
            f"WFG is active: {session.wfg.active}"
        )

    def _parse_plan(
        self,
        raw: str,
        session_id: str,
        available_agent_ids: set[str],
    ) -> WorkflowPlan:
        try:
            # Strip any markdown code fences if present
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text.strip())
        except (json.JSONDecodeError, IndexError):
            return WorkflowPlan(
                session_id=session_id,
                workflow_type=WorkflowType.FORGEMASTER_ONLY,
                status=WorkflowStatus.READY,
                forgemaster_summary="ForgeMaster received your request and is ready to proceed.",
                steps=[],
            )

        workflow_type = WorkflowType(data.get("workflow_type", "ForgeMasterOnly"))
        steps = []
        for step in data.get("steps", []):
            agent_id = step.get("agent_id")
            if agent_id is not None and agent_id not in available_agent_ids:
                continue
            steps.append(
                WorkflowStep(
                    agent_id=agent_id,
                    description=step.get("description", ""),
                    depends_on=step.get("depends_on", []),
                )
            )

        return WorkflowPlan(
            session_id=session_id,
            workflow_type=workflow_type,
            status=WorkflowStatus.READY,
            steps=steps,
            forgemaster_summary=data.get("summary", ""),
            clarification_needed=data.get("clarification_needed", False),
            clarification_question=data.get("clarification_question"),
        )
