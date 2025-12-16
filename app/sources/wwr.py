from __future__ import annotations
import feedparser, re
from typing import Iterable, List
from bs4 import BeautifulSoup
from ..models import Gig
from .base import Source

# We Work Remotely RSS feeds (example: all programming)
# You may add more categories or targeted searches as needed.
WWR_RSS = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(" ", strip=True)

class WeWorkRemotely(Source):
    name = "weworkremotely"

    async def fetch(self, limit: int = 50) -> Iterable[Gig]:
        feed = feedparser.parse(WWR_RSS)
        gigs: List[Gig] = []
        for entry in feed.entries[:limit]:
            desc = _extract_text(getattr(entry, "summary", ""))
            g = Gig(
                id=f"wwr-{getattr(entry, 'id', getattr(entry, 'link', str(hash(entry.title))))}",
                title=entry.title,
                company=None,
                url=entry.link,
                source=self.name,
                location=None,
                remote=True,
                tags=[],
                description=desc,
                pay=None,
                contract=True,
            )
            gigs.append(g)
        return gigs
