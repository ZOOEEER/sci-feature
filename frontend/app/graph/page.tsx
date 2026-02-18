"use client";

import { useEffect, useState } from "react";

import { Nav } from "../../components/nav";

type GraphNode = { id: string; type: string; label: string; meta?: Record<string, unknown> };
type GraphEdge = { source: string; target: string; type: string };

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function GraphPage() {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadGraph() {
      try {
        const response = await fetch(`${API_BASE}/api/graph`);
        if (!response.ok) {
          throw new Error("加载图谱失败");
        }
        const payload = (await response.json()) as { nodes: GraphNode[]; edges: GraphEdge[] };
        setNodes(payload.nodes);
        setEdges(payload.edges);
      } catch (err) {
        setError(err instanceof Error ? err.message : "未知错误");
      }
    }
    void loadGraph();
  }, []);

  return (
    <main style={{ maxWidth: 1040, margin: "0 auto", padding: 24 }}>
      <header style={{ marginBottom: 16 }}>
        <h1 style={{ margin: "0 0 8px" }}>Graph · 文献标签关系图</h1>
        <p style={{ margin: "0 0 12px", color: "#4b5a6a" }}>
          Week 7: 已打通 Paper-Tag 关系图数据接口与可视化列表。
        </p>
        <Nav />
      </header>

      {error ? <p style={{ color: "#b42318" }}>{error}</p> : null}

      <section style={{ background: "#fff", padding: 16, borderRadius: 12, marginBottom: 16 }}>
        <h2 style={{ marginTop: 0 }}>Nodes ({nodes.length})</h2>
        <ul>
          {nodes.map((node) => (
            <li key={node.id}>
              <strong>{node.label}</strong> [{node.type}] ({node.id})
            </li>
          ))}
        </ul>
      </section>

      <section style={{ background: "#fff", padding: 16, borderRadius: 12 }}>
        <h2 style={{ marginTop: 0 }}>Edges ({edges.length})</h2>
        <ul>
          {edges.map((edge, idx) => (
            <li key={`${edge.source}-${edge.target}-${idx}`}>
              {edge.source} --{edge.type}→ {edge.target}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
