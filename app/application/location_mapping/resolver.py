import re
from typing import Optional, Sequence


_ZONE_LOCATIONS = {
    "nezo": "Bauchi",
    "swzo": "Ibadan",
    "sezo": "Enugu",
    "nwzo": "Kano",
    "sszo": "Port Harcourt",
    "nczo": "Ilorin",
    "rlo": "Abuja",
}


def _compact(value: str) -> str:
    compacted = re.sub(r"[^a-z0-9]", "", value.casefold())
    return "portharcourt" if compacted == "pharcourt" else compacted


def resolve_station_office_code(value: str, distance_sources: Sequence[Optional[str]]) -> Optional[str]:
    """Resolve headquarters and zonal codes to canonical Distance source values."""
    raw = value.strip()
    if re.match(r"^hq(?:[-\s]|$)", raw, re.IGNORECASE):
        sources = [source.strip() for source in distance_sources if source and source.strip()]
        return (
            next((source for source in sources if _compact(source) == "minnahq"), None)
            or next((source for source in sources if _compact(source) == "minna"), None)
            or "Minna"
        )

    zone_location = _ZONE_LOCATIONS.get(_compact(raw))
    if not zone_location:
        return None

    return next(
        (
            source.strip()
            for source in distance_sources
            if source and _compact(source.strip()) == _compact(zone_location)
        ),
        zone_location,
    )
