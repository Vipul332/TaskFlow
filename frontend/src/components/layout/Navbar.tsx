
"use client";

import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/tasks": "My Tasks",
  "/team": "Team Members",
  "/notifications": "Notifications",
};

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  const pageTitle = pageTitles[pathname] || "TaskFlow";

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((part) => part[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "U";

  const handleLogout = async () => {
    try {
      await logout();
      router.replace("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <header className="flex min-h-20 items-center justify-between border-b border-gray-200 bg-white px-4 py-4 sm:px-6 lg:px-8">

      {/* Page Title */}
      <div>
        <h1 className="text-xl font-bold text-gray-800 sm:text-2xl">
          {pageTitle}
        </h1>

        <p className="hidden text-sm text-gray-500 sm:block">
          Manage your work efficiently.
        </p>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3 sm:gap-5">

        {/* Search Bar - UI only */}
        <div className="hidden md:flex items-center rounded-lg border border-gray-200 bg-gray-50 px-3 py-2">
          <span className="mr-2 text-gray-400">⌕</span>

          <input
            type="text"
            placeholder="Search..."
            className="w-36 bg-transparent text-sm outline-none lg:w-48"
          />
        </div>

        {/* User Profile */}
        {user && (
          <div className="flex items-center gap-3">

            {user.avatar_url ? (
              <Image
                src={user.avatar_url}
                alt={user.name}
                width={40}
                height={40}
                unoptimized
                className="h-10 w-10 rounded-full object-cover"
              />
            ) : (
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-semibold text-white">
                {initials}
              </div>
            )}

            <div className="hidden sm:block">
              <p className="text-sm font-semibold text-gray-800">
                {user.name}
              </p>

              <p className="max-w-40 truncate text-xs text-gray-500">
                {user.email}
              </p>
            </div>

            <button
              onClick={handleLogout}
              className="rounded-lg border border-gray-200 px-3 py-2 text-sm font-medium text-gray-600 transition hover:bg-red-50 hover:text-red-600"
            >
              Logout
            </button>

          </div>
        )}
      </div>
    </header>
  );
}
