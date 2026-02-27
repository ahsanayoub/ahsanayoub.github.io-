import Link from "next/link";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/requisitions", label: "Requisitions" },
  { href: "/candidates", label: "Candidates" },
];

export function AppShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-6xl gap-6 p-6">
      <aside className="w-56 rounded-lg border p-4">
        <h2 className="mb-4 text-lg font-semibold">ATS</h2>
        <nav className="space-y-2">
          {links.map((link) => (
            <Link key={link.href} className="block rounded px-3 py-2 hover:bg-slate-100" href={link.href}>
              {link.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 rounded-lg border p-6">
        <h1 className="mb-4 text-2xl font-semibold">{title}</h1>
        {children}
      </main>
    </div>
  );
}
