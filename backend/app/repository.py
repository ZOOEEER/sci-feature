from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from .notes import NoteRow, normalize_note_text
from .papers import DuplicatePaperError, PaperRow, normalize_doi, normalize_title


class PaperRepository:
    """PostgreSQL-backed paper repository (Week 5)."""

    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = dsn or os.getenv(
            "DATABASE_URL", "postgresql://sci:sci@localhost:5432/sci_feature"
        )

    def _connect(self):
        try:
            import psycopg
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise RuntimeError(
                "psycopg is required for PostgreSQL persistence. Install backend requirements first."
            ) from exc
        return psycopg.connect(self._dsn)

    def init_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS papers (
                      id UUID PRIMARY KEY,
                      title TEXT NOT NULL,
                      title_normalized TEXT NOT NULL,
                      doi TEXT,
                      year INT,
                      tags JSONB NOT NULL DEFAULT '[]'::jsonb,
                      source TEXT NOT NULL,
                      created_at TIMESTAMPTZ NOT NULL
                    );
                    """
                )
                cur.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_papers_title_normalized ON papers (title_normalized);"
                )
                cur.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_papers_doi_lower ON papers ((lower(doi))) WHERE doi IS NOT NULL;"
                )
            conn.commit()


    def init_note_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                      id UUID PRIMARY KEY,
                      paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
                      research_question TEXT NOT NULL DEFAULT '',
                      method TEXT NOT NULL DEFAULT '',
                      result TEXT NOT NULL DEFAULT '',
                      limitation TEXT NOT NULL DEFAULT '',
                      insight TEXT NOT NULL DEFAULT '',
                      created_at TIMESTAMPTZ NOT NULL
                    );
                    """
                )
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_notes_paper_id_created_at ON notes (paper_id, created_at DESC);"
                )
            conn.commit()

    def list_papers(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, title_normalized, doi, year, tags, source, created_at
                    FROM papers
                    ORDER BY created_at DESC;
                    """
                )
                rows = cur.fetchall()

        mapped = [
            PaperRow(
                id=row[0],
                title=row[1],
                title_normalized=row[2],
                doi=row[3],
                year=row[4],
                tags=row[5] if isinstance(row[5], list) else [],
                source=row[6],
                created_at=row[7],
            )
            for row in rows
        ]
        return [
            {
                "id": item.id,
                "title": item.title,
                "doi": item.doi,
                "year": item.year,
                "tags": item.tags,
                "source": item.source,
                "created_at": item.created_at,
            }
            for item in mapped
        ]

    def create_paper(
        self,
        *,
        title: str,
        doi: str | None,
        year: int | None,
        tags: list[str],
        source: str,
    ) -> dict[str, Any]:
        payload = {
            "id": uuid4(),
            "title": title.strip(),
            "title_normalized": normalize_title(title),
            "doi": normalize_doi(doi),
            "year": year,
            "tags": json.dumps(tags),
            "source": source,
            "created_at": datetime.utcnow(),
        }

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO papers (id, title, title_normalized, doi, year, tags, source, created_at)
                        VALUES (%(id)s, %(title)s, %(title_normalized)s, %(doi)s, %(year)s, %(tags)s::jsonb, %(source)s, %(created_at)s)
                        RETURNING id, title, doi, year, tags, source, created_at;
                        """,
                        payload,
                    )
                    row = cur.fetchone()
                conn.commit()
        except Exception as exc:  # pragma: no cover
            if "idx_papers_title_normalized" in str(exc) or "idx_papers_doi_lower" in str(exc):
                raise DuplicatePaperError("paper already exists") from exc
            raise

        return {
            "id": row[0],
            "title": row[1],
            "doi": row[2],
            "year": row[3],
            "tags": row[4] if isinstance(row[4], list) else [],
            "source": row[5],
            "created_at": row[6],
        }


    def create_note(
        self,
        *,
        paper_id: UUID,
        research_question: str,
        method: str,
        result: str,
        limitation: str,
        insight: str,
    ) -> dict[str, Any]:
        payload = {
            "id": uuid4(),
            "paper_id": paper_id,
            "research_question": normalize_note_text(research_question),
            "method": normalize_note_text(method),
            "result": normalize_note_text(result),
            "limitation": normalize_note_text(limitation),
            "insight": normalize_note_text(insight),
            "created_at": datetime.utcnow(),
        }

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO notes (id, paper_id, research_question, method, result, limitation, insight, created_at)
                    VALUES (%(id)s, %(paper_id)s, %(research_question)s, %(method)s, %(result)s, %(limitation)s, %(insight)s, %(created_at)s)
                    RETURNING id, paper_id, research_question, method, result, limitation, insight, created_at;
                    """,
                    payload,
                )
                row = cur.fetchone()
            conn.commit()

        return {
            "id": row[0],
            "paper_id": row[1],
            "research_question": row[2],
            "method": row[3],
            "result": row[4],
            "limitation": row[5],
            "insight": row[6],
            "created_at": row[7],
        }

    def list_notes(self, *, paper_id: UUID | None = None) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                if paper_id is not None:
                    cur.execute(
                        """
                        SELECT id, paper_id, research_question, method, result, limitation, insight, created_at
                        FROM notes
                        WHERE paper_id = %s
                        ORDER BY created_at DESC;
                        """,
                        (paper_id,),
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, paper_id, research_question, method, result, limitation, insight, created_at
                        FROM notes
                        ORDER BY created_at DESC;
                        """
                    )
                rows = cur.fetchall()

        mapped = [
            NoteRow(
                id=row[0],
                paper_id=row[1],
                research_question=row[2],
                method=row[3],
                result=row[4],
                limitation=row[5],
                insight=row[6],
                created_at=row[7],
            )
            for row in rows
        ]

        return [
            {
                "id": item.id,
                "paper_id": item.paper_id,
                "research_question": item.research_question,
                "method": item.method,
                "result": item.result,
                "limitation": item.limitation,
                "insight": item.insight,
                "created_at": item.created_at,
            }
            for item in mapped
        ]

paper_repository = PaperRepository()
