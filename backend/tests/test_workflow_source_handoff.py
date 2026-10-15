from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

from application.attach_source import AttachSource
from application.build_agent_task import BuildAgentTask
from application.dispatch_specialist import DispatchSpecialist
from application.run_workflow import RunWorkflow
from application.set_wfg import SetWFG
from application.update_prompt import UpdatePrompt
from agents.hermes_runtime import HermesInstructionLoader, HermesModelOutput, HermesRuntime
from domain.entities.session import Session
from domain.entities.workflow import WorkflowPlan, WorkflowStatus, WorkflowStep, WorkflowType
from domain.value_objects.action import Action
from infrastructure.repositories.local_source_repository import LocalSourceRepository
from infrastructure.repositories.memory_agent_repository import MemoryAgentRepository
from infrastructure.repositories.memory_session_repository import MemorySessionRepository
from infrastructure.runtime_registry import MemorySpecialistRuntimeRegistry


class FakeModelGateway:
    def __init__(self) -> None:
        self.last_request = None

    def analyze(self, request):
        self.last_request = request
        return HermesModelOutput(
            summary="Hermes analyzed the authorized login requirements.",
            findings=({"finding": "The website requires authenticated access."},),
            evidence_references=(request.sources[0].source_id,),
            supported_acceptance_criteria=request.acceptance_criteria,
        )


class StubInstructionLoader(HermesInstructionLoader):
    def load(self, capability_ids):
        return "Hermes instructions", tuple(f"Skill: {item}" for item in capability_ids)


class StubBeginWorkflow:
    def __init__(self, plan):
        self.plan = plan

    def execute(self, session_id):
        if session_id != self.plan.session_id:
            raise ValueError("Unexpected session")
        return self.plan


def make_docx(text: str) -> bytes:
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>"
    )
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", document)
    return buffer.getvalue()


class WorkflowSourceHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.storage_root = Path(self.temp_dir.name) / "sources"
        self.sessions = MemorySessionRepository()
        self.sources = LocalSourceRepository(self.storage_root)
        self.agents = MemoryAgentRepository()
        self.session = Session(
            prompt="Review the website login requirements.",
            selected_actions=[Action("Summarize")],
            selected_agent_id="hermes",
        )
        self.sessions.save(self.session)

    def attach_docx(self, session=None):
        target = session or self.session
        return AttachSource(self.sessions, self.sources, self.storage_root).execute(
            target.id,
            "Website Login Requirements.docx",
            make_docx("The website requires authenticated access."),
        )

    def make_plan(self):
        return WorkflowPlan(
            session_id=self.session.id,
            workflow_type=WorkflowType.SINGLE_AGENT,
            status=WorkflowStatus.READY,
            steps=[WorkflowStep(agent_id="hermes", description="Analyze the source.")],
            forgemaster_summary="Hermes will analyze the supplied requirements.",
        )

    def test_ingests_docx_inside_session_directory_with_hash_identity(self):
        source = self.attach_docx()

        location = Path(source.location)
        self.assertTrue(location.is_relative_to(self.storage_root / self.session.id))
        self.assertTrue(source.source_id.startswith("sha256:"))
        self.assertNotEqual(location.name, source.original_filename)
        self.assertEqual(self.sources.list_for_session(self.session.id), [source])

    def test_rejects_invalid_docx_package(self):
        with self.assertRaisesRegex(ValueError, "valid Office package"):
            AttachSource(self.sessions, self.sources, self.storage_root).execute(
                self.session.id, "invalid.docx", b"not-a-docx"
            )

    def test_updates_and_normalizes_workflow_objective(self):
        updated = UpdatePrompt(self.sessions).execute(
            self.session.id,
            "  Review the login requirements.  ",
        )

        self.assertEqual(updated.prompt, "Review the login requirements.")

    def test_task_contains_only_sources_from_its_session(self):
        expected = self.attach_docx()
        other = Session(prompt="Other")
        self.sessions.save(other)
        AttachSource(self.sessions, self.sources, self.storage_root).execute(
            other.id, "other.txt", b"Other session source"
        )

        task = BuildAgentTask(self.agents, self.sources).execute(
            self.session, self.make_plan(), self.make_plan().steps[0]
        )

        self.assertEqual(tuple(item.source_id for item in task.source_references), (expected.source_id,))
        self.assertEqual(task.requested_actions, ("summarize",))
        self.assertFalse(task.authorization.wfg_active)

    def test_wfg_blocks_task_construction(self):
        self.attach_docx()
        self.session.toggle_wfg()

        with self.assertRaisesRegex(ValueError, "WFG is active"):
            BuildAgentTask(self.agents, self.sources).execute(
                self.session, self.make_plan(), self.make_plan().steps[0]
            )

    def test_wfg_state_update_is_idempotent(self):
        first = SetWFG(self.sessions).execute(self.session.id, True)
        second = SetWFG(self.sessions).execute(self.session.id, True)

        self.assertTrue(first.wfg.active)
        self.assertTrue(second.wfg.active)

    def test_reset_removes_only_the_target_sessions_sources(self):
        from application.reset_session import ResetSession

        target_source = self.attach_docx()
        other = Session(prompt="Other")
        self.sessions.save(other)
        other_source = AttachSource(self.sessions, self.sources, self.storage_root).execute(
            other.id, "other.txt", b"Other session source"
        )

        ResetSession(self.sessions, self.sources).execute(self.session.id)

        self.assertFalse(Path(target_source.location).exists())
        self.assertTrue(Path(other_source.location).exists())
        self.assertEqual(self.sources.list_for_session(self.session.id), [])

    def test_deleting_one_source_cannot_remove_another_sessions_copy(self):
        target = self.attach_docx()
        other = Session(prompt="Other")
        self.sessions.save(other)
        other_source = AttachSource(self.sessions, self.sources, self.storage_root).execute(
            other.id, target.original_filename, make_docx("Other session content")
        )

        deleted = self.sources.delete(self.session.id, target.source_id)

        self.assertTrue(deleted)
        self.assertFalse(Path(target.location).exists())
        self.assertTrue(Path(other_source.location).exists())

    def test_forgemaster_plan_dispatches_real_docx_to_hermes_runtime(self):
        source = self.attach_docx()
        plan = self.make_plan()
        gateway = FakeModelGateway()
        runtime = HermesRuntime(
            model_gateway=gateway,
            instruction_loader=StubInstructionLoader(),
        )
        dispatcher = DispatchSpecialist(
            self.agents,
            MemorySpecialistRuntimeRegistry({"hermes": runtime}),
        )
        run = RunWorkflow(
            StubBeginWorkflow(plan),
            self.sessions,
            BuildAgentTask(self.agents, self.sources),
            dispatcher,
        ).execute(self.session.id)

        self.assertTrue(run.dispatch.succeeded)
        self.assertEqual(run.dispatch.result.agent_id, "hermes")
        self.assertEqual(gateway.last_request.sources[0].source_id, source.source_id)
        self.assertIn("authenticated access", gateway.last_request.sources[0].content)


if __name__ == "__main__":
    unittest.main()
