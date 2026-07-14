# 6. Creacion módulo para consultar el historico de las ultimos 10 eventos

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from datetime import datetime
from math import radians, sin, cos, asin, sqrt
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.storage import DB_PATH, init_db

# Número de eventos previos del usuario que se consideran para construir su
# perfil habitual (ubicación, zona horaria, dispositivos conocidos).
DEFAULT_WINDOW = 10

# Tope de velocidad (km/h) para evitar valores absurdos cuando el intervalo
# entre dos eventos es casi nulo (p.ej. accesos casi simultáneos desde dos
# países). Basta con superar holgadamente el umbral de "viaje imposible".
MAX_SPEED_KMH = 100000.0


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Distancia en kilómetros entre dos coordenadas (fórmula de haversine)."""
    r = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(a))


def _parse_iso(value: Any) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


def get_user_history(
    user_id: str,
    n: int = DEFAULT_WINDOW,
    db_path: Path = DB_PATH,
) -> List[Dict[str, Any]]:
    """Devuelve los N eventos previos del usuario (más reciente primero).

    Cada elemento es el evento crudo (``raw_event``) ya deserializado, que
    contiene las señales derivadas por el enriquecimiento (_lat, _lon,
    declared_city, timezone_offset, user_agent, etc.).
    """
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT raw_event
            FROM login_events
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, n),
        ).fetchall()

    history: List[Dict[str, Any]] = []
    for row in rows:
        try:
            history.append(json.loads(row["raw_event"]))
        except (json.JSONDecodeError, TypeError):
            continue
    return history


def _mode(values: List[Any]) -> Optional[Any]:
    """Valor más frecuente de una lista, ignorando vacíos."""
    limpios = [v for v in values if v]
    if not limpios:
        return None
    return Counter(limpios).most_common(1)[0][0]


def derive_history_signals(
    event: Dict[str, Any],
    n: int = DEFAULT_WINDOW,
    db_path: Path = DB_PATH,
) -> Dict[str, Any]:
    """Deriva las señales de secuencia a partir del historial del usuario.

    Devuelve un diccionario con las señales que consume el motor de scoring.
    Para un usuario SIN historial se aplica una línea base neutra: no se
    penaliza el primer acceso (no hay comportamiento previo con el que
    comparar); el perfil de riesgo emerge a partir del segundo evento.
    """
    user_id = event.get("user_id", "")
    history = get_user_history(user_id, n=n, db_path=db_path)

    señales: Dict[str, Any] = {
        "known_location": None,
        "country_change": 0,
        "distance_from_prev_km": 0.0,
        "time_since_prev_min": 0.0,
        "travel_speed_kmh": 0.0,
        "is_new_device": 0,
        "timezone_mismatch": 0,
    }

    # Usuario nuevo: sin historial, línea base neutra.
    if not history:
        return señales

    # Ubicación y zona horaria habituales = moda de la ventana de eventos.
    señales["known_location"] = _mode([h.get("declared_city") for h in history])
    tz_habitual = _mode([h.get("timezone_offset") for h in history])

    prev = history[0]  # evento inmediatamente anterior (más reciente)

    # Cambio de país respecto al último acceso.
    pais_actual = event.get("declared_country")
    pais_prev = prev.get("declared_country")
    if pais_actual and pais_prev and pais_actual != pais_prev:
        señales["country_change"] = 1

    # Distancia, tiempo y velocidad respecto al último acceso.
    lat_a, lon_a = event.get("_lat"), event.get("_lon")
    lat_p, lon_p = prev.get("_lat"), prev.get("_lon")
    if None not in (lat_a, lon_a, lat_p, lon_p):
        dist = _haversine_km(lat_p, lon_p, lat_a, lon_a)
        señales["distance_from_prev_km"] = round(dist, 2)

        t_actual = _parse_iso(event.get("timestamp"))
        t_prev = _parse_iso(prev.get("timestamp"))
        if t_actual and t_prev:
            minutos = abs((t_actual - t_prev).total_seconds()) / 60.0
            señales["time_since_prev_min"] = round(minutos, 2)
            if minutos > 0:
                velocidad = dist / (minutos / 60.0)
            else:
                # Dos accesos en el mismo instante desde puntos distantes:
                # desplazamiento físicamente imposible.
                velocidad = MAX_SPEED_KMH if dist > 0 else 0.0
            señales["travel_speed_kmh"] = round(min(velocidad, MAX_SPEED_KMH), 2)

    # Dispositivo nuevo: el user-agent actual no aparece en el historial.
    ua_actual = (event.get("user_agent") or "").strip().lower()
    ua_previos = {(h.get("user_agent") or "").strip().lower() for h in history}
    if ua_actual and ua_actual not in ua_previos:
        señales["is_new_device"] = 1

    # Desajuste de zona horaria respecto a la habitual del usuario.
    tz_actual = event.get("timezone_offset")
    if tz_habitual and tz_actual and tz_actual != tz_habitual:
        señales["timezone_mismatch"] = 1

    return señales
