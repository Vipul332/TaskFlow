
"use client";

import { useEffect, useRef, useState } from "react";
import { loginWithGoogle } from "@/services/auth.service";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (options: {
            client_id: string;
            callback: (response: { credential: string }) => void;
          }) => void;
          renderButton: (
            element: HTMLElement,
            options: {
              theme: string;
              size: string;
              width: number;
              text: string;
            }
          ) => void;
        };
      };
    };
  }
}

export default function GoogleLoginButton() {
  const buttonRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  const { refreshUser } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!clientId) return;

    let cancelled = false;

    const initializeGoogle = () => {
      if (cancelled || !window.google || !buttonRef.current) return;

      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: async (response) => {
          setLoading(true);
          setError("");

          try {
            await loginWithGoogle(response.credential);

            // Fetch the authenticated user from Flask.
            await refreshUser();

            // Navigate after successful authentication.
            router.push("/dashboard");
          } catch (err) {
            setError(
              err instanceof Error ? err.message : "Google login failed."
            );
          } finally {
            setLoading(false);
          }
        },
      });

      window.google.accounts.id.renderButton(buttonRef.current, {
        theme: "outline",
        size: "large",
        width: 280,
        text: "continue_with",
      });
    };

    const existingScript = document.querySelector(
      'script[src="https://accounts.google.com/gsi/client"]'
    );

    if (window.google) {
      initializeGoogle();
    } else if (existingScript) {
      existingScript.addEventListener("load", initializeGoogle);
    } else {
      const script = document.createElement("script");
      script.src = "https://accounts.google.com/gsi/client";
      script.async = true;
      script.defer = true;
      script.onload = initializeGoogle;
      script.onerror = () => {
        if (!cancelled) {
          setError("Unable to load Google sign-in.");
        }
      };

      document.head.appendChild(script);
    }

    return () => {
      cancelled = true;
    };
  }, [clientId, refreshUser, router]);

  return (
    <div className="flex flex-col items-center gap-3">
      {!clientId ? (
        <p className="text-sm text-red-600">
          Google Client ID is missing. Check your .env.local file.
        </p>
      ) : (
        <div ref={buttonRef} />
      )}

      {loading && <p>Signing you in...</p>}

      {error && (
        <p className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
