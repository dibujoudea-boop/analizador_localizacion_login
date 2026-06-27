from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any


CONFIG = {
    "weights": {
        "location_not_home": 20,
        "country_change": 12,
        "new_device": 8,
        "risky_network": 18,
        "timezone_mismatch": 8,
        "off_hours": 7,
        "high_speed_travel": 20,
        "medium_speed_travel": 10,
        "high_ip_reputation": 12,
        "medium_ip_reputation": 6,
        "proxy_indicator": 10,
        "vpn_indicator": 10,
        "hosting_indicator": 12,
    },
    "thresholds": {
        "high_speed_kmh": 900,
        "medium_speed_kmh": 300,
        "risk_medium": 25,
        "risk_high": 50,
    },
    "off_hours": {0, 1, 2, 3, 4, 5, 23},
    "risky_networks": {"proxy", "hosting", "tor", "vpn"},
}


@dataclass
class ScoreResult:
    score: int
    level: str
    reasons: List[str]
    recommended_action: str
    message: str


def _safe_lower(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _parse_hour(timestamp_value: Any) -> Optional[int]:
    try:
        if isinstance(timestamp_value, datetime):
            return timestamp_value.hour
        return datetime.fromisoformat(str(timestamp_value).replace("Z", "")).hour
    except Exception:
        return None


def classify_score(score: int, config: Dict = CONFIG) -> str:
    thresholds = config["thresholds"]

    if score >= thresholds["risk_high"]:
        return "alto"
    if score >= thresholds["risk_medium"]:
        return "medio"
    return "bajo"


def action_from_level(level: str) -> tuple[str, str]:
    if level == "alto":
        return (
            "block_or_review",
            "Riesgo alto: se recomienda bloquear preventivamente o escalar el evento para revisión."
        )
    if level == "medio":
        return (
            "step_up_mfa",
            "Riesgo medio: se recomienda solicitar verificación adicional antes de permitir el acceso."
        )
    return (
        "allow",
        "Riesgo bajo: el acceso puede permitirse sin controles adicionales."
    )


def score_login_event(event: Dict[str, Any], config: Dict = CONFIG) -> ScoreResult:
    weights = config["weights"]
    thresholds = config["thresholds"]

    score = 0
    reasons: List[str] = []

    known_location = _safe_lower(event.get("known_location"))
    declared_city = _safe_lower(event.get("declared_city"))

    if declared_city and known_location and declared_city != known_location:
        score += weights["location_not_home"]
        reasons.append("localizacion_distinta_a_la_habitual")

    if _safe_int(event.get("country_change")) == 1:
        score += weights["country_change"]
        reasons.append("cambio_de_pais")

    if _safe_int(event.get("is_new_device")) == 1:
        score += weights["new_device"]
        reasons.append("nuevo_dispositivo")

    network_type = _safe_lower(event.get("network_type"))

    if network_type in config["risky_networks"]:
        score += weights["risky_network"]
        reasons.append(f"red_sospechosa:{network_type}")

    if _safe_int(event.get("is_proxy")) == 1:
        score += weights["proxy_indicator"]
        reasons.append("indicador_proxy")

    if _safe_int(event.get("is_vpn")) == 1:
        score += weights["vpn_indicator"]
        reasons.append("indicador_vpn")

    if _safe_int(event.get("is_hosting")) == 1:
        score += weights["hosting_indicator"]
        reasons.append("indicador_hosting")

    if _safe_int(event.get("timezone_mismatch")) == 1:
        score += weights["timezone_mismatch"]
        reasons.append("desajuste_de_zona_horaria")

    hour = _parse_hour(event.get("timestamp"))

    if hour is not None and hour in config["off_hours"]:
        score += weights["off_hours"]
        reasons.append("horario_atipico")

    travel_speed = _safe_float(event.get("travel_speed_kmh"))

    if travel_speed >= thresholds["high_speed_kmh"]:
        score += weights["high_speed_travel"]
        reasons.append("viaje_imposible")
    elif travel_speed >= thresholds["medium_speed_kmh"]:
        score += weights["medium_speed_travel"]
        reasons.append("desplazamiento_poco_plausible")

    ip_reputation = _safe_lower(event.get("ip_reputation"))

    if ip_reputation == "high":
        score += weights["high_ip_reputation"]
        reasons.append("reputacion_ip_alta")
    elif ip_reputation == "medium":
        score += weights["medium_ip_reputation"]
        reasons.append("reputacion_ip_media")

    level = classify_score(score, config)
    recommended_action, message = action_from_level(level)

    return ScoreResult(
        score=score,
        level=level,
        reasons=reasons,
        recommended_action=recommended_action,
        message=message,
    )


def compare_expected_vs_obtained(expected: str, obtained: str) -> str:
    order = {"bajo": 1, "medio": 2, "alto": 3}

    expected = _safe_lower(expected)
    obtained = _safe_lower(obtained)

    if expected == obtained:
        return "acierto"
    if order.get(obtained, 0) < order.get(expected, 0):
        return "subestimacion"
    return "sobrestimacion"
