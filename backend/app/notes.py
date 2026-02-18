"""Week 6 note domain helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class NoteRow:
    id: UUID
    paper_id: UUID
    research_question: str = ""
    method: str = ""
    result: str = ""
    limitation: str = ""
    insight: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


def normalize_note_text(value: str) -> str:
    return value.strip()
