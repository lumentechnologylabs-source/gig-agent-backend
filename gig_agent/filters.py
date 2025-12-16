# gig_agent/filters.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Iterable, List, Dict, Optional

Listing = Dict[str, object]


def _normalize(text: Optional[str]) -> str:
    return (text or "").strip().lower()


def filter_remote_only(listings: Iterable[Listing], remote_only: bool) -> List[Listing]:
    if not remote_only:
        return list(listings)

    result: List[Listing] = []
    for row in listings:
        loc = _normalize(str(row.get("location", "")))
        title = _normalize(str(row.get("title", "")))
        # simple heuristics – adjust as needed
        if "remote" in loc or "remote" in title:
            result.append(row)
    return result


def filter_posted_within(listings: Iterable[Listing], days: Optional[int]) -> List[Listing]:
    if not days:
        return list(listings)

    cutoff = datetime.utcnow() - timedelta(days=days)
    result: List[Listing] = []

    for row in listings:
        published = row.get("published") or row.get("date") or row.get("posted_at")
        if not published:
            # keep if we don't know – or skip if you prefer stricter
            result.append(row)
            continue

        dt = _parse_date(published)
        if dt is None or dt >= cutoff:
            result.append(row)

    return result


def _parse_date(value) -> Optional[datetime]:
    if isinstance(value, datetime):
        return value

    if not value:
        return None

    text = str(value).strip()

    # try a couple of common formats; extend if needed
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    return None


def filter_company_blocklist(listings: Iterable[Listing], blocked: List[str]) -> List[Listing]:
    if not blocked:
        return list(listings)

    blocked_norm = [_normalize(c) for c in blocked]
    result: List[Listing] = []

    for row in listings:
        company = _normalize(str(row.get("company", "")))
        if company and any(b and b in company for b in blocked_norm):
            continue
        result.append(row)

    return result


def filter_title_allowlist(listings: Iterable[Listing], allowed_terms: List[str]) -> List[Listing]:
    if not allowed_terms:
        return list(listings)

    allowed_norm = [_normalize(t) for t in allowed_terms]
    result: List[Listing] = []

    for row in listings:
        title = _normalize(str(row.get("title", "")))
        if any(term in title for term in allowed_norm):
            result.append(row)

    return result


def filter_query_keywords(listings: Iterable[Listing], query: Optional[str]) -> List[Listing]:
    """
    Very simple keyword AND filter based on a query string, e.g.:
      'writer AND newsletter'
    We'll split on whitespace, ignore 'and'/'or', and require all remaining terms.
    """
    if not query:
        return list(listings)

    raw_terms = query.replace("AND", " ").replace("OR", " ").split()
    terms = [_normalize(t) for t in raw_terms if t.lower() not in {"and", "or"}]
    if not terms:
        return list(listings)

    result: List[Listing] = []
    for row in listings:
        haystack = " ".join(
            [
                _normalize(str(row.get("title", ""))),
                _normalize(str(row.get("description", ""))),
            ]
        )
        if all(term in haystack for term in terms):
            result.append(row)

    return result


def apply_filters(
    listings: Iterable[Listing],
    query: Optional[str] = None,
    remote_only: bool = False,
    posted_within: Optional[int] = None,
    company_block: Optional[str] = None,
    role_allow: Optional[str] = None,
) -> List[Listing]:
    """
    High-level convenience wrapper used by CLI.
    company_block and role_allow are comma-separated strings.
    """
    rows: List[Listing] = list(listings)

    rows = filter_query_keywords(rows, query)
    rows = filter_remote_only(rows, remote_only)
    rows = filter_posted_within(rows, posted_within)

    blocked = [c.strip() for c in (company_block or "").split(",") if c.strip()]
    rows = filter_company_blocklist(rows, blocked)

    allowed = [r.strip() for r in (role_allow or "").split(",") if r.strip()]
    rows = filter_title_allowlist(rows, allowed)

    return rows
