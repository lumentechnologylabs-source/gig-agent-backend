from __future__ import annotations
from datetime import datetime, timedelta
import re
from typing import List, Dict, Any, Iterable

def accept(listing, *args, **kwargs) -> bool:
    """
    Backwards-compatibility shim for older code that imported `accept`
    from filters. For now, we just accept all listings.
    New code should use `apply_filters` instead.
    """
    return True


def dedupe_listings(listings: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate listings based on a composite key of (source, id, url, title).
    This is defensive and will work even if some fields are missing.
    """
    seen = set()
    result = []
    for item in listings:
        key = (
            item.get("source"),
            item.get("id"),
            item.get("url"),
            item.get("title"),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _matches_query(listing: Dict[str, Any], query: str) -> bool:
    """
    Very simple query matcher:
    - supports 'AND' between terms
    - otherwise treats it as space-separated terms
    - matches against title + company + description text
    """
    if not query:
        return True

    text_parts = [
        listing.get("title", ""),
        listing.get("company", ""),
        listing.get("description", ""),
    ]
    haystack = " ".join(p for p in text_parts if p).lower()

    # split on 'AND' first
    and_parts = [part.strip() for part in query.split("AND")]
    for part in and_parts:
        if not part:
            continue
        # each part may have multiple words; all must appear
        words = part.lower().split()
        if not all(word in haystack for word in words):
            return False

    return True


def _is_remote(listing: Dict[str, Any]) -> bool:
    """
    Try to infer 'remote' from fields.
    Looks for:
      - explicit boolean flags
      - 'remote' in location or title fields
    """
    if listing.get("is_remote") is True:
        return True

    location = (listing.get("location") or "").lower()
    title = (listing.get("title") or "").lower()

    if "remote" in location or "remote" in title:
        return True

    return False


def _within_days(listing: Dict[str, Any], days: int) -> bool:
    """
    Filter listing by an approximate 'posted within N days' rule.
    Tries posted_at or date-like fields.
    """
    if not days or days <= 0:
        return True

    # Look for a few common date fields
    raw = (
        listing.get("posted_at")
        or listing.get("date")
        or listing.get("created_at")
        or listing.get("published_at")
    )
    if not raw:
        # No date info → keep it by default (we can adjust later)
        return True

    # Try a couple of basic parse strategies
    dt = None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(raw, fmt)
            break
        except Exception:
            continue

    if dt is None:
        # Unknown format → keep it for now
        return True

    cutoff = datetime.utcnow() - timedelta(days=days)
    # naive vs aware safety: compare using .timestamp()
    return dt.timestamp() >= cutoff.timestamp()


def _blocked_company(listing: Dict[str, Any], blocked: Iterable[str]) -> bool:
    """
    Returns True if listing's company matches any blocked name fragment.
    """
    company = (listing.get("company") or "").lower()
    for b in blocked:
        b = b.strip().lower()
        if not b:
            continue
        if b in company:
            return True
    return False


def _role_allowed(listing: Dict[str, Any], allowed: Iterable[str]) -> bool:
    """
    Returns True if listing's title matches any allowed role fragment.
    If 'allowed' is empty, everything is allowed.
    """
    allowed = [a.strip().lower() for a in allowed if a.strip()]
    if not allowed:
        return True

    title = (listing.get("title") or "").lower()
    for a in allowed:
        if a in title:
            return True
    return False


def apply_filters(
    listings: Iterable[Dict[str, Any]],
    query: str | None = None,
    remote_only: bool = False,
    posted_within: int | None = None,
    company_block: str | None = None,
    role_allow: str | None = None,
) -> List[Dict[str, Any]]:
    """
    Apply a pipeline of filters to the listing set.

    - query: simple AND query across title/company/description
    - remote_only: keep only remote-friendly roles
    - posted_within: keep jobs posted within N days (best-effort)
    - company_block: comma-separated list of company name fragments to exclude
    - role_allow: comma-separated list of role fragments to include
    """
    result = list(listings)

    # Text query
    if query:
        result = [l for l in result if _matches_query(l, query)]

    # Remote only
    if remote_only:
        result = [l for l in result if _is_remote(l)]

    # Posted within N days
    if posted_within:
        result = [l for l in result if _within_days(l, posted_within)]

    # Company blocklist
    blocked = []
    if company_block:
        blocked = [c.strip() for c in company_block.split(",") if c.strip()]
        if blocked:
            result = [l for l in result if not _blocked_company(l, blocked)]

    # Role allow-list
    allowed = []
    if role_allow:
        allowed = [r.strip() for r in role_allow.split(",") if r.strip()]
        if allowed:
            result = [l for l in result if _role_allowed(l, allowed)]

    return result
