
import GoogleLoginButton from "@/components/auth/GoogleLoginButton";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-lg">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome to TaskFlow
        </h1>

        <p className="mt-3 text-gray-500">
          Manage tasks, collaborate with your team, and stay productive.
        </p>

        <div className="mt-8 flex justify-center">
          <GoogleLoginButton />
        </div>
      </div>
    </main>
  );
}
