
"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

import {
  getTeamMembers,
  type TeamMember,
} from "@/services/user.service";

export default function TeamContent() {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchMembers() {
      try {
        setLoading(true);
        setError("");

        const response = await getTeamMembers();
        setMembers(response.users || []);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load team members."
        );
      } finally {
        setLoading(false);
      }
    }

    fetchMembers();
  }, []);

  if (loading) {
    return (
      <main className="p-6">
        <p className="text-gray-500">
          Loading team members...
        </p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="p-6">
        <div className="rounded-lg border border-red-200 bg-red-50 p-5">
          <h2 className="font-semibold text-red-700">
            Something went wrong
          </h2>
          <p className="mt-2 text-sm text-red-600">
            {error}
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Team Members
        </h1>

        <p className="mt-2 text-sm text-gray-500">
          View all registered members of your TaskFlow workspace.
        </p>
      </div>

      <div className="mb-8 max-w-xs rounded-xl border bg-white p-6 shadow-sm">
        <p className="text-sm font-medium text-gray-500">
          Total Members
        </p>

        <h2 className="mt-2 text-3xl font-bold text-gray-900">
          {members.length}
        </h2>
      </div>

      {members.length === 0 ? (
        <div className="rounded-xl border bg-white p-10 text-center shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800">
            No team members yet
          </h2>

          <p className="mt-2 text-sm text-gray-500">
            Other users will appear here after they sign in to TaskFlow.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {members.map((member) => (
            <div
              key={member.id}
              className="rounded-xl border bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="flex items-center gap-4">
                {member.avatar_url ? (
                  <Image
                    src={member.avatar_url}
                    alt={`${member.name}'s profile`}
                    width={48}
                    height={48}
                    className="h-12 w-12 rounded-full object-cover"
                  />
                ) : (
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-blue-100 text-lg font-bold text-blue-700">
                    {member.name?.charAt(0).toUpperCase() || "U"}
                  </div>
                )}

                <div className="min-w-0">
                  <h3 className="truncate font-semibold text-gray-900">
                    {member.name}
                  </h3>

                  <p className="truncate text-sm text-gray-500">
                    {member.email}
                  </p>
                </div>
              </div>

              <div className="mt-5 border-t pt-4">
                <span className="inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700">
                  <span className="h-2 w-2 rounded-full bg-green-500" />
                  Registered Member
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
