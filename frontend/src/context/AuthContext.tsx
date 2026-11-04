
"use client";

import {
  createContext,
  useCallback,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import type { User } from "@/types/auth.types";
import {
  getCurrentUser,
  logoutUser,
} from "@/services/auth.service";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  refreshUser: () => Promise<void>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Restore the user's session.
  const refreshUser = useCallback(async () => {
    try {
      const response = await getCurrentUser();
      setUser(response.user);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // Logout the user.
  const logout = useCallback(async () => {
    try {
      await logoutUser();
    } finally {
      setUser(null);
    }
  }, []);

  // Check the existing session when the application loads.
  useEffect(() => {
    let cancelled = false;

    const checkSession = async () => {
      try {
        const response = await getCurrentUser();

        if (!cancelled) {
          setUser(response.user);
        }
      } catch {
        if (!cancelled) {
          setUser(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    void checkSession();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: Boolean(user),
        refreshUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
