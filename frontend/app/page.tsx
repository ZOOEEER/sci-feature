import { Nav } from "../components/nav";
import { milestones, todayTasks } from "../lib/data";

const cardStyle: React.CSSProperties = {
  background: "#fff",
  borderRadius: 12,
  padding: 16,
  boxShadow: "0 1px 3px rgba(24,32,42,.1)",
};

export default function HomePage() {
  return (
    <main style={{ maxWidth: 1040, margin: "0 auto", padding: 24 }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ margin: "0 0 8px", fontSize: 28 }}>Sci Feature Workspace</h1>
        <p style={{ margin: "0 0 14px", color: "#4b5a6a" }}>
          从文献检索、阅读整理到关系图谱与综述输出的一体化科研工作台（开发启动版本）。
        </p>
        <Nav />
      </header>

      <section style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }}>
        <article style={cardStyle}>
          <h2 style={{ marginTop: 0 }}>今日开发任务</h2>
          <ul>
            {todayTasks.map((task) => (
              <li key={task}>{task}</li>
            ))}
          </ul>
        </article>

        <article style={cardStyle}>
          <h2 style={{ marginTop: 0 }}>12周里程碑</h2>
          <ol>
            {milestones.map((ms) => (
              <li key={ms}>{ms}</li>
            ))}
          </ol>
        </article>
      </section>
    </main>
  );
}
