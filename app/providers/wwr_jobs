from __future__ import annotations

from typing import List, Dict, Optional, Tuple

import feedparser
from bs4 import BeautifulSoup

# WWR has an "all jobs" feed plus category feeds.
WWR_FEEDS = [
    "https://weworkremotely.com/remote-jobs.rss",  # all jobs
    # Or use category-specific feeds later to reduce noise:
    # "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    # "https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss",
]

def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(" ", strip=True)

def _parse_title_company(raw_title: str) -> Tuple[str, Optional[str]]:
    # Common WWR RSS title format: "Company: Role"
    if not raw_title:
        return "", None
    if ": " in raw_title:
        company, title = raw_title.split(": ", 1)
        return title.strip(), (company.strip() or None)
    return raw_title.strip(), None

async def fetch_wwr_jobs(limit: int = 50) -> List[Dict]:
    gigs: List[Dict] = []

    for url in WWR_FEEDS:
        feed = feedparser.parse(url)  # blocking but okay for now; we can thread later
        for entry in getattr(feed, "entries", []):
            if len(gigs) >= limit:
                break

            link = getattr(entry, "link", None)
            if not link:
                continue

            raw_title = getattr(entry, "title", "") or ""
            title, company = _parse_title_company(raw_title)

            desc = _extract_text(getattr(entry, "summary", ""))

            gigs.append(
            {
                "source": "weworkremotely",
                "id": f"wwr-{getattr(entry, 'id', None) or link}",
                "position": title,          # match RemoteOK schema
                "title": title,             # optional convenience; ok to keep both
                "company": company,
                "tags": [],
                "url": link,
                "description": desc,
                "location": "Remote",       # nicer than None for display
                "salary": None,             # match RemoteOK schema
                "remote": True,
            }
    )


    return gigs
