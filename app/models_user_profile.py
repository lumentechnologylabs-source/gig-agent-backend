from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    preferred_roles: Optional[List[str]] = []
    skills: Optional[List[str]] = []
    keywords: Optional[List[str]] = []
    disqualifiers: Optional[List[str]] = []
