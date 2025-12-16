# app/core/summaries.py

from typing import Dict, List


ROLE_KEYWORDS = {
    "contract": ["contract", "contractor", "1099"],
    "part-time": ["part-time", "part time"],
    "full-time": ["full-time", "full time"],
    "freelance": ["freelance", "gig", "project-based", "project based"],
}

FOCUS_KEYWORDS = {
    "email marketing": ["email marketing", "email campaigns", "newsletters"],
    "content strategy": ["content strategy", "content strategist", "editorial"],
    "copywriting": ["copywriting", "copywriter", "sales copy"],
    "automation": ["automation", "workflows", "drip campaigns"],
    "analytics": ["analytics", "GA4", "google analytics", "dashboard"],
    "b2b": ["b2b", "business to business"],
}


def _detect_matches(text: str, keyword_map: Dict[str, List[str]]) -> List[str]:
    hits = []
    for label, terms in keyword_map.items():
        if any(term in text for term in terms):
            hits.append(label)
    return hits


def summarize_gig(gig: Dict, max_length: int = 240) -> str:
    """
    Produce a short, human-friendly summary of the gig.
    No AI calls, just heuristic text extraction.
    """
    title = (gig.get("position") or "Role").strip()
    company = (gig.get("company") or "an unnamed company").strip()
    location = gig.get("location") or "Remote / flexible"
    salary = gig.get("salary") or ""
    tags = gig.get("tags") or []
    description = (gig.get("description") or "").replace("\n", " ")
    text = description.lower()

    role_types = _detect_matches(text, ROLE_KEYWORDS)
    focuses = _detect_matches(text, FOCUS_KEYWORDS)

    role_part = ", ".join(role_types) if role_types else "flexible"
    focus_part = ", ".join(focuses) if focuses else None

    tag_snippet = ", ".join(tags[:4]) if tags else ""

    pieces = []

    # Core sentence
    core = f"{title} at {company} ({location}), {role_part}."
    pieces.append(core)

    # Focus
    if focus_part:
        pieces.append(f" Focus on {focus_part}.")
    elif tag_snippet:
        pieces.append(f" Focus around {tag_snippet}.")

    # Pay line if we have anything descriptive
    if isinstance(salary, str) and salary.strip():
        pieces.append(f" Compensation: {salary.strip()}.")

    summary = "".join(pieces).strip()

    if not summary:
        summary = "Role details are not clearly specified; description may need a closer look."

    # Truncate to max_length cleanly
    if len(summary) > max_length:
        summary = summary[: max_length - 1].rstrip() + "…"

    return summary
