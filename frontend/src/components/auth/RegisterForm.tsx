"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import PasswordInput from "./PasswordInput";

interface RegisterFormProps {
  switchToLogin: () => void;
}

export default function RegisterForm({ switchToLogin }: RegisterFormProps) {
  const { register } = useAuth();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await register({ first_name: firstName, last_name: lastName, email, password });
      // After registration, switch to login or show success
      switchToLogin();
    }catch (err: any) {
    const detail = err.response?.data?.detail;
      if (typeof detail === "string") {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map((e: any) => e.msg).join(", "));
      } else {
        setError("Registration failed");
      }
    }finally {
      setLoading(false);
    }
  };


  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <input
        placeholder="First Name"
        value={firstName}
        onChange={(e) => setFirstName(e.target.value)}
        className="w-full rounded-xl border px-4 py-3"
      />
      <input
        placeholder="Last Name"
        value={lastName}
        onChange={(e) => setLastName(e.target.value)}
        className="w-full rounded-xl border px-4 py-3"
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full rounded-xl border px-4 py-3"
      />
      <PasswordInput
        id="register-password"
        name="password"
        value={password}
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <PasswordInput
        id="confirm-password"
        name="confirmPassword"
        value={confirmPassword}
        placeholder="Confirm Password"
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-xl bg-black py-3 text-white disabled:opacity-50"
      >
        {loading ? "Creating..." : "Create Account"}
      </button>
      <p className="text-center text-sm">
        Already have an account?
        <button type="button" onClick={switchToLogin} className="ml-2 underline">
          Login
        </button>
      </p>
    </form>
  );
}