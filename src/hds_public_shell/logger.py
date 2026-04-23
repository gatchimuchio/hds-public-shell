"""
監査ログ

全ての F→M→C 相遷移と決定を記録する。本実装は in-memory を基底とし、
オプションで JSONL ファイルにも同時書き出しする。

監査の完全性は HDS Public-Safe Upper Control の根幹。全ての相・決定・
停止理由は例外なくここに流れる。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import AuditEvent


class AuditLogger:
    """in-memory + optional JSONL ファイル出力の監査ログ"""

    def __init__(self, log_path: Path | str | None = None) -> None:
        self._events: list[AuditEvent] = []
        self.log_path: Path | None = Path(log_path) if log_path else None
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        request_id: str,
        phase: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        event = AuditEvent(
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            request_id=request_id,
            phase=phase,
            event_type=event_type,
            payload=payload,
        )
        self._events.append(event)
        if self.log_path:
            with self.log_path.open("a", encoding="utf-8") as fp:
                fp.write(event.model_dump_json() + "\n")

    def get_all(self) -> list[AuditEvent]:
        return list(self._events)

    def get_by_request_id(self, request_id: str) -> list[AuditEvent]:
        return [e for e in self._events if e.request_id == request_id]

    def clear(self) -> None:
        """in-memory バッファのみクリア。ファイル出力は残す。"""
        self._events.clear()

    def dump_jsonl(self, path: Path | str) -> int:
        """現在の in-memory バッファを JSONL にダンプする。

        Returns:
            書き出したイベント数
        """
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fp:
            for e in self._events:
                fp.write(e.model_dump_json() + "\n")
        return len(self._events)

    @staticmethod
    def load_jsonl(path: Path | str) -> list[AuditEvent]:
        """JSONL から AuditEvent 群を復元する。"""
        events: list[AuditEvent] = []
        with Path(path).open(encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                events.append(AuditEvent(**json.loads(line)))
        return events
