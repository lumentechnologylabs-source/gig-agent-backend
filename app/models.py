from __future__ import annotations
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class Gig(BaseModel):
    id: str
    title: str
    company: str | None = None
    url: HttpUrl
    source: str
    location: str | None = None
    remote: bool = True
    tags: list[str] = []
    description: str | None = None
    pay: float | None = None  # hourly USD if parsed
    contract: bool = True

class ScoredGig(Gig):
    score: float
