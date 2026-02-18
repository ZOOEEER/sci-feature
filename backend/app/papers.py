"""Week 5 paper persistence and deduplication helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


class DuplicatePaperError(ValueError):
    """Raised when paper DOI/title already exists."""


@dataclass(slots=True)
class PaperRow:
    id: UUID
    title: str
    title_normalized: str
    doi: str | None
    year: int | None
    tags: list[str]
    source: str
    created_at: datetime


def normalize_title(value: str) -> str:
    return " ".join(value.lower().split())


def normalize_doi(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized or None


def row_to_paper_dict(row: PaperRow) -> dict[str, Any]:
    return {
        "id": str(row.id),
        "title": row.title,
        "doi": row.doi,
        "year": row.year,
        "tags": row.tags,
        "source": row.source,
        "created_at": row.created_at,
    }
