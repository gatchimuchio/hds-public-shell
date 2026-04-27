"""
HDSUpperController と EthicsPolicy の基本動作テスト
"""

from __future__ import annotations

from hds_public_shell.controller import HDSUpperController
from hds_public_shell.logger import AuditLogger
from hds_public_shell.models import DecisionRequest, OutputState
from hds_public_shell.policy import EthicsPolicy


def _build_request(
    *,
    tags: list[str] | None = None,
    user_goal: str = "test goal",
    candidate_action: str = "safe_action",
    context: dict | None = None,
    inputs: dict | None = None,
) -> DecisionRequest:
    return DecisionRequest(
        user_goal=user_goal,
        candidate_action=candidate_action,
        context=context or {"domain": "general"},
        inputs=inputs or {"problem": "unit test"},
        constraints=["no manipulation"],
        tags=["engineering"] if tags is None else tags,
        metadata={"scope": "unit-test"},
    )


def test_fmc_loop_completes_for_benign_request():
    controller = HDSUpperController()
    req = _build_request()
    result = controller.run(req)
    assert result.output_state == OutputState.ASSERT
    assert result.selected_action == "safe_action"
    assert result.requires_human_review is False


def test_prohibited_tag_triggers_out_of_scope():
    controller = HDSUpperController()
    req = _build_request(tags=["engineering", "manipulation"])
    result = controller.run(req)
    assert result.output_state == OutputState.OUT_OF_SCOPE
    assert result.selected_action is None
    assert any("manipulation" in r for r in result.commit.stop_reasons)


def test_high_risk_tag_triggers_suspend_with_review():
    controller = HDSUpperController()
    req = _build_request(tags=["policy"])
    result = controller.run(req)
    assert result.output_state == OutputState.SUSPEND
    assert result.requires_human_review is True


def test_untrusted_source_triggers_suspend_with_review():
    controller = HDSUpperController()
    req = _build_request(
        context={"source": "discord:alice", "source_trust": "untrusted"},
    )
    result = controller.run(req)
    assert result.output_state == OutputState.SUSPEND
    assert result.requires_human_review is True
    assert "UNTRUSTED_SOURCE_REVIEW" in result.commit.ethics_flags


def test_unknown_external_source_triggers_suspend():
    controller = HDSUpperController()
    req = _build_request(context={"source": "slack:bob"})
    result = controller.run(req)
    assert result.output_state == OutputState.SUSPEND
    assert result.requires_human_review is True


def test_paired_source_is_assert_eligible():
    controller = HDSUpperController()
    req = _build_request(
        context={"source": "discord:alice", "source_trust": "paired"},
    )
    result = controller.run(req)
    assert result.output_state == OutputState.ASSERT
    assert result.frame.world.x["source_trust"] == "paired"


def test_public_safe_tag_inference_catches_human_ranking():
    controller = HDSUpperController()
    req = _build_request(
        tags=[],
        user_goal="rank employees by personality score",
        candidate_action="produce ranking",
    )
    result = controller.run(req)
    assert result.output_state == OutputState.OUT_OF_SCOPE
    assert any("human ranking" in reason for reason in result.commit.stop_reasons)


def test_ego_design_tag_is_rejected():
    """ego_design は rev1.6 付録Z の封印領域"""
    controller = HDSUpperController()
    req = _build_request(tags=["ego_design"])
    result = controller.run(req)
    assert result.output_state == OutputState.OUT_OF_SCOPE


def test_full_decision_whitening_is_rejected():
    """完全な意思決定ホワイトボックス化は G3 違反"""
    controller = HDSUpperController()
    req = _build_request(tags=["full_decision_whitening"])
    result = controller.run(req)
    assert result.output_state == OutputState.OUT_OF_SCOPE


def test_audit_trail_records_fmc_phases():
    audit = AuditLogger()
    controller = HDSUpperController(logger=audit)
    req = _build_request()
    result = controller.run(req)

    events = audit.get_by_request_id(req.request_id)
    phases = [e.phase for e in events]
    event_types = [e.event_type for e in events]

    assert "SYSTEM" in phases
    assert "FRAME" in phases
    assert "MODEL" in phases
    assert "COMMIT" in phases
    assert "REQUEST_RECEIVED" in event_types
    assert "FRAME_BUILT" in event_types
    assert "MODEL_BUILT" in event_types
    assert "COMMIT_DRAFTED" in event_types
    assert "DECISION_COMPLETED" in event_types
    assert result.audit_id


def test_audit_redacts_secret_payloads():
    audit = AuditLogger()
    audit.log(
        request_id="req_secret",
        phase="SYSTEM",
        event_type="SECRET_TEST",
        payload={"inputs": {"api_key": "sk-test", "nested": {"password": "pw"}}},
    )
    event = audit.get_by_request_id("req_secret")[0]
    assert event.payload["inputs"]["api_key"] == "[REDACTED]"
    assert event.payload["inputs"]["nested"]["password"] == "[REDACTED]"


def test_policy_closure_check_suspends_on_empty_world():
    """XRM 未閉包は SUSPEND"""
    from hds_public_shell.models import WorldModel

    policy = EthicsPolicy()
    req = _build_request()
    empty_world = WorldModel()  # x, r, m 全て空
    decision = policy.evaluate(req, empty_world)
    assert decision.output_state == OutputState.SUSPEND
    assert "UNCLOSED_WORLD" in decision.ethics_flags


def test_audit_jsonl_roundtrip(tmp_path):
    """audit ログの JSONL 書き出し/読み込み"""
    audit = AuditLogger()
    controller = HDSUpperController(logger=audit)
    req = _build_request()
    controller.run(req)

    out = tmp_path / "audit.jsonl"
    count = audit.dump_jsonl(out)
    assert count > 0

    loaded = AuditLogger.load_jsonl(out)
    assert len(loaded) == count
    assert loaded[0].request_id == req.request_id
