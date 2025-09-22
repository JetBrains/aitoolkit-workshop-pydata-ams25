from datetime import datetime


def current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_iso(dt: str) -> datetime:
    # Handles ISO8601 with timezone (e.g., 2025-09-24T09:00:00+02:00 or Z)
    if dt is None:
        return None
    if dt.endswith("Z"):
        dt = dt.replace("Z", "+00:00")
    return datetime.fromisoformat(dt)


def duration_to_minutes(hhmm: str) -> int:
    # Pretalx FRAB format: "HH:MM"
    if not hhmm:
        return 0
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m
