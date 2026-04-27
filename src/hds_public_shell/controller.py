"""
HDS Upper Controller

F→M→C 3相ループの実行エンジン。各相で監査ログを刻み、倫理ポリシーに
違反する候補行為は SUSPEND / REJECT / OUT_OF_SCOPE で停止する。

**重要**: _phase_m の value_estimate / risk_estimate は意図的に
placeholder。内部評価器は封印範囲であり、公開骨格では受け皿のみ提供する。
"""

from __future__ import annotations

from uuid import uuid4

from .logger import AuditLogger
from .models import (
    CommitOutput,
    DecisionPhase,
    DecisionRequest,
    DecisionResult,
    EthicsPrinciple,
    FrameOutput,
    ModelOutput,
    OutputState,
    PolicyDecision,
    RiskLevel,
    WorldModel,
)
from .policy import DefaultHumanGate, EthicsPolicy


class DecisionException(Exception):
    """F→M→C 内の早期停止用例外の基底"""

    def __init__(self, message: str, reasons: list[str] | None = None) -> None:
        super().__init__(message)
        self.reasons = reasons or []


class SuspendDecision(DecisionException):
    pass


class RejectDecision(DecisionException):
    pass


class OutOfScopeDecision(DecisionException):
    pass


class HDSUpperController:
    """F→M→C 3相ループのコントローラ"""

    def __init__(
        self,
        logger: AuditLogger | None = None,
        ethics_policy: EthicsPolicy | None = None,
        human_gate: DefaultHumanGate | None = None,
    ) -> None:
        self.logger = logger or AuditLogger()
        self.ethics_policy = ethics_policy or EthicsPolicy()
        self.human_gate = human_gate or DefaultHumanGate()

    def run(self, request: DecisionRequest) -> DecisionResult:
        audit_id = str(uuid4())

        self.logger.log(
            request_id=request.request_id,
            phase="SYSTEM",
            event_type="REQUEST_RECEIVED",
            payload=request.model_dump(),
        )

        try:
            frame = self._phase_f(request)
            model = self._phase_m(request, frame)
            commit = self._phase_c(request, frame, model)

            result = DecisionResult(
                request_id=request.request_id,
                audit_id=audit_id,
                output_state=commit.output_state,
                selected_action=commit.action,
                rationale_summary=commit.rationale_summary,
                requires_human_review=commit.requires_human_review,
                frame=frame,
                model=model,
                commit=commit,
            )

            self.logger.log(
                request_id=request.request_id,
                phase="SYSTEM",
                event_type="DECISION_COMPLETED",
                payload={
                    "audit_id": audit_id,
                    "output_state": result.output_state.value,
                    "requires_human_review": result.requires_human_review,
                },
            )
            return result

        except SuspendDecision as e:
            return self._abort_result(
                request, audit_id, OutputState.SUSPEND, str(e), e.reasons
            )
        except RejectDecision as e:
            return self._abort_result(
                request, audit_id, OutputState.REJECT, str(e), e.reasons
            )
        except OutOfScopeDecision as e:
            return self._abort_result(
                request, audit_id, OutputState.OUT_OF_SCOPE, str(e), e.reasons
            )
        except Exception as e:
            self.logger.log(
                request_id=request.request_id,
                phase="SYSTEM",
                event_type="FAIL",
                payload={"error": repr(e)},
            )
            return self._abort_result(
                request,
                audit_id,
                OutputState.FAIL,
                "運用障害",
                [repr(e)],
            )

    def _phase_f(self, request: DecisionRequest) -> FrameOutput:
        """F 相: 目的と保護値の明示、世界モデルの初期化"""
        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.F.value,
            event_type="ENTER",
            payload={},
        )

        protected_values = list(dict.fromkeys([
            EthicsPrinciple.G1.value,
            EthicsPrinciple.G2.value,
            EthicsPrinciple.G3.value,
            EthicsPrinciple.G4.value,
            EthicsPrinciple.G5.value,
            *request.constraints,
        ]))
        source, source_trust = self.ethics_policy.source_info(request)
        inferred_tags = self.ethics_policy.collect_tags(request)

        world = WorldModel(
            x={
                "request_id": request.request_id,
                "candidate_action": request.candidate_action,
                "scope": request.metadata.get("scope", "unspecified"),
                "source": source,
                "source_trust": source_trust,
            },
            r={
                "goal": request.user_goal,
                "context_keys": list(request.context.keys()),
                "input_keys": list(request.inputs.keys()),
                "tags": inferred_tags,
            },
            m={
                "stop_rule_enabled": True,
                "log_required": True,
                "public_safe_only": True,
                "no_reproducible_core_recipe": True,
                "source_trust_required_for_external_input": True,
                "tag_inference": "public_safe_rules_only",
            },
        )

        frame = FrameOutput(
            purpose=[request.user_goal],
            protected_values=protected_values,
            out_of_scope=request.metadata.get("out_of_scope", []),
            observation_boundary=request.metadata.get(
                "observation_boundary",
                [
                    "外周のみ扱う",
                    "ブラックボックス完全可視化を行わない",
                    "不可逆公開を既定動作にしない",
                ],
            ),
            world=world,
        )

        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.F.value,
            event_type="FRAME_BUILT",
            payload=frame.model_dump(),
        )
        return frame

    def _phase_m(self, request: DecisionRequest, frame: FrameOutput) -> ModelOutput:
        """M 相: 抽象化と評価の構造化

        ここは封印領域の**受け皿**のみ提供する。実際の value_estimate や
        risk_estimate の計算は公開骨格には含まれない。
        """
        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.M.value,
            event_type="ENTER",
            payload={},
        )

        model = ModelOutput(
            abstractions={
                "goal": request.user_goal,
                "candidate": request.candidate_action,
                "constraints": request.constraints,
                "tags": self.ethics_policy.collect_tags(request),
            },
            structure={
                "axes": ["value", "risk", "goal"],
                "phases": ["F", "M", "C"],
                "note": "公開骨格では内部評価器を固定しない",
                "source_trust": self.ethics_policy.source_info(request)[1],
            },
            value_estimate={
                "status": "placeholder",
                "description": "目的に照らした望ましさの受け皿",
            },
            risk_estimate={
                "level": RiskLevel.UNKNOWN.value,
                "tail_risk": "uncomputed",
                "reversibility_required": True,
            },
            alternatives=request.metadata.get(
                "alternatives",
                ["SUSPEND", "HUMAN_REVIEW", "SAFE_MINIMAL_ACTION"],
            ),
        )

        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.M.value,
            event_type="MODEL_BUILT",
            payload=model.model_dump(),
        )
        return model

    def _phase_c(
        self,
        request: DecisionRequest,
        frame: FrameOutput,
        model: ModelOutput,
    ) -> CommitOutput:
        """C 相: 倫理ポリシー評価と最終コミット"""
        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.C.value,
            event_type="ENTER",
            payload={},
        )

        policy: PolicyDecision = self.ethics_policy.evaluate(request, frame.world)

        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.C.value,
            event_type="POLICY_EVALUATED",
            payload=policy.model_dump(),
        )

        if not policy.allowed:
            if policy.output_state == OutputState.SUSPEND:
                raise SuspendDecision("未閉包または決定保留", policy.reasons)
            if policy.output_state == OutputState.REJECT:
                raise RejectDecision("仕様違反", policy.reasons)
            raise OutOfScopeDecision("封印領域または条約抵触", policy.reasons)

        draft = CommitOutput(
            output_state=policy.output_state,
            action=None if policy.requires_human_review else request.candidate_action,
            rationale_summary=self._build_rationale(request, policy),
            requires_human_review=policy.requires_human_review,
            ethics_flags=policy.ethics_flags,
            stop_reasons=policy.reasons,
        )

        if draft.requires_human_review:
            draft = self.human_gate.review(draft)

        self.logger.log(
            request_id=request.request_id,
            phase=DecisionPhase.C.value,
            event_type="COMMIT_DRAFTED",
            payload=draft.model_dump(),
        )
        return draft

    @staticmethod
    def _build_rationale(request: DecisionRequest, policy: PolicyDecision) -> str:
        if policy.requires_human_review:
            return f"候補行為 '{request.candidate_action}' は高リスクのため人間レビューへ上送"
        if policy.allowed:
            return f"候補行為 '{request.candidate_action}' は公開骨格上は許容"
        return "停止または拒否"

    def _abort_result(
        self,
        request: DecisionRequest,
        audit_id: str,
        state: OutputState,
        message: str,
        reasons: list[str],
    ) -> DecisionResult:
        commit = CommitOutput(
            output_state=state,
            action=None,
            rationale_summary=message,
            requires_human_review=False,
            stop_reasons=reasons,
        )

        self.logger.log(
            request_id=request.request_id,
            phase="SYSTEM",
            event_type="DECISION_ABORTED",
            payload={
                "audit_id": audit_id,
                "state": state.value,
                "message": message,
                "reasons": reasons,
            },
        )

        return DecisionResult(
            request_id=request.request_id,
            audit_id=audit_id,
            output_state=state,
            selected_action=None,
            rationale_summary=message,
            requires_human_review=False,
            frame=FrameOutput(),
            model=ModelOutput(),
            commit=commit,
        )
