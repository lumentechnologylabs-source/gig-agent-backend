from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Any


# This should resolve to: C:\lumen_agents\agents\gig_agent\configs
DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"


@dataclass
class UserConfig:
    profile_name: str = "default"

    # Core matching
    titles_include: List[str] = field(default_factory=list)
    keywords_must_have: List[str] = field(default_factory=list)
    keywords_nice_to_have: List[str] = field(default_factory=list)
    keywords_avoid: List[str] = field(default_factory=list)

    # Work style
    remote_only: bool = True
    locations_preferred: List[str] = field(default_factory=list)
    max_hours_per_week: Optional[int] = None

    # Money / seniority
    min_hourly_rate: Optional[float] = None
    min_annual_salary: Optional[float] = None
    preferred_seniority: List[str] = field(default_factory=list)

    # Free-form notes
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

    data = path.read_text(encoding="utf-8")
    import json
    obj = json.loads(data)

    return UserConfig.from_dict(obj)
