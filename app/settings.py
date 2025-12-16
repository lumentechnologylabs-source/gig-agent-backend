from __future__ import annotations
from dataclasses import dataclass
import os
from datetime import timedelta

def _csv(name: str) -> list[str]:
    raw = os.getenv(name, "") or ""
    return [x.strip().lower() for x in raw.split(",") if x.strip()]

@dataclass
class Settings:
    keywords: list[str]
    avoid: list[str]
    min_pay: float | None
    remote_only: bool
    allow_contracts: bool

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            keywords=_csv("GA_KEYWORDS"),
            avoid=_csv("GA_AVOID"),
            min_pay=float(os.getenv("GA_MIN_PAY")) if os.getenv("GA_MIN_PAY") else None,
            remote_only=(os.getenv("GA_REMOTE_ONLY", "true").lower() == "true"),
            allow_contracts=(os.getenv("GA_ALLOW_CONTRACTS", "true").lower() == "true"),
        )

settings = Settings.load()

# Try to load .env if python-dotenv is available; otherwise rely on process env
try:
    from dotenv import load_dotenv  # optional
    load_dotenv()
except Exception:
    pass

def _get(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v if v is not None else default

def _get_float(name: str, default: float) -> float:
    try:
        return float(_get(name, str(default)))
    except Exception:
        return default

def get_scoring_settings():
    # keywords as lowercased, trimmed list
    kws = [k.strip().lower() for k in _get("PREFERRED_KEYWORDS", "").split(",") if k.strip()]
    weight_keywords = _get_float("WEIGHT_KEYWORDS", 0.7)
    weight_remote   = _get_float("WEIGHT_REMOTE",   0.2)
    weight_recency  = _get_float("WEIGHT_RECENCY",  0.1)
    half_life_days  = int(float(_get("RECENCY_HALF_LIFE_DAYS", "21")))

    # Normalize weights to sum to 1.0
    total = max(1e-9, (weight_keywords + weight_remote + weight_recency))
    weights = {
        "keywords": weight_keywords / total,
        "remote":   weight_remote   / total,
        "recency":  weight_recency  / total,
    }
    return {
        "keywords": kws,
        "weights": weights,
        "half_life_days": half_life_days,
    }
