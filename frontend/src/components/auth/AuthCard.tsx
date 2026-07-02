"use client";

import { useState } from "react";

import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function AuthCard() {
  const [login, setLogin] =
    useState(true);

  return (
    <div
      className="
        w-full
        max-w-md
        rounded-3xl
        border
        bg-white
        p-8
        shadow-lg
      "
    >
      <div className="mb-8 text-center">

        <h1 className="text-3xl font-semibold">
          {login
            ? "Welcome Back"
            : "Create Account"}
        </h1>

        <p className="mt-2 text-gray-500">
          Continue to Vimsy
        </p>

      </div>

      {login ? (
        <LoginForm
          switchToRegister={() =>
            setLogin(false)
          }
        />
      ) : (
        <RegisterForm
          switchToLogin={() =>
            setLogin(true)
          }
        />
      )}

    </div>
  );
}