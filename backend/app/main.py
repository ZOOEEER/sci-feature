from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from .papers import DuplicatePaperError
from .repository import paper_repository


class PaperCreate(BaseModel):
    title: str = Field(min_length=3)
    doi: str | None = None
    year: int | None = None
    tags: List[str] = Field(default_factory=list)
    source: str = Field(default="manual", pattern="^(manual|doi)$")


class Paper(PaperCreate):
    id: UUID
    created_at: datetime


class NoteCreate(BaseModel):
    paper_id: UUID
    research_question: str = ""
    method: str = ""
    result: str = ""
    limitation: str = ""
    insight: str = ""


class Note(NoteCreate):
    id: UUID
    created_at: datetime


app = FastAPI(title="Sci Feature API", version="0.3.0")


@app.on_event("startup")
def setup_schema() -> None:
    paper_repository.init_schema()
    paper_repository.init_note_schema()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/papers", response_model=List[Paper])
def list_papers() -> List[Paper]:
    return [Paper(**item) for item in paper_repository.list_papers()]


@app.post("/api/papers", response_model=Paper, status_code=201)
def create_paper(payload: PaperCreate) -> Paper:
    try:
        created = paper_repository.create_paper(
            title=payload.title,
            doi=payload.doi,
            year=payload.year,
            tags=payload.tags,
            source=payload.source,
        )
    except DuplicatePaperError as exc:
        raise HTTPException(status_code=409, detail="Paper already exists") from exc

    return Paper(**created)


@app.post("/api/notes", response_model=Note, status_code=201)
def create_note(payload: NoteCreate) -> Note:
    note = paper_repository.create_note(
        paper_id=payload.paper_id,
        research_question=payload.research_question,
        method=payload.method,
        result=payload.result,
        limitation=payload.limitation,
        insight=payload.insight,
    )
    return Note(**note)


@app.get("/api/notes", response_model=List[Note])
def list_notes(paper_id: UUID | None = Query(default=None)) -> List[Note]:
    return [Note(**item) for item in paper_repository.list_notes(paper_id=paper_id)]
