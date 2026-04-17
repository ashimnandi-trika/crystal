"""Base types for Crystal Guard analyzers."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def points(self) -> int:
        return {"critical": 15, "high": 8, "medium": 4, "low": 2}[self.value]

    @property
    def rank(self) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}[self.value]


@dataclass
class Issue:
    analyzer: str
    severity: str
    file: str
    line: int | None
    rule_id: str
    message: str
    suggestion: str
    why: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def severity_enum(self) -> Severity:
        return Severity(self.severity)
