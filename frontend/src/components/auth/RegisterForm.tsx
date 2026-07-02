"use client";

import { useState } from "react";

import PasswordInput from "./PasswordInput";

interface RegisterFormProps {
  switchToLogin: () => void;
}

export default function RegisterForm({
  switchToLogin,
}: RegisterFormProps) {
  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [confirmPassword,
    setConfirmPassword] =
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
        placeholder="Full Name"
        value={name}
        onChange={(event) =>
          setName(
            event.target.value
          )
        }
        className="
          w-full
          rounded-xl
          border
          px-4
          py-3
        "
      />

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) =>
          setEmail(
            event.target.value
          )
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
        id="register-password"
        name="password"
        value={password}
        placeholder="Password"
        onChange={(event) =>
          setPassword(
            event.target.value
          )
        }
      />

      <PasswordInput
        id="confirm-password"
        name="confirmPassword"
        value={confirmPassword}
        placeholder="Confirm Password"
        onChange={(event) =>
          setConfirmPassword(
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
        Create Account
      </button>

      <p
        className="
          text-center
          text-sm
        "
      >
        Already have an account?

        <button
          type="button"
          onClick={switchToLogin}
          className="
            ml-2
            underline
          "
        >
          Login
        </button>
      </p>

    </form>
  );
}