import Link from "next/link";

const navItems = [
  { label: "Dashboard", href: "/" },
  { label: "Library", href: "/library" },
  { label: "Reader", href: "#" },
  { label: "Graph", href: "#" },
  { label: "Writer", href: "#" },
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
        <Link
          key={item.label}
          href={item.href}
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
          {item.label}
        </Link>
          {item}
        </span>
      ))}
    </nav>
  );
}
