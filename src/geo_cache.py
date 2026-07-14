# 5. Creación de cache de geolocalizaciones

from __future__ import annotations

import json
from pathlib import Path

from src import enrichment

# Caché en disco de respuestas de geolocalización. Clave = IP, valor = dict
# devuelto por enrichment.geolocate_ip. Aporta dos cosas:
#   1) Reproducibilidad: una API online devuelve datos que dependen de la red
#      y del momento; con caché, re-ejecutar el notebook da el mismo resultado.
#   2) Ahorro de peticiones: evita agotar el límite gratuito de ip-api
#      (~45 peticiones/minuto) al repetir IPs.
CACHE_PATH = Path("data/geo_cache.json")

_installed = False


def _load() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def install_cache() -> None:
    """Envuelve ``enrichment.geolocate_ip`` con una caché en disco.

    No modifica ``enrichment.py``: sustituye la referencia del módulo por una
    versión cacheada. Como ``enrich_geo`` invoca ``geolocate_ip`` por su nombre
    global, empezará a usar la caché de forma transparente. Es idempotente.
    """
    global _installed
    if _installed:
        return

    original = enrichment.geolocate_ip

    def cached(ip: str, timeout: int = 5) -> dict:
        cache = _load()
        if ip in cache:
            return cache[ip]
        result = original(ip, timeout=timeout)
        # Solo se cachean respuestas válidas; los fallos se reintentan.
        if result.get("geo_ok"):
            cache[ip] = result
            _save(cache)
        return result

    enrichment.geolocate_ip = cached
    _installed = True
