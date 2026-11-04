
"use client";

import { useCallback, useEffect, useState } from "react";

import {
  getNotifications,
  type Notification,
} from "@/services/notification.service";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchNotifications = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getNotifications();

      setNotifications(response.notifications || []);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load notifications."
      );
    } finally {
      setLoading(false);
    }
  }, []);

 useEffect(() => {
  let isMounted = true;

  getNotifications()
    .then((response) => {
      if (isMounted) {
        setNotifications(response.notifications || []);
      }
    })
    .catch((err) => {
      if (isMounted) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load notifications."
        );
      }
    })
    .finally(() => {
      if (isMounted) {
        setLoading(false);
      }
    });

  return () => {
    isMounted = false;
  };
}, []);

  const formatDate = (date: string) => {
    return new Date(date).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  };

  const getNotificationTitle = (notification: Notification) => {
    if (notification.type === "TASK_ASSIGNED") {
      return "New task assigned to you";
    }

    return "Task completed";
  };

  const getNotificationDescription = (
    notification: Notification
  ) => {
    if (notification.type === "TASK_ASSIGNED") {
      return `You have been assigned a task: ${
        notification.tasks?.title || "Untitled task"
      }`;
    }

    return `The task you created has been completed: ${
      notification.tasks?.title || "Untitled task"
    }`;
  };

  const getDeliveryStyle = (status: Notification["status"]) => {
    switch (status) {
      case "SENT":
        return "bg-green-100 text-green-700";

      case "FAILED":
        return "bg-red-100 text-red-700";

      default:
        return "bg-yellow-100 text-yellow-700";
    }
  };

  return (
    <main className="space-y-6 p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Notifications
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Stay updated with your task assignments and completions.
          </p>
        </div>

        <button
          onClick={fetchNotifications}
          disabled={loading}
          className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500">
              Total notifications
            </p>

            <p className="mt-1 text-3xl font-bold text-gray-900">
              {notifications.length}
            </p>
          </div>

          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-2xl">
            🔔
          </div>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
          <button
            onClick={fetchNotifications}
            className="ml-2 font-semibold underline"
          >
            Try again
          </button>
        </div>
      )}

      {loading ? (
        <div className="rounded-xl border border-gray-200 bg-white p-10 text-center">
          <p className="text-gray-500">
            Loading notifications...
          </p>
        </div>
      ) : notifications.length === 0 ? (
        <div className="rounded-xl border border-gray-200 bg-white p-12 text-center">
          <div className="mb-3 text-4xl">🔔</div>

          <h2 className="text-lg font-semibold text-gray-900">
            No notifications yet
          </h2>

          <p className="mt-2 text-sm text-gray-500">
            Your task assignment and completion notifications
            will appear here.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:shadow-md"
            >
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xl">
                    {notification.type === "TASK_ASSIGNED"
                      ? "📋"
                      : "✅"}
                  </div>

                  <div>
                    <h2 className="font-semibold text-gray-900">
                      {getNotificationTitle(notification)}
                    </h2>

                    <p className="mt-1 text-sm text-gray-600">
                      {getNotificationDescription(notification)}
                    </p>

                    <p className="mt-2 text-xs text-gray-400">
                      {formatDate(notification.created_at)}
                    </p>
                  </div>
                </div>

                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${getDeliveryStyle(
                    notification.status
                  )}`}
                >
                  Email: {notification.status}
                </span>
              </div>

              {notification.tasks && (
                <div className="mt-4 border-t border-gray-100 pt-3">
                  <div className="flex flex-wrap gap-4 text-sm">
                    <p className="text-gray-600">
                      Priority:{" "}
                      <span className="font-medium text-gray-900">
                        {notification.tasks.priority}
                      </span>
                    </p>

                    <p className="text-gray-600">
                      Task status:{" "}
                      <span className="font-medium text-gray-900">
                        {notification.tasks.status}
                      </span>
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
