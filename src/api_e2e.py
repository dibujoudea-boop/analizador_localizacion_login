# 8. Creación del nuevo end point

from __future__ import annotations

from typing import Optional

from fastapi import Request
from pydantic import BaseModel, Field

# Importa la app existente y añade una ruta nueva. No modifica
# api_login_analyzer.py: solo registra un endpoint adicional sobre la misma
# instancia.
from src.api_login_analyzer import app
from src.schemas import RiskResponse
from src.pipeline import run_raw_pipeline


class RawLoginBody(BaseModel):
    user_id: str = Field(..., description="Identificador seudonimizado del usuario")
    known_location: Optional[str] = Field(
        default=None,
        description="Ciudad habitual del usuario. Opcional; en el futuro se derivará del historial.",
    )


@app.post("/login-event/raw", response_model=RiskResponse, tags=["end-to-end"])
def analyze_raw_login_event(body: RawLoginBody, request: Request) -> RiskResponse:
    """Analiza un evento de login a partir de la petición real.

    A diferencia de POST /login-event (v4), no exige las señales precalculadas:
    captura IP, user-agent y hora de la propia petición HTTP y deriva la
    geolocalización antes de puntuar.
    """
    return run_raw_pipeline(body.model_dump(), request)
