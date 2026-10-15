"""Direct API tests — no browser required."""
import pytest
import httpx

API = "http://localhost:8000"


@pytest.fixture(scope="module")
def client():
    with httpx.Client(base_url=API, timeout=10.0) as c:
        yield c


def test_health(client: httpx.Client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_agents_returns_six(client: httpx.Client) -> None:
    r = client.get("/api/agents")
    assert r.status_code == 200
    agents = r.json()
    assert len(agents) == 6


def test_agent_fields(client: httpx.Client) -> None:
    r = client.get("/api/agents")
    agent = r.json()[0]
    for field in ("id", "name", "role", "description", "status", "portrait_index"):
        assert field in agent


def test_hermes_is_available(client: httpx.Client) -> None:
    r = client.get("/api/agents")
    hermes = next(a for a in r.json() if a["id"] == "hermes")
    assert hermes["status"] == "Available"
    assert hermes["role"] == "Information Intelligence Agent"


def test_apolo_is_unavailable(client: httpx.Client) -> None:
    r = client.get("/api/agents")
    apolo = next(a for a in r.json() if a["id"] == "apolo")
    assert apolo["status"] == "Unavailable"


def test_create_session(client: httpx.Client) -> None:
    r = client.post("/api/sessions")
    assert r.status_code == 200
    data = r.json()
    assert "id" in data


def test_get_session(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    r = client.get(f"/api/sessions/{session_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == session_id


def test_toggle_wfg(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    r = client.patch(f"/api/sessions/{session_id}/wfg")
    assert r.status_code == 200
    assert r.json()["wfg_active"] is True
    r2 = client.patch(f"/api/sessions/{session_id}/wfg")
    assert r2.json()["wfg_active"] is False


def test_select_available_agent(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    r = client.patch(
        f"/api/sessions/{session_id}/agent",
        json={"agent_id": "hermes"},
    )
    assert r.status_code == 200
    assert r.json()["selected_agent_id"] == "hermes"


def test_cannot_select_unavailable_agent(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    r = client.patch(
        f"/api/sessions/{session_id}/agent",
        json={"agent_id": "apolo"},
    )
    assert r.status_code == 400


def test_update_actions(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    r = client.patch(
        f"/api/sessions/{session_id}/actions",
        json={"actions": ["Summarize", "Identify gaps"]},
    )
    assert r.status_code == 200
    assert set(r.json()["selected_actions"]) == {"Summarize", "Identify gaps"}


def test_deselect_agent(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    client.patch(f"/api/sessions/{session_id}/agent", json={"agent_id": "hermes"})
    r = client.patch(f"/api/sessions/{session_id}/agent", json={"agent_id": None})
    assert r.status_code == 200
    assert r.json()["selected_agent_id"] is None


def test_reset_session(client: httpx.Client) -> None:
    session_id = client.post("/api/sessions").json()["id"]
    client.patch(f"/api/sessions/{session_id}/agent", json={"agent_id": "hermes"})
    r = client.delete(f"/api/sessions/{session_id}")
    assert r.status_code == 200
    # Session state should be cleared
    state = client.get(f"/api/sessions/{session_id}").json()
    assert state["selected_agent_id"] is None
    assert state["selected_actions"] == []
