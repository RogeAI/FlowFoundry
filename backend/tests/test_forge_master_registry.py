import json
import sys
import types
import unittest

try:
    import anthropic  # noqa: F401
except ModuleNotFoundError:
    sys.modules["anthropic"] = types.SimpleNamespace(Anthropic=object)

from domain.entities.agent import Agent, AgentStatus
from domain.services.forge_master import ForgeMasterService


class ForgeMasterRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ForgeMasterService.__new__(ForgeMasterService)
        self.hermes = Agent(
            id="hermes",
            name="Hermes",
            role="Information Intelligence Agent",
            description="Transforms mixed information into evidence-aware intelligence.",
            status=AgentStatus.AVAILABLE,
            portrait_index=1,
        )

    def test_system_prompt_uses_registered_roster(self) -> None:
        prompt = self.service._build_system_prompt([self.hermes])

        self.assertIn("hermes: Information Intelligence Agent", prompt)
        self.assertNotIn("scribe: Document Intelligence", prompt)

    def test_plan_rejects_unregistered_agent_id(self) -> None:
        raw = json.dumps(
            {
                "workflow_type": "SingleAgent",
                "steps": [
                    {"agent_id": "hermes", "description": "Analyze", "depends_on": []},
                    {"agent_id": "scribe", "description": "Legacy", "depends_on": []},
                ],
                "summary": "Use Hermes.",
                "clarification_needed": False,
                "clarification_question": None,
            }
        )

        plan = self.service._parse_plan(raw, "session-1", {"hermes"})

        self.assertEqual([step.agent_id for step in plan.steps], ["hermes"])


if __name__ == "__main__":
    unittest.main()
