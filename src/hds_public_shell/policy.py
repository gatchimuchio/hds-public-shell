"""
倫理ポリシー

G1-G5 倫理原則に基づく公開可能域の判定シェル。

**重要**: 本モジュールは public-safe shell のみを含む。
再現可能な核手順、具体閾値、検出器はここに入れない。
それらは神域原理 rev1.6 付録Z 第一戒律により永久非公開。
"""

from __future__ import annotations

import re
from typing import Any

from .models import DecisionRequest, OutputState, PolicyDecision, SourceTrust, WorldModel


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

    _TEXT_TAG_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
        (
            re.compile(
                r"(?i)\b(human ranking|rank people|rank humans|rank employees|"
                r"rank students|score people|score humans|score employees)\b|"
                r"(人間|人物|社員|学生).*(ランキング|順位付け|格付け)",
            ),
            "human_ranking",
        ),
        (
            re.compile(
                r"(?i)\b(personality score|personality scoring|score personality|"
                r"predict personality)\b|人格.*(スコア|採点|評価)",
            ),
            "personality_scoring",
        ),
        (
            re.compile(
                r"(?i)\b(manipulate|coerce|dominate|exploit a weakness|dark pattern)\b|"
                r"(支配|強制|弱点を突く|ダークパターン)",
            ),
            "manipulation",
        ),
    )

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

        source, source_trust = self.source_info(request)
        if source and source_trust not in {
            SourceTrust.LOCAL.value,
            SourceTrust.TRUSTED.value,
            SourceTrust.PAIRED.value,
        }:
            return PolicyDecision(
                allowed=True,
                output_state=OutputState.SUSPEND,
                reasons=[f"untrusted or unknown source requires pairing/review: {source}"],
                requires_human_review=True,
                ethics_flags=["UNTRUSTED_SOURCE_REVIEW"],
            )

        tags = self.collect_tags(request)

        # 2. 禁止タグ
        for tag in tags:
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
        high_risk = sorted(tag for tag in tags if tag in self.HIGH_RISK_TAGS)
        if high_risk:
            return PolicyDecision(
                allowed=True,
                output_state=OutputState.SUSPEND,
                reasons=[f"high-risk HDS tag requires human review: {', '.join(high_risk)}"],
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

    @classmethod
    def collect_tags(cls, request: DecisionRequest) -> list[str]:
        tags: list[str] = []
        tags.extend(str(tag) for tag in request.tags if tag)
        for container in (request.context, request.inputs, request.metadata):
            extra_tags = container.get("hds_tags") if isinstance(container, dict) else None
            if isinstance(extra_tags, str):
                tags.append(extra_tags)
            elif isinstance(extra_tags, (list, tuple, set)):
                tags.extend(str(tag) for tag in extra_tags if tag)

        text_parts = [
            request.user_goal,
            request.candidate_action,
            *cls._string_values(request.inputs),
            *cls._string_values(request.context),
        ]
        for text in text_parts:
            for pattern, tag in cls._TEXT_TAG_RULES:
                if pattern.search(text):
                    tags.append(tag)

        module = str(request.context.get("module", ""))
        resource = str(request.context.get("resource", ""))
        if module == "web_fetch" or resource.startswith(("http://", "https://")):
            tags.append("security")
        if _as_int(request.inputs.get("payload_size")) > 200_000:
            tags.append("mass_impact")
        if _as_int(request.inputs.get("side_effect_bytes_out_total")) > 10 * 1024 * 1024:
            tags.append("mass_impact")
        return sorted(set(tags))

    @staticmethod
    def source_info(request: DecisionRequest) -> tuple[str | None, str]:
        source = _first_str(
            request.context.get("source"),
            request.metadata.get("source"),
            request.inputs.get("source"),
        )
        trust = _first_str(
            request.context.get("source_trust"),
            request.metadata.get("source_trust"),
            request.inputs.get("source_trust"),
        )
        if trust in {item.value for item in SourceTrust}:
            return source, trust
        return source, SourceTrust.UNKNOWN.value if source else SourceTrust.LOCAL.value

    @staticmethod
    def _string_values(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, dict):
            out: list[str] = []
            for item in value.values():
                out.extend(EthicsPolicy._string_values(item))
            return out
        if isinstance(value, (list, tuple, set)):
            out: list[str] = []
            for item in value:
                out.extend(EthicsPolicy._string_values(item))
            return out
        return []


def _first_str(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


class DefaultHumanGate:
    """人間レビューゲート（デフォルト実装）

    本実装は最低限のパススルー。実運用では承認待ちキューや
    通知システムと接続する。
    """

    def review(self, draft):
        draft.requires_human_review = True
        return draft
