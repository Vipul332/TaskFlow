import { apiRequest } from "./api";

export interface TeamMember {
  id: string;
  name: string;
  email: string;
  avatar_url: string | null;
}

export interface TeamMembersResponse {
  success: boolean;
  message: string;
  users: TeamMember[];
}

export async function getTeamMembers(): Promise<TeamMembersResponse> {
  return apiRequest<TeamMembersResponse>("/users/", {
    method: "GET",
  });
}