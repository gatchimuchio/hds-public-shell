"""
倫理ポリシー

G1-G5 倫理原則に基づく公開可能域の判定シェル。

**重要**: 本モジュールは public-safe shell のみを含む。
再現可能な核手順、具体閾値、検出器はここに入れない。
それらは神域原理 rev1.6 付録Z 第一戒律により永久非公開。
"""

from __future__ import annotations

from .models import DecisionRequest, OutputState, PolicyDecision, WorldModel


class EthicsPolicy:
    """G1-G5 倫理原則に基づくポリシー評価器（公開骨格）

    評価順序:
        1. World Model (X, R, M) の閉包チェック → 未閉包なら SUSPEND
        2. 禁止タグ（PROHIBITED_TAGS）該当 → OUT_OF_SCOPE
        3. 高リスクタグ（HIGH_RISK_TAGS）該当 → SUSPEND (human review required)
        4. 上記いずれにも該当しなければ ASSERT

    公開骨格は上記の**構造**を提供するのみ。実際の意思決定を担保する
    検出器や閾値は封印範囲。
    """

    # 禁止タグ: G1-G5 のいずれかに明確に抵触する候補行為
    PROHIBITED_TAGS: dict[str, str] = {
        "human_ranking": "G1 violation: human ranking / dignity breach",
        "personality_scoring": "G1 violation: personality scoring",
        "manipulation": "G3/G4 violation: manipulation / domination route",
        "inducement": "G3/G4 violation: inducement / control route",
        "full_emotion_structuring": "G3 violation: full emotion structuring",
        "ego_design": "G3 violation: ego design / autonomous optimization",
        "full_decision_whitening": "G3 violation: total decision white-boxing",
        "irreversible_release": "G5 violation: irreversible release path",
        "weaponized_authority": "G1/G2 violation: authority shield usage",
    }

    # 高リスクタグ: 即座には禁止しないが、人間レビューを必須とする領域
    HIGH_RISK_TAGS: set[str] = {
        "policy",
        "public_infrastructure",
        "security",
        "finance",
        "biometrics",
        "psychological_inference",
        "mass_impact",
    }

    def evaluate(self, request: DecisionRequest, world: WorldModel) -> PolicyDecision:
        reasons: list[str] = []
        flags: list[str] = []

        # 1. 閉包チェック
        missing = self._check_closure(world)
        if missing:
            reasons.append(f"未閉包: {', '.join(missing)}")
            return PolicyDecision(
                allowed=False,
                output_state=OutputState.SUSPEND,
                reasons=reasons,
                requires_human_review=False,
                ethics_flags=["UNCLOSED_WORLD"],
            )

        # 2. 禁止タグ
        for tag in request.tags:
            if tag in self.PROHIBITED_TAGS:
                reasons.append(self.PROHIBITED_TAGS[tag])

        if reasons:
            flags.extend(["SEALED_DOMAIN_RISK", "TREATY_CONFLICT"])
            return PolicyDecision(
                allowed=False,
                output_state=OutputState.OUT_OF_SCOPE,
                reasons=reasons,
                requires_human_review=False,
                ethics_flags=flags,
            )

        # 3. 高リスクタグ
        if any(tag in self.HIGH_RISK_TAGS for tag in request.tags):
            return PolicyDecision(
                allowed=True,
                output_state=OutputState.SUSPEND,
                reasons=["高リスク領域のため人間レビューへ上送"],
                requires_human_review=True,
                ethics_flags=["HUMAN_REVIEW_REQUIRED"],
            )

        # 4. 通過
        return PolicyDecision(
            allowed=True,
            output_state=OutputState.ASSERT,
            reasons=[],
            requires_human_review=False,
            ethics_flags=[],
        )

    @staticmethod
    def _check_closure(world: WorldModel) -> list[str]:
        """TCP W:=(X,R,M) の閉包チェック。欠落軸のリストを返す。"""
        missing: list[str] = []
        if not world.x:
            missing.append("X")
        if not world.r:
            missing.append("R")
        if not world.m:
            missing.append("M")
        return missing


class DefaultHumanGate:
    """人間レビューゲート（デフォルト実装）

    本実装は最低限のパススルー。実運用では承認待ちキューや
    通知システムと接続する。
    """

    def review(self, draft):
        draft.requires_human_review = True
        return draft
