"""Week 7 graph builder for Paper-Tag relations."""

from __future__ import annotations

from collections import Counter
from typing import Any


def build_graph_payload(papers: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    tag_counter: Counter[str] = Counter()

    for paper in papers:
        paper_id = str(paper["id"])
        nodes.append(
            {
                "id": paper_id,
                "type": "paper",
                "label": paper["title"],
                "meta": {"year": paper.get("year"), "source": paper.get("source")},
            }
        )
        for tag in paper.get("tags", []):
            normalized = str(tag).strip().lower()
            if not normalized:
                continue
            tag_counter[normalized] += 1
            edges.append(
                {
                    "source": paper_id,
                    "target": f"tag:{normalized}",
                    "type": "HAS_TAG",
                }
            )

    for tag, count in tag_counter.items():
        nodes.append({"id": f"tag:{tag}", "type": "tag", "label": tag, "meta": {"count": count}})

    return {"nodes": nodes, "edges": edges}
