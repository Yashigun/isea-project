"use client";

import { useState } from "react";

import PasswordInput from "./PasswordInput";

interface LoginFormProps {
  switchToRegister: () => void;
}

export default function LoginForm({
  switchToRegister,
}: LoginFormProps) {
  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  function submit(
    event: React.FormEvent
  ) {
    event.preventDefault();

    // API later
  }

  return (
    <form
      onSubmit={submit}
      className="space-y-5"
    >
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) =>
          setEmail(event.target.value)
        }
        className="
          w-full
          rounded-xl
          border
          px-4
          py-3
        "
      />

      <PasswordInput
        id="login-password"
        name="password"
        value={password}
        placeholder="Password"
        onChange={(event) =>
          setPassword(
            event.target.value
          )
        }
      />

      <button
        className="
          w-full
          rounded-xl
          bg-black
          py-3
          text-white
        "
      >
        Login
      </button>

      <p
        className="
          text-center
          text-sm
        "
      >
        Don't have an account?

        <button
          type="button"
          onClick={
            switchToRegister
          }
          className="
            ml-2
            underline
          "
        >
          Create one
        </button>
      </p>

    </form>
  );
}