"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import PasswordInput from "./PasswordInput";

interface LoginFormProps {
  switchToRegister: () => void;
}

export default function LoginForm({ switchToRegister }: LoginFormProps) {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full rounded-xl border px-4 py-3"
      />
      <PasswordInput
        id="login-password"
        name="password"
        value={password}
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-xl bg-black py-3 text-white disabled:opacity-50"
      >
        {loading ? "Logging in..." : "Login"}
      </button>
      <p className="text-center text-sm">
        Don't have an account?
        <button type="button" onClick={switchToRegister} className="ml-2 underline">
          Create one
        </button>
      </p>
    </form>
  );
}