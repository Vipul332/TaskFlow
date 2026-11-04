
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigationItems = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: "▦",
  },
  {
    name: "My Tasks",
    href: "/tasks",
    icon: "☑",
  },
  {
    name: "Team",
    href: "/team",
    icon: "♙",
  },
  {
    name: "Notifications",
    href: "/notifications",
    icon: "♧",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex min-h-screen w-64 flex-col bg-slate-900 text-white">

      {/* Logo */}
      <div className="border-b border-slate-700 px-6 py-6">
        <h1 className="text-2xl font-bold tracking-wide">
          <span className="text-blue-400">Task</span>Flow
        </h1>

        <p className="mt-1 text-xs text-slate-400">
          Collaborative Workspace
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <p className="mb-4 px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Workspace
        </p>

        <div className="space-y-2">
          {navigationItems.map((item) => {
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-700 p-5">
        <p className="text-xs text-slate-400">
          TaskFlow Workspace
        </p>
        <p className="mt-1 text-xs text-slate-500">
          Manage work together.
        </p>
      </div>

    </aside>
  );
}
