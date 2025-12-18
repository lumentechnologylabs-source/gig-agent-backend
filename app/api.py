from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict

from pydantic import BaseModel

from app.providers.remoteok_jobs import fetch_remoteok_jobs
from app.providers.wwr_jobs import fetch_wwr_jobs
from app.core.scoring import score_gig

print("🚀 Loaded API from C:\\dev\\gig_agent\\app\\api.py")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔹 Health check / root
@app.get("/")
async def health():
    return {
        "status": "ok",
        "message": "GigAgent backend is running.",
    }


# 🔹 Basic profile model
class Profile(BaseModel):
    name: str
    label: str
    skills: List[str]
    keywords: List[str]
    min_pay: Optional[int] = 0
    remote_only: bool = True


# 🔹 Built-in demo profiles
PROFILES: Dict[str, Profile] = {
    "cindy": Profile(
        name="cindy",
        label="Cindy – Email & Content",
        skills=["email marketing", "copywriting", "campaign strategy"],
        keywords=["email", "newsletter", "campaign", "copywriter", "content"],
        min_pay=20,
        remote_only=True,
    ),
    "creative": Profile(
        name="creative",
        label="Creative – Design & Art",
        skills=["design", "illustration", "branding"],
        keywords=["designer", "illustrator", "graphics", "branding"],
        min_pay=0,
        remote_only=True,
    ),
    "developer": Profile(
        name="developer",
        label="Developer – Web & Software",
        skills=["javascript", "python", "react", "next.js", "frontend", "backend"],
        keywords=["developer", "engineer", "software", "frontend", "full stack"],
        min_pay=30,
        remote_only=True,
    ),
    "musician": Profile(
        name="musician",
        label="Musician – Audio & Creative",
        skills=["music", "production", "audio editing"],
        keywords=["music", "audio", "sound", "podcast", "composer"],
        min_pay=0,
        remote_only=True,
    ),
    "fastgigs": Profile(
        name="fastgigs",
        label="Fast Gigs – Quick Wins",
        skills=["data entry", "typing", "admin"],
        keywords=["data entry", "assistant", "transcription", "quick"],
        min_pay=0,
        remote_only=True,
    ),
    "gentle": Profile(
        name="gentle",
        label="Gentle Mode – Low-Energy Day",
        skills=["writing", "light admin"],
        keywords=["easy", "simple", "entry", "light"],
        min_pay=0,
        remote_only=True,
    ),
}


# 🔹 Profile model for arbitrary users (used by POST /gigs/search)
class UserProfile(BaseModel):
    preferred_roles: Optional[List[str]] = []
    skills: Optional[List[str]] = []
    keywords: Optional[List[str]] = []
    disqualifiers: Optional[List[str]] = []


# 🔹 Core search logic shared by both endpoints
async def run_gig_search(user_config: dict, limit: int = 10):
    """
    Core search routine:
    - fetches raw gigs
    - filters based on user_config
    - scores and sorts
    - returns a shaped payload
    """
    print("USER CONFIG:", user_config)
    print("LIMIT:", limit)

    # 1) Fetch raw gigs from RemoteOK
    raw_remoteok: List[dict] = []
    raw_wwr: List[dict] = []

    try:
        raw_remoteok = await fetch_remoteok_jobs(limit=50)
    except Exception as e:
        print("RemoteOK fetch failed:", e)

    try:
        raw_wwr = await fetch_wwr_jobs(limit=50)
    except Exception as e:
        print("WWR fetch failed:", e)

    raw_gigs = raw_remoteok + raw_wwr
    print(
        "RAW GIGS FETCHED:",
        len(raw_gigs),
        "(remoteok:",
        len(raw_remoteok),
        "wwr:",
        len(raw_wwr),
        ")",
    )


    # 2) Filter based on disqualifiers (hard filter only)
    filtered_gigs: List[dict] = []
    disqualifiers = [d.lower() for d in user_config.get("disqualifiers", []) or []]

    for gig in raw_gigs:
        title = (gig.get("title") or gig.get("position") or "").lower()
        desc = (gig.get("description") or "").lower()
        haystack = f"{title} {desc}"

        if disqualifiers and any(bad in haystack for bad in disqualifiers):
            continue

        filtered_gigs.append(gig)

    if not filtered_gigs:
        print("No gigs after filtering, falling back to raw gigs.")
        filtered_gigs = raw_gigs

    print("FILTERED GIGS:", len(filtered_gigs))

    # 3) Score + sort using your existing scoring logic + profile keywords
    profile_keywords = [kw.lower() for kw in (user_config.get("keywords") or [])]

    scored_gigs: List[dict] = []
    for gig in filtered_gigs:
        base_score = score_gig(gig, user_config)

        title = (gig.get("title") or gig.get("position") or "").lower()
        desc = (gig.get("description") or "").lower()
        haystack = f"{title} {desc}"

        keyword_hits = sum(1 for kw in profile_keywords if kw and kw in haystack)
        boost = keyword_hits * 10  # adjust if you want stronger/weaker effect

        total_score = base_score + boost

        scored_gigs.append({**gig, "score": total_score})

    # 4) Sort and limit
    scored_gigs.sort(key=lambda g: g.get("score", 0), reverse=True)
    top_gigs = scored_gigs[:limit]

    return {
        "profile_used": user_config,
        "gigs": top_gigs,
    }


# 🔹 POST /gigs/search — rich JSON profile, used by your form (if/when needed)
@app.post("/gigs/search")
async def search_gigs_with_profile(
    profile: UserProfile,
    limit: int = 10,
):
    """
    Multi-user endpoint:
    Accepts a JSON profile body and uses it to curate gigs.
    """
    user_config = profile.dict()
    return await run_gig_search(user_config, limit)


# 🔹 GET /gigs — simple profile-key endpoint used by your UI (/api/gigs?profile=cindy)
@app.get("/gigs")
async def get_gigs(
    profile: str = Query("cindy", description="Profile key, e.g. 'cindy' or 'creative'"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Simple endpoint compatible with the older Next.js route:
    GET /gigs?profile=cindy&limit=10

    Uses the lightweight Profile system, but still goes through
    the main run_gig_search() pipeline.
    """
    profile_key = profile.lower().strip()
    profile_obj = PROFILES.get(profile_key, PROFILES["cindy"])

    user_config = {
        "preferred_roles": [profile_key],
        "skills": profile_obj.skills,
        "keywords": profile_obj.keywords,
        "disqualifiers": [],
        "min_pay": profile_obj.min_pay,
        "remote_only": profile_obj.remote_only,
    }

    return await run_gig_search(user_config, limit)
