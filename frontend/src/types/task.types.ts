export type TaskStatus = "TODO" | "IN_PROGRESS" | "COMPLETED";

export type TaskPriority = "LOW" | "MEDIUM" | "HIGH" | "URGENT";

export interface TaskUser {
  id: string;
  name: string;
  email: string;
  avatar_url: string | null;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  creator_id: string;
  assignee_id: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  due_date: string | null;
  created_at: string;
  updated_at: string;
  creator: TaskUser | null;
  assignee: TaskUser | null;
}

export interface TasksResponse {
  success: boolean;
  message: string;
  tasks: Task[];
}