"""Domain layer for offline-testable research entities.

This module intentionally has zero third-party dependencies so it can be
validated in restricted environments without network package installation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import UUID, uuid4


@dataclass(slots=True)
class PaperRecord:
    id: UUID
    title: str
    doi: str | None = None
    year: int | None = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


class DuplicatePaperError(ValueError):
    """Raised when trying to add an existing paper by DOI or normalized title."""


class PaperStore:
    def __init__(self) -> None:
        self._papers: Dict[UUID, PaperRecord] = {}

    @staticmethod
    def _normalize_title(title: str) -> str:
        return " ".join(title.lower().split())

    def add_paper(
        self,
        *,
        title: str,
        doi: str | None = None,
        year: int | None = None,
        tags: List[str] | None = None,
    ) -> PaperRecord:
        clean_title = self._normalize_title(title)
        for existing in self._papers.values():
            if doi and existing.doi and doi.strip().lower() == existing.doi.strip().lower():
                raise DuplicatePaperError("duplicate doi")
            if clean_title == self._normalize_title(existing.title):
                raise DuplicatePaperError("duplicate title")

        paper = PaperRecord(
            id=uuid4(),
            title=title,
            doi=doi,
            year=year,
            tags=tags or [],
        )
        self._papers[paper.id] = paper
        return paper

    def list_papers(self) -> List[PaperRecord]:
        return list(self._papers.values())
