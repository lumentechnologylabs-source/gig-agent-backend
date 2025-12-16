from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import List, Optional, Any
from pathlib import Path
import json
from typing import Optional

# Base directory of the project: .../gig_agent
BASE_DIR = Path(__file__).resolve().parent.parent

# configs/ directory beside app/
CONFIG_DIR = BASE_DIR / "configs"

# Map simple profile keys to JSON filenames
PROFILE_MAP = {
    "cindy": "cindy.json",
    # later: "designer": "designer.json", etc.
}


def load_profile(profile_key: Optional[str] = None) -> dict:
    """
    Load a profile configuration by key.
    If no key is provided, defaults to 'cindy'.
    """
    key = (profile_key or "cindy").lower()

    filename = PROFILE_MAP.get(key)
    if not filename:
        raise ValueError(
        f"Unknown profile '{key}'. Valid options: {list(PROFILE_MAP.keys())}"
        )

    path = CONFIG_DIR / filename

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Profile file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in profile file {path}: {e}")

# Where we'll look for profile configs, relative to project root
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "configs"


@dataclass
class UserConfig:
    profile_name: str = "default"

    # Core matching
    titles_include: List[str] = field(default_factory=list)        # job titles you like
    keywords_must_have: List[str] = field(default_factory=list)    # required
    keywords_nice_to_have: List[str] = field(default_factory=list) # bonus
    keywords_avoid: List[str] = field(default_factory=list)        # red flags

    # Work style
    remote_only: bool = True
    locations_preferred: List[str] = field(default_factory=list)
    max_hours_per_week: Optional[int] = None

    # Money / seniority
    min_hourly_rate: Optional[float] = None
    min_annual_salary: Optional[float] = None
    preferred_seniority: List[str] = field(default_factory=list)   # ["junior","mid","senior"]

    # Free-form notes / future extension
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserConfig":
        return cls(
            profile_name=data.get("profile_name", "default"),
            titles_include=data.get("titles_include", []),
            keywords_must_have=data.get("keywords_must_have", []),
            keywords_nice_to_have=data.get("keywords_nice_to_have", []),
            keywords_avoid=data.get("keywords_avoid", []),
            remote_only=data.get("remote_only", True),
            locations_preferred=data.get("locations_preferred", []),
            max_hours_per_week=data.get("max_hours_per_week"),
            min_hourly_rate=data.get("min_hourly_rate"),
            min_annual_salary=data.get("min_annual_salary"),
            preferred_seniority=data.get("preferred_seniority", []),
            notes=data.get("notes", ""),
        )


def load_user_config(profile: Optional[str]) -> Optional[UserConfig]:
    """
    If profile is None, return None (no customization).
    Otherwise, load configs/<profile>.json.
    """
    if not profile:
        return None

    config_dir = DEFAULT_CONFIG_DIR
    path = config_dir / f"{profile}.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Profile '{profile}' not found at {path}. "
            f"Create it or choose a different --profile."
        )

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return UserConfig.from_dict(data)
