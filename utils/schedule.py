import json
import os
from typing import Literal

import pandas as pd

# Data file paths
_DATA_DIR = "data"
_SCHEDULE_FILE = os.path.join(_DATA_DIR, "pydata_amsterdam_2025_schedule.json")
_DESCRIPTIONS_FILE = os.path.join(_DATA_DIR, "pydata_amsterdam_2025_descriptions.json")
_SPEAKERS_FILE = os.path.join(_DATA_DIR, "pydata_amsterdam_2025_speakers_description.json")

# Module-level caches
_cache_schedule: list[dict[str, str | int]] | None = None
_cache_descriptions: dict[int, str] | None = None
_cache_speakers: dict[str, str] | None = None


def _load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def _ensure_loaded() -> None:
    global _cache_schedule, _cache_descriptions, _cache_speakers
    if _cache_schedule is None:
        _cache_schedule = _load_json(_SCHEDULE_FILE)
    if _cache_descriptions is None:
        _cache_descriptions = _load_json(_DESCRIPTIONS_FILE)
    if _cache_speakers is None:
        _cache_speakers = _load_json(_SPEAKERS_FILE)


def get_schedule(out_format: Literal["dict", "pandas"] = "dict") -> list[dict[str, str | int]] | pd.DataFrame:
    """Get the schedule data.

    Args:
        out_format: "dict" (default) for native Python structures, or "pandas" for DataFrame.

    Returns:
        list[dict] or pandas.DataFrame
    """
    _ensure_loaded()
    return pd.DataFrame(_cache_schedule) if out_format == "pandas" else _cache_schedule


def get_descriptions(out_format: Literal["dict", "pandas"] = "dict") -> dict[str, str] | pd.Series:
    """Get the descriptions mapping keyed by event_id (as str).

    Args:
        out_format: "dict" (default) or "pandas" (Series indexed by event_id)
    """
    _ensure_loaded()
    return pd.Series(_cache_descriptions, name="description") if out_format == "pandas" else _cache_descriptions


def get_speakers(out_format: Literal["dict", "pandas"] = "dict") -> dict[str, str] | pd.DataFrame:
    """Get the speakers mapping keyed by speaker_id (as str).

    Args:
        out_format: "dict" (default) or "pandas" (DataFrame indexed by speaker_id)
    """
    _ensure_loaded()
    return pd.DataFrame.from_dict(_cache_speakers, orient="index") if out_format == "pandas" else _cache_speakers
