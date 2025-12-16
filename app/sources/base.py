from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from ..models import Gig

class Source(ABC):
    name: str

    @abstractmethod
    async def fetch(self, limit: int = 50) -> Iterable[Gig]:
        ...
