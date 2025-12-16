from __future__ import annotations
import math
import re
from datetime import datetime, timezone
from typing import Dict, List, Any
from .config import get_scoring_settings

_DT_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d",
    "%m/%d/%Y",
]

def _parse_dt(s: str | None):
    if not s:
        return None
    for fmt in _DT_FORMATS:
        try:
            dt = datetime.strptime(s, fmt)
            if not dt.tzinfo:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            continue
    return None

def _text(*parts: Any) -> str:
    return " ".join([str(p) for p in parts if p]).lower()

def _is_remote(listing: Dict[str, Any]) -> bool:
    # Loose signals that this is truly remote / global
    t = _text(listing.get("title"), listing.get("location"), listing.get("tags"), listing.get("description"))
    return any(
        kw in t
        for kw in ("remote", "anywhere", "work from anywhere", "distributed", "global")
    )

def _keyword_score(listing: Dict[str, Any], keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    hay = _text(
        listing.get("title"),
        listing.get("company"),
        listing.get("description"),
        " ".join(listing.get("tags", []) or []),
    )
    score = 0
    for kw in keywords:
        # whole word-ish match to avoid over-hits
        if re.search(rf"\b{re.escape(kw)}\b", hay):
            score += 1
    return score / max(1, len(keywords))  # normalize 0..1

def _recency_score(listing: Dict[str, Any], half_life_days: int) -> float:
    # Convert publication date to an exponential decay (1.0=now, ~0 as it ages)
    dt = _parse_dt(listing.get("published") or listing.get("date"))
    if not dt:
        return 0.0
    now = datetime.now(timezone.utc)
    age_days = max(0.0, (now - dt).total_seconds() / 86400.0)
    # half-life decay: score = 0.5 ** (age / half_life)
    if half_life_days <= 0:
        return 0.0
    return math.pow(0.5, age_days / float(half_life_days))

def score_listing(listing: Dict[str, Any]) -> float:
    s = get_scoring_settings()
    kws       = s["keywords"]
    weights   = s["weights"]
    half_life = s["half_life_days"]

    k = _keyword_score(listing, kws)
    r = 1.0 if _is_remote(listing) else 0.0
    t = _recency_score(listing, half_life)

    # weighted combination → 0..1
    final = (k * weights["keywords"]) + (r * weights["remote"]) + (t * weights["recency"])
    return round(float(final), 4)

def apply_scoring(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for item in listings:
        item = dict(item)
        item["score"] = score_listing(item)
        out.append(item)
    # sort high → low
    out.sort(key=lambda x: x.get("score", 0), reverse=True)
    return out
def score_listing_for_profile(
    listing: Dict[str, Any],
    user_config: Dict[str, Any],
) -> float:
    """
    Score a listing using a dynamic user_config instead of global keywords.
    user_config is expected to have fields like:
      - keywords: List[str]
      - skills: List[str]
      - preferred_roles: List[str]
      - disqualifiers: List[str]   (optional, handled outside if you prefer)
    """
    s = get_scoring_settings()
    weights   = s["weights"]
    half_life = s["half_life_days"]

    # Build a combined keyword list from the user profile
    combined_keywords: List[str] = []

    for field in ("keywords", "skills", "preferred_roles"):
        for val in user_config.get(field, []) or []:
            if isinstance(val, str):
                combined_keywords.append(val.lower())

    k = _keyword_score(listing, combined_keywords)
    r = 1.0 if _is_remote(listing) else 0.0
    t = _recency_score(listing, half_life)

    final = (k * weights["keywords"]) + (r * weights["remote"]) + (t * weights["recency"])
    return round(float(final), 4)

def apply_scoring_for_profile(
    listings: List[Dict[str, Any]],
    user_config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Apply per-user scoring across a batch of listings.
    """
    out = []
    for item in listings:
        item = dict(item)
        item["score"] = score_listing_for_profile(item, user_config)
        out.append(item)

    out.sort(key=lambda x: x.get("score", 0), reverse=True)
    return out
