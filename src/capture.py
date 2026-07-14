# 3. Creación del módulo de captura

from __future__ import annotations
from datetime import datetime, timezone
from fastapi import Request


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"


def capture_signals(request: Request) -> dict:
    return {
        "ip": get_client_ip(request),
        "user_agent": request.headers.get("user-agent", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

