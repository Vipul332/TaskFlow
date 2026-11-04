
import { apiRequest } from "./api";
import type {
  Task,
  TasksResponse,
} from "@/types/task.types";

export interface CreateTaskInput {
  title: string;
  description: string;
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  assignee_id: string | null;
}

export interface CreateTaskResponse {
  success: boolean;
  message: string;
  task: Task;
}

// Fetch all tasks belonging to the logged-in user
export async function getTasks(): Promise<TasksResponse> {
  return apiRequest<TasksResponse>("/tasks/", {
    method: "GET",
  });
}

// Create a new task
export async function createTask(
  taskData: CreateTaskInput
): Promise<CreateTaskResponse> {
  return apiRequest<CreateTaskResponse>("/tasks/", {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}
export async function updateTaskStatus(
  taskId: string,
  status: "TODO" | "IN_PROGRESS" | "COMPLETED"
): Promise<CreateTaskResponse> {
  return apiRequest<CreateTaskResponse>(`/tasks/${taskId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}
