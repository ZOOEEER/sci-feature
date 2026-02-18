"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import { Nav } from "../../components/nav";

type Paper = {
  id: string;
  title: string;
};

type Note = {
  id: string;
  paper_id: string;
  research_question: string;
  method: string;
  result: string;
  limitation: string;
  insight: string;
  created_at: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function ReaderPage() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [selectedPaperId, setSelectedPaperId] = useState("");
  const [notes, setNotes] = useState<Note[]>([]);
  const [error, setError] = useState("");

  const [researchQuestion, setResearchQuestion] = useState("");
  const [method, setMethod] = useState("");
  const [result, setResult] = useState("");
  const [limitation, setLimitation] = useState("");
  const [insight, setInsight] = useState("");

  async function loadPapers() {
    const res = await fetch(`${API_BASE}/api/papers`);
    if (!res.ok) {
      throw new Error("加载文献失败");
    }
    const items = (await res.json()) as Paper[];
    setPapers(items);
    if (!selectedPaperId && items.length > 0) {
      setSelectedPaperId(items[0].id);
    }
  }

  async function loadNotes(paperId?: string) {
    if (!paperId) {
      setNotes([]);
      return;
    }
    const res = await fetch(`${API_BASE}/api/notes?paper_id=${paperId}`);
    if (!res.ok) {
      throw new Error("加载笔记失败");
    }
    setNotes((await res.json()) as Note[]);
  }

  useEffect(() => {
    loadPapers().catch((err) => setError(err instanceof Error ? err.message : "未知错误"));
  }, []);

  useEffect(() => {
    loadNotes(selectedPaperId).catch((err) => setError(err instanceof Error ? err.message : "未知错误"));
  }, [selectedPaperId]);

  const selectedPaper = useMemo(
    () => papers.find((paper) => paper.id === selectedPaperId),
    [papers, selectedPaperId],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedPaperId) {
      setError("请先选择文献");
      return;
    }

    setError("");
    const response = await fetch(`${API_BASE}/api/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        paper_id: selectedPaperId,
        research_question: researchQuestion,
        method,
        result,
        limitation,
        insight,
      }),
    });

    if (!response.ok) {
      setError("保存笔记失败");
      return;
    }

    setResearchQuestion("");
    setMethod("");
    setResult("");
    setLimitation("");
    setInsight("");
    await loadNotes(selectedPaperId);
  }

  return (
    <main style={{ maxWidth: 1040, margin: "0 auto", padding: 24 }}>
      <header style={{ marginBottom: 16 }}>
        <h1 style={{ margin: "0 0 8px" }}>Reader · 结构化阅读笔记</h1>
        <p style={{ margin: "0 0 12px", color: "#4b5a6a" }}>
          Week 6: 按文献记录研究问题、方法、结果、局限和启发。
        </p>
        <Nav />
      </header>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12, marginBottom: 16 }}>
        <h2 style={{ marginTop: 0 }}>选择文献</h2>
        <select
          value={selectedPaperId}
          onChange={(e) => setSelectedPaperId(e.target.value)}
          style={{ minWidth: 360 }}
        >
          <option value="">-- 请选择 --</option>
          {papers.map((paper) => (
            <option key={paper.id} value={paper.id}>
              {paper.title}
            </option>
          ))}
        </select>
        {selectedPaper ? <p>当前文献：{selectedPaper.title}</p> : null}
      </section>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12, marginBottom: 16 }}>
        <h2 style={{ marginTop: 0 }}>新增笔记</h2>
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: 10 }}>
          <textarea placeholder="研究问题" value={researchQuestion} onChange={(e) => setResearchQuestion(e.target.value)} />
          <textarea placeholder="方法" value={method} onChange={(e) => setMethod(e.target.value)} />
          <textarea placeholder="结果" value={result} onChange={(e) => setResult(e.target.value)} />
          <textarea placeholder="局限" value={limitation} onChange={(e) => setLimitation(e.target.value)} />
          <textarea placeholder="启发" value={insight} onChange={(e) => setInsight(e.target.value)} />
          <button type="submit" style={{ width: 140 }}>保存笔记</button>
        </form>
        {error ? <p style={{ color: "#b42318" }}>{error}</p> : null}
      </section>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12 }}>
        <h2 style={{ marginTop: 0 }}>笔记列表</h2>
        {notes.length === 0 ? <p>暂无笔记。</p> : null}
        <ul>
          {notes.map((note) => (
            <li key={note.id} style={{ marginBottom: 12 }}>
              <div><strong>RQ:</strong> {note.research_question || "n/a"}</div>
              <div><strong>Method:</strong> {note.method || "n/a"}</div>
              <div><strong>Result:</strong> {note.result || "n/a"}</div>
              <div><strong>Limitation:</strong> {note.limitation || "n/a"}</div>
              <div><strong>Insight:</strong> {note.insight || "n/a"}</div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
