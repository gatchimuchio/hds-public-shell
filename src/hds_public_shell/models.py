"""
データモデル定義

HDS Public-Safe Upper Control の Pydantic モデル群。
決定要求・フレーム出力・モデル出力・コミット出力・監査イベント等。
"""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class OutputState(str, Enum):
    """出力状態。F→M→C ループの最終判定。"""

    ASSERT = "ASSERT"
    SUSPEND = "SUSPEND"
    REJECT = "REJECT"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    END = "END"
    FAIL = "FAIL"


class DecisionPhase(str, Enum):
    """決定相。F (Frame) → M (Model) → C (Commit)。"""

    F = "FRAME"
    M = "MODEL"
    C = "COMMIT"


class RiskLevel(str, Enum):
    """リスク水準。"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class EthicsPrinciple(str, Enum):
    """倫理原則 G1-G5。"""

    G1 = "G1_DIGNITY_NON_RANKING"
    G2 = "G2_SINCERITY"
    G3 = "G3_BLACK_BOX_RESPECT"
    G4 = "G4_GAMEOVER_AVOIDANCE"
    G5 = "G5_REVERSIBILITY"


class DecisionRequest(BaseModel):
    """決定要求。候補行為・目的・文脈を含む。"""

    request_id: str = Field(default_factory=lambda: str(uuid4()))
    user_goal: str
    candidate_action: str

    context: dict[str, Any] = Field(default_factory=dict)
    inputs: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorldModel(BaseModel):
    """TCP: World := (X, R, M)。X=対象、R=関係、M=メタ規則。"""

    x: dict[str, Any] = Field(default_factory=dict)
    r: dict[str, Any] = Field(default_factory=dict)
    m: dict[str, Any] = Field(default_factory=dict)


class FrameOutput(BaseModel):
    """F 相の出力。目的・保護値・観測境界・世界モデルを定義する。"""

    purpose: list[str] = Field(default_factory=list)
    protected_values: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    observation_boundary: list[str] = Field(default_factory=list)
    world: WorldModel = Field(default_factory=WorldModel)


class ModelOutput(BaseModel):
    """M 相の出力。抽象化・構造・評価の受け皿。

    公開骨格では内部評価器を固定しない（value_estimate / risk_estimate は
    placeholder）。実運用では封印された核手順で埋める。
    """

    abstractions: dict[str, Any] = Field(default_factory=dict)
    structure: dict[str, Any] = Field(default_factory=dict)
    value_estimate: dict[str, Any] = Field(default_factory=dict)
    risk_estimate: dict[str, Any] = Field(default_factory=dict)
    alternatives: list[str] = Field(default_factory=list)


class CommitOutput(BaseModel):
    """C 相の出力。最終コミット or 保留・拒否・圏外。"""

    output_state: OutputState
    action: str | None = None
    rationale_summary: str
    requires_human_review: bool = False
    ethics_flags: list[str] = Field(default_factory=list)
    stop_reasons: list[str] = Field(default_factory=list)


class DecisionResult(BaseModel):
    """F→M→C 完了後の最終結果。監査IDと全相の出力を含む。"""

    request_id: str
    audit_id: str
    output_state: OutputState
    selected_action: str | None = None
    rationale_summary: str
    requires_human_review: bool

    frame: FrameOutput
    model: ModelOutput
    commit: CommitOutput


class PolicyDecision(BaseModel):
    """倫理ポリシー評価結果。C 相で参照される。"""

    allowed: bool
    output_state: OutputState
    reasons: list[str] = Field(default_factory=list)
    requires_human_review: bool = False
    ethics_flags: list[str] = Field(default_factory=list)


class AuditEvent(BaseModel):
    """監査イベント。全ての相遷移と決定がここに記録される。"""

    timestamp_utc: str
    request_id: str
    phase: str
    event_type: str
    payload: dict[str, Any]


class HealthResponse(BaseModel):
    """/health エンドポイントの応答。"""

    status: str
    service: str
    mode: str
    version: str
