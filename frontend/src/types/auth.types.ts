
export interface User {
  id: string;
  name: string;
  email: string;
  avatar_url: string | null;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  user: User;
}

export interface MeResponse {
  success: boolean;
  user: User;
}
