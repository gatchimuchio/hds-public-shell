"""
FastAPI エンドポイントのスモークテスト
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from hds_public_shell.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "hds-public-shell"
    assert data["mode"] == "public-safe-shell"
    assert "version" in data
    assert data["sealed_scope_enforced"] is True
    assert "source_trust_review" in data["capabilities"]


def test_readiness_endpoint():
    response = client.get("/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["source_trust_policy"]["untrusted"] == "SUSPEND"


def test_policy_endpoint_lists_principles():
    response = client.get("/policy")
    assert response.status_code == 200
    data = response.json()
    assert "public_scope" in data
    assert "sealed_scope" in data
    assert "source_trust" in data
    assert "prohibited_tags" in data
    assert "high_risk_tags" in data
    assert "ethics_principles" in data
    # G1-G5 全て入っている
    assert len(data["ethics_principles"]) == 5
    assert any("DIGNITY" in p for p in data["ethics_principles"])


def test_decision_endpoint_assert_for_benign():
    payload = {
        "user_goal": "test goal",
        "candidate_action": "safe_action",
        "context": {"domain": "general"},
        "inputs": {"problem": "smoke"},
        "constraints": ["reversible"],
        "tags": ["engineering"],
        "metadata": {"scope": "smoke-test"},
    }
    response = client.post("/decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["output_state"] == "ASSERT"
    assert data["selected_action"] == "safe_action"


def test_decision_endpoint_out_of_scope_for_prohibited():
    payload = {
        "user_goal": "bad goal",
        "candidate_action": "bad_action",
        "tags": ["manipulation"],
    }
    response = client.post("/decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["output_state"] == "OUT_OF_SCOPE"
    assert data["selected_action"] is None


def test_decision_endpoint_suspends_untrusted_source():
    payload = {
        "user_goal": "external message",
        "candidate_action": "answer",
        "context": {"source": "discord:alice", "source_trust": "untrusted"},
    }
    response = client.post("/decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["output_state"] == "SUSPEND"
    assert data["requires_human_review"] is True
    assert "UNTRUSTED_SOURCE_REVIEW" in data["commit"]["ethics_flags"]
