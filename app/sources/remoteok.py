"""
remoteok.py

Heuristically decide whether a gig looks remote-friendly.

Usage (CLI):
    python -m app.sources.remoteok "Job description text here"
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List

class WorkMode(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


@dataclass
class RemoteCheckResult:
    is_remote_ok: bool
    mode: WorkMode
    confidence: float  # 0.0 – 1.0, rough heuristic
    reasons: List[str]
    flags: Dict[str, bool]

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["mode"] = self.mode.value
        return data


# --- Keyword groups ---------------------------------------------------------

POSITIVE_REMOTE = [
    r"\bremote\b",
    r"work from home",
    r"work\-from\-home",
    r"fully remote",
    r"100% remote",
    r"work from anywhere",
    r"distributed team",
    r"telecommute",
    r"telecommuting",
    r"home\-based",
]

HYBRID_HINTS = [
    r"\bhybrid\b",
    r"\b2 days in (the )?office\b",
    r"\b3 days in (the )?office\b",
    r"\b\d+ days in (the )?office\b",
    r"\bon[- ]site\b.*\b(\d|one|two|three)\s+days\b",
]

NEGATIVE_REMOTE = [
    r"\bno remote\b",
    r"\bnot remote\b",
    r"\bremote not available\b",
    r"\bremote work (is )?not (available|offered)\b",
    r"\bmust be on[- ]site\b",
    r"\bmust be in[- ]office\b",
    r"\b(on[- ]site|in[- ]office) only\b",
    r"\brelocation required\b",
    r"\blocated in [A-Za-z ]+ (office|campus)\b",
]

LOCAL_ONLY = [
    r"\blocal candidates only\b",
    r"\bmust live within\b",
    r"\bwithin \d+\s*(miles|km|kilometers)\b",
]


def _compile(patterns: List[str]) -> List[re.Pattern]:
    return [re.compile(p, re.IGNORECASE) for p in patterns]


POSITIVE_REMOTE_RE = _compile(POSITIVE_REMOTE)
HYBRID_HINTS_RE = _compile(HYBRID_HINTS)
NEGATIVE_REMOTE_RE = _compile(NEGATIVE_REMOTE)
LOCAL_ONLY_RE = _compile(LOCAL_ONLY)


# --- Core logic -------------------------------------------------------------


def _count_matches(regexes: List[re.Pattern], text: str) -> int:
    return sum(1 for r in regexes if r.search(text))


def score_remote(text: str) -> RemoteCheckResult:
    """
    Inspect a job/gig text and guess whether it's remote-friendly.
    """

    normalized = " ".join(text.split())  # collapse whitespace

    pos_count = _count_matches(POSITIVE_REMOTE_RE, normalized)
    hybrid_count = _count_matches(HYBRID_HINTS_RE, normalized)
    neg_count = _count_matches(NEGATIVE_REMOTE_RE, normalized)
    local_count = _count_matches(LOCAL_ONLY_RE, normalized)

    flags: Dict[str, bool] = {
        "has_positive_remote": pos_count > 0,
        "has_hybrid_hints": hybrid_count > 0,
        "has_negative_remote": neg_count > 0,
        "has_local_only": local_count > 0,
    }

    reasons: List[str] = []

    # 1) Hard negatives: not remote-friendly
    if flags["has_negative_remote"] or flags["has_local_only"]:
        mode = WorkMode.ONSITE
        is_remote_ok = False
        confidence = 0.9
        if flags["has_negative_remote"]:
            reasons.append("Explicit language that remote is not available.")
        if flags["has_local_only"]:
            reasons.append("Local/relocation-only language detected.")
        return RemoteCheckResult(
            is_remote_ok=is_remote_ok,
            mode=mode,
            confidence=confidence,
            reasons=reasons or ["Appears to be on-site only."],
            flags=flags,
        )

    # 2) Hybrid signals
    if flags["has_hybrid_hints"] and flags["has_positive_remote"]:
        mode = WorkMode.HYBRID
        is_remote_ok = True  # partial remote
        confidence = 0.85
        reasons.append("Mentions remote plus in-office days (likely hybrid).")
    elif flags["has_hybrid_hints"]:
        mode = WorkMode.HYBRID
        is_remote_ok = True
        confidence = 0.75
        reasons.append("Hybrid language detected (some in-office expected).")
    # 3) Strong remote signals
    elif flags["has_positive_remote"]:
        mode = WorkMode.REMOTE
        is_remote_ok = True
        confidence = 0.8 if pos_count == 1 else 0.9
        reasons.append("Remote-friendly language detected.")
    else:
        # 4) Unknown, no clear signals
        mode = WorkMode.UNKNOWN
        is_remote_ok = False
        confidence = 0.4
        reasons.append("No clear remote/onsite language found; treating as unknown.")

    return RemoteCheckResult(
        is_remote_ok=is_remote_ok,
        mode=mode,
        confidence=confidence,
        reasons=reasons,
        flags=flags,
    )


def is_remote_ok(text: str, *, require_strict_remote: bool = False) -> bool:
    """
    Simple boolean check.

    If require_strict_remote=True, only 'remote' is accepted.
    If False (default), 'remote' or 'hybrid' count as okay.
    """
    result = score_remote(text)
    if require_strict_remote:
        return result.mode == WorkMode.REMOTE
    return result.mode in {WorkMode.REMOTE, WorkMode.HYBRID}


# --- Tiny CLI for quick testing --------------------------------------------


def _cli(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python -m app.sources.remoteok \"job description text...\"")
        return 1

    text = " ".join(argv[1:])
    result = score_remote(text)
    print("Mode      :", result.mode.value)
    print("Remote OK :", result.is_remote_ok)
    print("Confidence:", f"{result.confidence:.2f}")
    print("Reasons   :")
    for r in result.reasons:
        print("  -", r)
    print("Flags     :", result.flags)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv))
