# app/providers/remoteok.py

from typing import List, Dict
import httpx

REMOTEOK_API = "https://remoteok.com/api"


async def fetch_remoteok_jobs(limit: int = 25) -> List[Dict]:
    """
    Fetch jobs from the RemoteOK API and return a list of normalized gig dicts.
    """
    async with httpx.AsyncClient(timeout=30.0, headers={"User-Agent": "gig-agent/0.1"}) as client:
        resp = await client.get(REMOTEOK_API)
        resp.raise_for_status()
        data = resp.json()

    # RemoteOK has a metadata element at index 0, then jobs
    jobs_raw = data[1:] if data and isinstance(data, list) else data

    gigs: List[Dict] = []
    for job in jobs_raw[:limit]:
        gigs.append(
            {
                "source": "remoteok",
                "id": job.get("id"),
                "position": job.get("position"),
                "company": job.get("company"),
                "tags": job.get("tags", []),
                "url": job.get("url") or job.get("apply_url"),
                "description": job.get("description"),
                "location": job.get("location") or "Remote",
                "salary": job.get("salary") or job.get("compensation"),
            }
        )
    return gigs
