# 7. Creación del pipeline

from __future__ import annotations

from typing import Any, Dict

from fastapi import Request

from src.capture import capture_signals
from src import enrichment
from src import geo_cache
from src.history import derive_history_signals
from src.risk_engine import score_login_event
from src.storage import save_event_result
from src.schemas import RiskResponse

# Activa la caché sobre enrichment.geolocate_ip al importar el pipeline.
geo_cache.install_cache()


def run_raw_pipeline(body: Dict[str, Any], request: Request) -> RiskResponse:
    """Flujo funcional end-to-end para un evento de login crudo.

    Recibe únicamente lo aportado por el cliente (user_id y, opcionalmente,
    known_location), captura las señales reales de la petición HTTP, enriquece
    con geolocalización y reutiliza el motor y la persistencia de la v4 SIN
    modificarlos.
    """
    # 1) Captura de señales reales de la petición (IP, user-agent, hora).
    captured = capture_signals(request)

    # 2) Evento base: identidad del cliente + señales capturadas.
    event: Dict[str, Any] = {
        "user_id": body.get("user_id"),
        "ip": captured["ip"],
        "user_agent": captured["user_agent"],
        "timestamp": captured["timestamp"],
        "network_type": "residential",
        "scenario_type": "api_event_raw",
    }

    # 3) Enriquecimiento geográfico (con caché). Reutiliza tu enrich_geo.
    event = enrichment.enrich_geo(event)

    # 4) Señales de secuencia derivadas del historial del usuario:
    #    distancia, velocidad (viaje imposible), cambio de país, dispositivo
    #    nuevo, desajuste horario y ubicación habitual. Se calcula ANTES de
    #    guardar el evento actual, para no compararlo consigo mismo.
    señales_historial = derive_history_signals(event)
    event.update(señales_historial)

    # 5) known_location: la ubicación habitual derivada del historial tiene
    #    prioridad; si el usuario no tiene historial, se usa la que aporte el
    #    cliente y, en su defecto, la ciudad actual (para no penalizar el
    #    primer acceso).
    event["known_location"] = (
        señales_historial.get("known_location")
        or body.get("known_location")
        or event.get("declared_city")
    )

    # 6) Scoring con el motor existente (sin cambios).
    result = score_login_event(event)

    # 7) Persistencia con el módulo existente (sin cambios).
    save_event_result(
        event=event,
        risk_score=result.score,
        risk_level=result.level,
        recommended_action=result.recommended_action,
        risk_reasons=result.reasons,
    )

    return RiskResponse(
        user_id=event.get("user_id"),
        risk_score=result.score,
        risk_level=result.level,
        recommended_action=result.recommended_action,
        risk_reasons=result.reasons,
        message=result.message,
    )
