from __future__ import annotations
from fastapi import FastAPI, Query
from typing import List
import asyncio

from .models import ScoredGig, Gig
from .sources.remoteok import RemoteOK
from .sources.wwr import WeWorkRemotely
from .scoring import rank_gigs
from .filters import accept

app = FastAPI(title="Gig Agent", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/gigs", response_model=List[ScoredGig])
async def gigs(limit: int = Query(25, ge=1, le=200)):
    sources = [RemoteOK(), WeWorkRemotely()]
    results: List[Gig] = []
    fetched = await asyncio.gather(*[s.fetch(limit=limit) for s in sources])
    for group in fetched:
        for g in group:
            if accept(g):
                results.append(g)
    ranked = rank_gigs(results)[:limit]
    return ranked
