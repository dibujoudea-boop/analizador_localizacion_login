from __future__ import annotations

from fastapi import FastAPI
from src.schemas import LoginEvent, RiskResponse
from src.risk_engine import score_login_event
from src.storage import save_event_result, read_recent_events, init_db


app = FastAPI(
    title="Analizador Localización de Login",
    description="API funcional para analizar riesgo contextual de eventos de inicio de sesión.",
    version="4.0.0",
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/")
def root() -> dict:
    return {
        "project": "Analizador Localización de Login",
        "version": "4.0.0",
        "status": "running",
    }


@app.post("/login-event", response_model=RiskResponse)
def analyze_login_event(event: LoginEvent) -> RiskResponse:
    event_dict = event.model_dump()

    result = score_login_event(event_dict)

    save_event_result(
        event=event_dict,
        risk_score=result.score,
        risk_level=result.level,
        recommended_action=result.recommended_action,
        risk_reasons=result.reasons,
    )

    return RiskResponse(
        user_id=event.user_id,
        risk_score=result.score,
        risk_level=result.level,
        recommended_action=result.recommended_action,
        risk_reasons=result.reasons,
        message=result.message,
    )


@app.get("/events/recent")
def recent_events(limit: int = 20) -> dict:
    return {
        "events": read_recent_events(limit=limit)
    }
