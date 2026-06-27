from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class LoginEvent(BaseModel):
    user_id: str = Field(..., description="Identificador seudonimizado del usuario")
    timestamp: str = Field(..., description="Fecha y hora del evento de login en formato ISO")
    ip: str = Field(..., description="Dirección IP pública observada")
    known_location: str = Field(..., description="Localización habitual del usuario")
    declared_city: str = Field(..., description="Ciudad estimada del evento")
    declared_region: Optional[str] = Field(default=None, description="Región estimada del evento")
    declared_country: str = Field(..., description="País estimado del evento")
    timezone_offset: Optional[str] = Field(default=None, description="Desfase horario estimado")
    user_agent: Optional[str] = Field(default=None, description="User agent del navegador o cliente")
    device_type: Optional[str] = Field(default=None, description="Tipo de dispositivo")
    network_type: Optional[str] = Field(default="residential", description="Tipo de red")
    asn: Optional[str] = Field(default=None, description="Sistema autónomo asociado a la IP")
    is_proxy: int = 0
    is_vpn: int = 0
    is_hosting: int = 0
    ip_reputation: str = "low"
    is_new_device: int = 0
    country_change: int = 0
    distance_from_prev_km: float = 0.0
    time_since_prev_min: float = 0.0
    travel_speed_kmh: float = 0.0
    timezone_mismatch: int = 0
    scenario_type: Optional[str] = "api_event"
    expected_result: Optional[str] = None


class RiskResponse(BaseModel):
    user_id: str
    risk_score: int
    risk_level: str
    recommended_action: str
    risk_reasons: List[str]
    message: str
