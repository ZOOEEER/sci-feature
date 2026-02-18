import Link from "next/link";

const navItems = [
  { label: "Dashboard", href: "/" },
  { label: "Library", href: "/library" },
  { label: "Reader", href: "/reader" },
  { label: "Graph", href: "/graph" },
  { label: "Writer", href: "#" },
];

export function Nav() {
  return (
    <nav style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
      {navItems.map((item) => (
        <Link
          key={item.label}
          href={item.href}
          style={{
            padding: "6px 10px",
            borderRadius: 8,
            background: "#e8eefb",
            fontSize: 14,
            fontWeight: 600,
          }}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
