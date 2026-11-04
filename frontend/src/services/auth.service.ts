
import { apiRequest } from "./api";
import type { AuthResponse, MeResponse } from "@/types/auth.types";

export const loginWithGoogle = async (
  credential: string
): Promise<AuthResponse> => {
  return apiRequest<AuthResponse>("/auth/google", {
    method: "POST",
    body: JSON.stringify({ credential }),
  });
};

export const getCurrentUser = async (): Promise<MeResponse> => {
  return apiRequest<MeResponse>("/auth/me", {
    method: "GET",
  });
};

export const logoutUser = async (): Promise<{ success: boolean; message: string }> => {
  return apiRequest("/auth/logout", {
    method: "POST",
  });
};
