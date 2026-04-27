"""FastAPI entrypoint for the public-safe HDS shell."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from . import __version__
from .controller import HDSUpperController
from .logger import AuditLogger
from .models import AuditEvent, DecisionRequest, DecisionResult, EthicsPrinciple, HealthResponse
from .policy import EthicsPolicy


def create_app() -> FastAPI:
    app = FastAPI(
        title="HDS Public-Safe Upper Control API",
        version=__version__,
        description=(
            "公開可能域に限定した HDS 上流制御層。"
            "F→M→C 3相ループと G1-G5 倫理原則を骨格として提供する。"
        ),
    )

    logger = AuditLogger()
    policy = EthicsPolicy()
    controller = HDSUpperController(logger=logger, ethics_policy=policy)

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service="hds-public-shell",
            mode="public-safe-shell",
            version=__version__,
            sealed_scope_enforced=True,
            capabilities=[
                "fmc_loop",
                "tcp_closure_check",
                "source_trust_review",
                "public_safe_tag_inference",
                "audit_redaction",
            ],
        )

    @app.get("/readiness")
    def readiness() -> dict[str, Any]:
        return {
            "status": "ready",
            "service": "hds-public-shell",
            "mode": "public-safe-shell",
            "fail_closed_recommended": True,
            "source_trust_policy": {
                "missing_external_trust": "SUSPEND",
                "untrusted": "SUSPEND",
                "paired": "ASSERT_ELIGIBLE",
                "trusted": "ASSERT_ELIGIBLE",
            },
        }

    @app.post("/decision", response_model=DecisionResult)
    def decide(request: DecisionRequest) -> DecisionResult:
        return controller.run(request)

    @app.get("/audit", response_model=list[AuditEvent])
    def get_audit(request_id: str | None = None) -> list[AuditEvent]:
        if request_id:
            return logger.get_by_request_id(request_id)
        return logger.get_all()

    @app.delete("/audit")
    def clear_audit() -> dict[str, str]:
        logger.clear()
        return {"status": "cleared"}

    @app.get("/policy")
    def policy_summary() -> dict[str, Any]:
        return {
            "public_scope": [
                "operational definitions",
                "closure conditions",
                "stop rules",
                "log schema",
                "misuse-prevention boundaries",
            ],
            "sealed_scope": [
                "reproducible core recipe",
                "thresholds",
                "detectors",
                "HDS-BB detailed implementation",
                "full decision whitening",
            ],
            "source_trust": {
                "local": "eligible for normal policy evaluation",
                "trusted": "eligible for normal policy evaluation",
                "paired": "eligible for normal policy evaluation",
                "untrusted": "SUSPEND for human review",
                "unknown": "SUSPEND when a source is present",
            },
            "prohibited_tags": sorted(policy.PROHIBITED_TAGS),
            "high_risk_tags": sorted(policy.HIGH_RISK_TAGS),
            "ethics_principles": [e.value for e in EthicsPrinciple],
        }

    return app


app = create_app()


def run() -> None:
    import uvicorn
    uvicorn.run("hds_public_shell.main:app", host="127.0.0.1", port=8000, reload=False)
