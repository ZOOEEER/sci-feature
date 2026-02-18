"""Offline executable API contract layer.

This mirrors core request/response semantics of the HTTP API so tests can run
in restricted environments without FastAPI/TestClient installation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from .domain import DuplicatePaperError, PaperStore


@dataclass(slots=True)
class NoteRecord:
    id: UUID
    paper_id: UUID
    research_question: str = ""
    method: str = ""
    result: str = ""
    limitation: str = ""
    insight: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


class ApiContractService:
    """In-memory service used by executable API contract tests."""

    def __init__(self) -> None:
        self._papers = PaperStore()
        self._notes: list[NoteRecord] = []

    def create_paper(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        title = str(payload.get("title", "")).strip()
        if len(title) < 3:
            return 422, {"detail": "title must have at least 3 characters"}

        source = payload.get("source", "manual")
        if source not in {"manual", "doi"}:
            return 422, {"detail": "source must be one of: manual, doi"}

        try:
            paper = self._papers.add_paper(
                title=title,
                doi=payload.get("doi"),
                year=payload.get("year"),
                tags=payload.get("tags") or [],
            )
        except DuplicatePaperError:
            return 409, {"detail": "Paper already exists"}

        return 201, {
            "id": str(paper.id),
            "title": paper.title,
            "doi": paper.doi,
            "year": paper.year,
            "tags": paper.tags,
            "source": source,
            "created_at": paper.created_at.isoformat(),
        }

    def list_papers(self) -> tuple[int, list[dict[str, Any]]]:
        items = [
            {
                "id": str(p.id),
                "title": p.title,
                "doi": p.doi,
                "year": p.year,
                "tags": p.tags,
                "source": "manual",
                "created_at": p.created_at.isoformat(),
            }
            for p in self._papers.list_papers()
        ]
        return 200, items

    def create_note(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        try:
            paper_id = UUID(str(payload.get("paper_id")))
        except Exception:
            return 422, {"detail": "paper_id is invalid"}

        paper_ids = {p.id for p in self._papers.list_papers()}
        if paper_id not in paper_ids:
            return 404, {"detail": "Paper not found"}

        note = NoteRecord(
            id=uuid4(),
            paper_id=paper_id,
            research_question=str(payload.get("research_question", "")).strip(),
            method=str(payload.get("method", "")).strip(),
            result=str(payload.get("result", "")).strip(),
            limitation=str(payload.get("limitation", "")).strip(),
            insight=str(payload.get("insight", "")).strip(),
        )
        self._notes.append(note)
        return 201, {
            "id": str(note.id),
            "paper_id": str(note.paper_id),
            "research_question": note.research_question,
            "method": note.method,
            "result": note.result,
            "limitation": note.limitation,
            "insight": note.insight,
            "created_at": note.created_at.isoformat(),
        }

    def list_notes(self, *, paper_id: str | None = None) -> tuple[int, list[dict[str, Any]]]:
        items = self._notes
        if paper_id:
            items = [n for n in items if str(n.paper_id) == paper_id]

        return 200, [
            {
                "id": str(note.id),
                "paper_id": str(note.paper_id),
                "research_question": note.research_question,
                "method": note.method,
                "result": note.result,
                "limitation": note.limitation,
                "insight": note.insight,
                "created_at": note.created_at.isoformat(),
            }
            for note in items
        ]
