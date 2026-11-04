
"use client";

import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function DashboardContent() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading your profile...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  const initials = user.name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const handleLogout = async () => {
  try {
    await logout();
    router.replace("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="mx-auto max-w-5xl">

        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              TaskFlow Dashboard
            </h1>
            <p className="mt-2 text-gray-600">
              Welcome to your workspace!
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="rounded-lg bg-red-600 px-5 py-2 text-white hover:bg-red-700"
          >
            Logout
          </button>
        </div>

        {/* User Profile */}
        <section className="rounded-xl bg-white p-6 shadow-sm">
          <h2 className="mb-6 text-xl font-semibold text-gray-900">
            Your Profile
          </h2>

          <div className="flex items-center gap-5">
          {user.avatar_url ? (
  <Image
    src={user.avatar_url}
    alt={user.name}
    width={64}
    height={64}
    unoptimized
    className="h-16 w-16 rounded-full object-cover"
  />
) : (
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-xl font-bold text-white">
                {initials}
              </div>
            )}

            <div>
              <h3 className="text-xl font-semibold text-gray-900">
                {user.name}
              </h3>
              <p className="text-gray-600">
                {user.email}
              </p>
            </div>
          </div>

          <div className="mt-6 border-t pt-5">
            <p className="mb-2 text-sm text-gray-500">
              User ID
            </p>
            <p className="break-all text-sm font-medium text-gray-800">
              {user.id}
            </p>
          </div>
        </section>

        {/* Task Statistics */}
        <section className="mt-6 grid gap-5 md:grid-cols-3">
          <div className="rounded-xl bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Total Tasks</p>
            <h3 className="mt-2 text-3xl font-bold">0</h3>
          </div>

          <div className="rounded-xl bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">In Progress</p>
            <h3 className="mt-2 text-3xl font-bold">0</h3>
          </div>

          <div className="rounded-xl bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Completed</p>
            <h3 className="mt-2 text-3xl font-bold">0</h3>
          </div>
        </section>

      </div>
    </main>
  );
}
