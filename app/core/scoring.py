from typing import Dict, List
from typing import Dict, Any, Optional
from app.user_config import UserConfig
DEFAULT_PREFERENCES: Dict = {
    "skills": [
        # Core strengths
        "email marketing",
        "email campaigns",
        "newsletters",
        "content marketing",
        "content strategy",
        "copywriting",
        "copywriter",
        "editorial",
        "landing pages",
        "lead generation",
        "demand generation",
        "marketing automation",
        "funnels",
        "seo",
        "sem",
        "social media",
        "campaign strategy",

        # Tools you know / adjacent
        "HubSpot",
        "GA4",
        "google analytics",
        "crm",
        "marketing ops",
        "b2b",
    ],
    "min_rate_hourly": 40,  # you can bump this as you like
    "prefer_remote": True,
    # Jobs we probably DON'T want at the top of the list
    "anti_terms": [
        "unpaid",
        "commission only",
        "mlm",
        "crypto casino",
        "door to door",
        "cold calling",
        "recruitment consultant",
        "recruiter",
        "data engineer",
        "backend engineer",
        "senior motion designer",
        "3d artist",
        "c++",
    ],
    # Phrases that nudge things upward a bit
    "bonus_terms": [
        "part-time",
        "part time",
        "contract",
        "freelance",
        "project-based",
        "project based",
        "remote",
        "async",
        "independent contractor",
        "flexible hours",
    ],
}

def normalize_text(gig: Dict) -> str:
    parts: List[str] = []
    for key in ("position", "company", "description", "tags", "location"):
        val = gig.get(key)
        if isinstance(val, list):
            parts.extend(str(v) for v in val)
        elif val:
            parts.append(str(val))
    return " ".join(parts).lower()

from typing import Dict, Any, Optional
from app.user_config import UserConfig


def score_gig(
    gig: Dict[str, Any],
    preferences: Optional[Dict[str, Any]] = None,
    user_config: Optional[UserConfig] = None,
) -> float:
    """
    Compute a score for a gig.

    - `preferences` is kept for backwards compatibility (can be {} or None).
    - `user_config` is the new, richer profile-based config.

    If user_config is provided, we use it to boost/penalize gigs based on
    Cindy-style preferences (titles, must-have, avoid, etc.).
    """

    title = (gig.get("position") or gig.get("title") or "").lower()
    description = (gig.get("description") or "").lower()
    location = (gig.get("location") or "").lower()
    text = f"{title}\n{description}"

    score = 0.0

    # --- Generic base heuristics (you can tweak these later) ---

    # Slight bonus if clearly remote
    if "remote" in text or "work from home" in text:
        score += 5

    # Slight penalty if clearly on-site with no remote mention
    if ("onsite" in text or "on-site" in text) and "remote" not in text:
        score -= 5

    # Very rough seniority hints
    if "senior" in text:
        score += 1
    if "junior" in text or "entry-level" in text:
        score -= 1

    # --- UserConfig-based scoring ---

    if user_config is not None:
        # required keywords: missing = big penalty
        if user_config.keywords_must_have:
            missing = [
                kw for kw in user_config.keywords_must_have
                if kw.lower() not in text
            ]
            if missing:
                score -= 50  # effectively sinks gigs that miss must-haves

        # nice-to-have keywords: each one adds a small bonus
        for kw in user_config.keywords_nice_to_have:
            if kw.lower() in text:
                score += 3

        # avoid keywords: each one subtracts
        for kw in user_config.keywords_avoid:
            if kw.lower() in text:
                score -= 10

        # prefer certain titles
        for desired in user_config.titles_include:
            if desired.lower() in title:
                score += 8

        # remote-only preference
        if user_config.remote_only:
            if ("onsite" in text or "on-site" in text) and "remote" not in text:
                score -= 15

        # preferred locations
        if user_config.locations_preferred:
            if any(loc.lower() in location for loc in user_config.locations_preferred):
                score += 5

        # rough hours check
        if user_config.max_hours_per_week is not None:
            if "full-time" in text or "40 hours" in text or "40hrs" in text:
                score -= 5

        # seniority preference
        for level in user_config.preferred_seniority:
            if level.lower() in text:
                score += 4

    # You can still later add extra handling if `preferences` is a dict,
    # but for now we largely ignore it; old calls can pass {} safely.
    return score
