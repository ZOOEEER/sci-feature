from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
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


class Note(NoteCreate):
    id: UUID
    created_at: datetime


app = FastAPI(title="Sci Feature API", version="0.2.0")
NOTES: dict[UUID, Note] = {}


@app.on_event("startup")
def setup_schema() -> None:
    paper_repository.init_schema()
app = FastAPI(title="Sci Feature API", version="0.1.0")

PAPERS: dict[UUID, Paper] = {}
NOTES: dict[UUID, Note] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/papers", response_model=List[Paper])
def list_papers() -> List[Paper]:
    return [Paper(**item) for item in paper_repository.list_papers()]
    return list(PAPERS.values())


@app.post("/api/papers", response_model=Paper, status_code=201)
def create_paper(payload: PaperCreate) -> Paper:
    paper = Paper(id=uuid4(), created_at=datetime.utcnow(), **payload.model_dump())
    PAPERS[paper.id] = paper
    return paper


@app.get("/api/papers/{paper_id}", response_model=Paper)
def get_paper(paper_id: UUID) -> Paper:
    paper = PAPERS.get(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@app.post("/api/notes", response_model=Note, status_code=201)
def create_note(payload: NoteCreate) -> Note:
    if payload.paper_id not in PAPERS:
        raise HTTPException(status_code=404, detail="Paper not found for note")

    note = Note(id=uuid4(), created_at=datetime.utcnow(), **payload.model_dump())
    NOTES[note.id] = note
    return note


@app.get("/api/notes", response_model=List[Note])
def list_notes() -> List[Note]:
    return list(NOTES.values())
