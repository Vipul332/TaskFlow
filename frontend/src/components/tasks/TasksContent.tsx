
"use client";

import { useCallback, useEffect, useState } from "react";

import {
  createTask,
  getTasks,
  updateTaskStatus,
} from "@/services/task.service";

import type {
  CreateTaskInput,
} from "@/services/task.service";

import {
  getTeamMembers,
  type TeamMember,
} from "@/services/user.service";

import type {
  Task,
  TaskStatus,
} from "@/types/task.types";

const priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"] as const;

const statuses: TaskStatus[] = [
  "TODO",
  "IN_PROGRESS",
  "COMPLETED",
];

export default function TasksContent() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [members, setMembers] = useState<TeamMember[]>([]);

  const [loading, setLoading] = useState(true);
  const [membersLoading, setMembersLoading] = useState(true);
  const [error, setError] = useState("");

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [updatingTaskId, setUpdatingTaskId] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState("");

  const [formData, setFormData] = useState<CreateTaskInput>({
    title: "",
    description: "",
    priority: "MEDIUM",
    assignee_id: null,
  });

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    try {
      setError("");

      const response = await getTasks();
      setTasks(response.tasks);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load tasks."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  // Load tasks and team members
  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        const [taskResponse, memberResponse] = await Promise.all([
          getTasks(),
          getTeamMembers(),
        ]);

        if (!cancelled) {
          setTasks(taskResponse.tasks);
          setMembers(memberResponse.users);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load tasks or team members."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
          setMembersLoading(false);
        }
      }
    }

    void loadData();

    return () => {
      cancelled = true;
    };
  }, []);

  // Handle input changes
  function handleChange(
    event: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: name === "assignee_id" ? value || null : value,
    }));
  }

  // Create task
  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    if (!formData.title.trim()) {
      setError("Task title is required.");
      return;
    }

    try {
      setSubmitting(true);
      setError("");
      setSuccessMessage("");

      await createTask({
        ...formData,
        title: formData.title.trim(),
        description: formData.description.trim(),
      });

      setSuccessMessage("Task created successfully!");

      setFormData({
        title: "",
        description: "",
        priority: "MEDIUM",
        assignee_id: null,
      });

      setIsModalOpen(false);

      await fetchTasks();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to create task."
      );
    } finally {
      setSubmitting(false);
    }
  }

  // Update task status
  async function handleStatusChange(
    taskId: string,
    newStatus: TaskStatus
  ) {
    try {
      setUpdatingTaskId(taskId);
      setError("");
      setSuccessMessage("");

      await updateTaskStatus(taskId, newStatus);

      setSuccessMessage("Task status updated successfully!");

      // Fetch updated task data, including creator and assignee details.
      await fetchTasks();

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to update task status."
      );
    } finally {
      setUpdatingTaskId(null);
    }
  }

  const priorityStyles: Record<string, string> = {
    LOW: "bg-gray-100 text-gray-700",
    MEDIUM: "bg-blue-100 text-blue-700",
    HIGH: "bg-orange-100 text-orange-700",
    URGENT: "bg-red-100 text-red-700",
  };

  const statusStyles: Record<string, string> = {
    TODO: "bg-gray-100 text-gray-700",
    IN_PROGRESS: "bg-yellow-100 text-yellow-700",
    COMPLETED: "bg-green-100 text-green-700",
  };

  return (
    <div className="space-y-6">

      {/* Page Header */}
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            My Tasks
          </h1>

          <p className="mt-2 text-gray-600">
            Manage and track your tasks here.
          </p>
        </div>

        <button
          onClick={() => {
            setError("");
            setSuccessMessage("");
            setIsModalOpen(true);
          }}
          className="rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white hover:bg-blue-700"
        >
          + Create Task
        </button>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="rounded-lg bg-green-50 p-3 text-green-700">
          {successMessage}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="flex items-center justify-between rounded-lg bg-red-50 p-3 text-red-700">
          <p>{error}</p>

          <button
            onClick={() => setError("")}
            className="font-bold"
          >
            ×
          </button>
        </div>
      )}

      {/* Tasks List */}
      <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">

        {loading ? (
          <p className="p-8 text-center text-gray-500">
            Loading tasks...
          </p>
        ) : tasks.length === 0 ? (
          <div className="p-12 text-center">
            <h3 className="text-lg font-semibold text-gray-800">
              No tasks found
            </h3>

            <p className="mt-2 text-gray-500">
              Create your first task to get started.
            </p>
          </div>
        ) : (
          <table className="w-full min-w-200 text-left">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-5 py-4 text-sm font-semibold text-gray-600">
                  Task
                </th>

                <th className="px-5 py-4 text-sm font-semibold text-gray-600">
                  Assigned To
                </th>

                <th className="px-5 py-4 text-sm font-semibold text-gray-600">
                  Priority
                </th>

                <th className="px-5 py-4 text-sm font-semibold text-gray-600">
                  Status
                </th>

                <th className="px-5 py-4 text-sm font-semibold text-gray-600">
                  Created
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-100">
              {tasks.map((task) => (
                <tr key={task.id} className="hover:bg-gray-50">

                  {/* Task Details */}
                  <td className="px-5 py-4">
                    <p className="font-medium text-gray-900">
                      {task.title}
                    </p>

                    <p className="mt-1 max-w-xs truncate text-sm text-gray-500">
                      {task.description || "No description"}
                    </p>
                  </td>

                  {/* Assigned User */}
                  <td className="px-5 py-4">
                    {task.assignee ? (
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {task.assignee.name}
                        </p>

                        <p className="text-xs text-gray-500">
                          {task.assignee.email}
                        </p>
                      </div>
                    ) : (
                      <span className="text-sm text-gray-400">
                        Unassigned
                      </span>
                    )}
                  </td>

                  {/* Priority */}
                  <td className="px-5 py-4">
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        priorityStyles[task.priority] || ""
                      }`}
                    >
                      {task.priority}
                    </span>
                  </td>

                  {/* Editable Status */}
                  <td className="px-5 py-4">
                    <select
                      value={task.status}
                      onChange={(event) =>
                        handleStatusChange(
                          task.id,
                          event.target.value as TaskStatus
                        )
                      }
                      disabled={updatingTaskId === task.id}
                      className={`rounded-lg border-0 px-3 py-2 text-xs font-semibold outline-none focus:ring-2 focus:ring-blue-300 disabled:cursor-wait disabled:opacity-60 ${
                        statusStyles[task.status] || ""
                      }`}
                    >
                      {statuses.map((status) => (
                        <option key={status} value={status}>
                          {status.replace("_", " ")}
                        </option>
                      ))}
                    </select>

                    {updatingTaskId === task.id && (
                      <p className="mt-1 text-xs text-gray-500">
                        Updating...
                      </p>
                    )}
                  </td>

                  {/* Created Date */}
                  <td className="px-5 py-4 text-sm text-gray-500">
                    {new Date(task.created_at).toLocaleDateString()}
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Create Task Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">

          <div className="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">

            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                Create New Task
              </h2>

              <button
                onClick={() => setIsModalOpen(false)}
                className="text-2xl text-gray-500 hover:text-gray-800"
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">

              {/* Title */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Task Title *
                </label>

                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Enter task title"
                  maxLength={200}
                  required
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Description */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Description
                </label>

                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe your task..."
                  maxLength={5000}
                  rows={4}
                  className="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              {/* Assignee */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Assign To
                </label>

                <select
                  name="assignee_id"
                  value={formData.assignee_id || ""}
                  onChange={handleChange}
                  disabled={membersLoading}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-blue-500 disabled:bg-gray-100"
                >
                  <option value="">
                    Unassigned
                  </option>

                  {members.map((member) => (
                    <option key={member.id} value={member.id}>
                      {member.name} ({member.email})
                    </option>
                  ))}
                </select>

                <p className="mt-2 text-xs text-gray-500">
                  Select a registered team member to assign this task.
                </p>
              </div>

              {/* Priority */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Priority
                </label>

                <select
                  name="priority"
                  value={formData.priority}
                  onChange={handleChange}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-blue-500"
                >
                  {priorities.map((priority) => (
                    <option key={priority} value={priority}>
                      {priority}
                    </option>
                  ))}
                </select>
              </div>

              {/* Buttons */}
              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  disabled={submitting}
                  className="rounded-lg border border-gray-300 px-5 py-2.5 text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={submitting || membersLoading}
                  className="rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {submitting ? "Creating..." : "Create Task"}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
