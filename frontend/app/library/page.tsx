"use client";

import { FormEvent, useEffect, useState } from "react";

import { Nav } from "../../components/nav";

type Paper = {
  id: string;
  title: string;
  doi?: string | null;
  year?: number | null;
  tags: string[];
  source: "manual" | "doi";
  created_at: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function LibraryPage() {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [title, setTitle] = useState("");
  const [doi, setDoi] = useState("");
  const [year, setYear] = useState("");
  const [tags, setTags] = useState("");
  const [source, setSource] = useState<"manual" | "doi">("manual");

  async function loadPapers() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/api/papers`);
      if (!response.ok) {
        throw new Error("加载文献失败");
      }
      const json = (await response.json()) as Paper[];
      setPapers(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "未知错误");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadPapers();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    try {
      const response = await fetch(`${API_BASE}/api/papers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          doi: doi || null,
          year: year ? Number(year) : null,
          tags: tags
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
          source,
        }),
      });

      if (response.status === 409) {
        throw new Error("文献已存在（DOI 或标题重复）");
      }
      if (!response.ok) {
        throw new Error("创建文献失败");
      }

      setTitle("");
      setDoi("");
      setYear("");
      setTags("");
      await loadPapers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "未知错误");
    }
  }

  return (
    <main style={{ maxWidth: 1040, margin: "0 auto", padding: 24 }}>
      <header style={{ marginBottom: 16 }}>
        <h1 style={{ margin: "0 0 8px" }}>Library · 文献导入与归档</h1>
        <p style={{ margin: "0 0 12px", color: "#4b5a6a" }}>
          Week 5: 已接入 DOI/手动导入、PostgreSQL 持久化与去重规则。
        </p>
        <Nav />
      </header>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12, marginBottom: 16 }}>
        <h2 style={{ marginTop: 0 }}>新增文献</h2>
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: 10 }}>
          <input required placeholder="标题" value={title} onChange={(e) => setTitle(e.target.value)} />
          <input placeholder="DOI（可选）" value={doi} onChange={(e) => setDoi(e.target.value)} />
          <input placeholder="年份（可选）" value={year} onChange={(e) => setYear(e.target.value)} />
          <input
            placeholder="标签，逗号分隔（如 catalysis, review）"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
          />
          <select value={source} onChange={(e) => setSource(e.target.value as "manual" | "doi") }>
            <option value="manual">manual</option>
            <option value="doi">doi</option>
          </select>
          <button type="submit" style={{ width: 140 }}>保存文献</button>
        </form>
        {error ? <p style={{ color: "#b42318" }}>{error}</p> : null}
      </section>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12 }}>
        <h2 style={{ marginTop: 0 }}>文献列表</h2>
        {loading ? <p>加载中...</p> : null}
        {!loading && papers.length === 0 ? <p>暂无文献，请先导入。</p> : null}
        <ul>
          {papers.map((paper) => (
            <li key={paper.id} style={{ marginBottom: 10 }}>
              <strong>{paper.title}</strong> ({paper.year ?? "n/a"})
              <div>DOI: {paper.doi ?? "n/a"} · Source: {paper.source}</div>
              <div>Tags: {paper.tags.join(", ") || "n/a"}</div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
