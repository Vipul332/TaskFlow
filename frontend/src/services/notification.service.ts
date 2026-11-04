
import { apiRequest } from "@/services/api";

export interface NotificationTask {
  title: string;
  description: string | null;
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  status: "TODO" | "IN_PROGRESS" | "COMPLETED";
}

export interface Notification {
  id: string;
  task_id: string;
  recipient_id: string;
  type: "TASK_ASSIGNED" | "TASK_COMPLETED";
  status: "PENDING" | "SENT" | "FAILED";
  sent_at: string | null;
  error_message: string | null;
  created_at: string;
  tasks: NotificationTask | null;
}

export interface NotificationsResponse {
  success: boolean;
  message: string;
  notifications: Notification[];
}

export async function getNotifications(): Promise<NotificationsResponse> {
  return apiRequest<NotificationsResponse>("/notifications/");
}
