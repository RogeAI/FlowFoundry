import unittest

from agents.hermes import build_hermes_manifest
from infrastructure.repositories.memory_agent_repository import MemoryAgentRepository


class HermesManifestTests(unittest.TestCase):
    def test_manifest_declares_approved_identity_and_contract(self) -> None:
        manifest = build_hermes_manifest()

        self.assertEqual(manifest.agent_id, "hermes")
        self.assertEqual(manifest.agent_version, "1.0.0")
        self.assertIn("1.00", manifest.supported_contract_versions)

    def test_testability_capabilities_require_explicit_activation(self) -> None:
        manifest = build_hermes_manifest()
        capabilities = {item.capability_id: item for item in manifest.capabilities}

        self.assertTrue(capabilities["testability_analysis"].explicit_user_activation_required)
        self.assertTrue(capabilities["test_design_handover"].explicit_user_activation_required)
        self.assertFalse(capabilities["information_intelligence"].explicit_user_activation_required)

    def test_manifest_preserves_forgemaster_boundary(self) -> None:
        manifest = build_hermes_manifest()

        self.assertTrue(any("ForgeMaster" in boundary for boundary in manifest.boundaries))
        self.assertTrue(any("WFG" in boundary for boundary in manifest.boundaries))

    def test_registry_exposes_hermes_public_profile_and_manifest(self) -> None:
        repository = MemoryAgentRepository()

        public_agent = repository.get_by_id("hermes")
        manifest = repository.get_manifest("hermes")

        self.assertIsNotNone(public_agent)
        self.assertIsNotNone(manifest)
        self.assertEqual(public_agent.id, manifest.agent_id)
        self.assertEqual(len(repository.get_all()), 6)
        self.assertEqual([item.agent_id for item in repository.get_all_manifests()], ["hermes"])


if __name__ == "__main__":
    unittest.main()
