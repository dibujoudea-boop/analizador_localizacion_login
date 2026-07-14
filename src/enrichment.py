# 4. Creación del módulo de enriquecimiento

from __future__ import annotations

import json
import urllib.request
from ipaddress import ip_address

_NEUTRAL = {
    "declared_city": None,
    "declared_region": None,
    "declared_country": None,
    "lat": None,
    "lon": None,
    "timezone_offset": None,
    "asn": None,
    "geo_ok": False,
}


def _is_geolocatable(ip: str) -> bool:
    try:
        addr = ip_address(ip)
        return not (addr.is_private or addr.is_loopback or addr.is_reserved
                    or addr.is_link_local or addr.is_unspecified)
    except ValueError:
        return False


def geolocate_ip(ip: str, timeout: int = 5) -> dict:
    result = dict(_NEUTRAL)
    if not _is_geolocatable(ip):
        return result

    fields = "status,message,countryCode,regionName,city,lat,lon,timezone,as"
    url = f"http://ip-api.com/json/{ip}?fields={fields}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("status") == "success":
            result.update({
                "declared_city": data.get("city"),
                "declared_region": data.get("regionName"),
                "declared_country": data.get("countryCode"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "timezone_offset": data.get("timezone"),
                "asn": data.get("as"),
                "geo_ok": True,
            })
    except Exception:
        pass
    return result


def enrich_geo(event_dict: dict) -> dict:
    geo = geolocate_ip(event_dict.get("ip", ""))
    if geo["geo_ok"]:
        event_dict["declared_city"] = geo["declared_city"] or event_dict.get("declared_city")
        event_dict["declared_region"] = geo["declared_region"]
        event_dict["declared_country"] = geo["declared_country"] or event_dict.get("declared_country")
        event_dict["timezone_offset"] = geo["timezone_offset"]
        event_dict["asn"] = geo["asn"]
        event_dict["_lat"] = geo["lat"]
        event_dict["_lon"] = geo["lon"]
    return event_dict
