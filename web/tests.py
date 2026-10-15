import json

from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def test_about_page_preserves_locked_product_language(self):
        response = self.client.get(reverse("web:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "From an idea to coordinated action")
        self.assertContains(response, "ForgeMaster")
        self.assertContains(response, "Wait for GO")

    def test_workspace_is_rendered_by_django(self):
        response = self.client.get(reverse("web:workspace"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What would you like to achieve?")
        self.assertContains(response, "WFG")

    def test_python_endpoint_prepares_the_local_workflow(self):
        response = self.client.post(
            reverse("web:prepare_workflow"),
            data=json.dumps({"objective": "Review requirements", "actions": ["Identify gaps"], "preferred_agent": "athena"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ready")
        self.assertEqual(len(payload["steps"]), 3)
        self.assertEqual(payload["preferred_agent"], "athena")
        self.assertEqual(payload["workflow_type"], "Chained")
        self.assertTrue(payload["session_id"])

    def test_go_releases_wfg_in_the_python_domain(self):
        response = self.client.post(
            reverse("web:prepare_workflow"),
            data=json.dumps({"objective": "Review requirements", "wfg_active": True}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["wfg_active"])

    def test_workspace_uses_the_python_agent_registry(self):
        response = self.client.get(reverse("web:workspace"))
        self.assertContains(response, "Athena")
        self.assertContains(response, "Information Intelligence Agent")
        self.assertContains(response, "Currently unavailable")

    def test_empty_objective_requests_clarification(self):
        response = self.client.post(reverse("web:prepare_workflow"), data=json.dumps({"objective": ""}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "clarification")

    def test_working_session_is_rendered_by_django(self):
        response = self.client.get(reverse("web:session"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workflow in progress")
        self.assertContains(response, "ForgeMaster Live Feed")
        self.assertContains(response, "Local Django simulation")

    def test_python_endpoint_resumes_an_investigating_session(self):
        response = self.client.post(
            reverse("web:respond_to_session"),
            data=json.dumps({"response": "Executive audience with a concise summary."}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "resumed")
        self.assertIn("Hermes", payload["acknowledgement"])

    def test_session_response_requires_meaningful_input(self):
        response = self.client.post(
            reverse("web:respond_to_session"),
            data=json.dumps({"response": "   "}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "clarification")
