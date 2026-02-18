const navItems = [
  "Dashboard",
  "Library",
  "Reader",
  "Graph",
  "Writer",
];

export function Nav() {
  return (
    <nav style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
      {navItems.map((item) => (
        <span
          key={item}
          style={{
            padding: "6px 10px",
            borderRadius: 8,
            background: "#e8eefb",
            fontSize: 14,
            fontWeight: 600,
          }}
        >
          {item}
        </span>
      ))}
    </nav>
  );
}
