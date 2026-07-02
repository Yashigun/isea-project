"use client";

import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";

interface PasswordInputProps {
  id: string;
  name: string;
  value: string;
  placeholder?: string;
  onChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void;
}

export default function PasswordInput({
  id,
  name,
  value,
  placeholder,
  onChange,
}: PasswordInputProps) {
  const [visible, setVisible] =
    useState(false);

  return (
    <div className="relative">

      <input
        id={id}
        name={name}
        type={
          visible ? "text" : "password"
        }
        value={value}
        placeholder={placeholder}
        onChange={onChange}
        className="
          w-full
          rounded-xl
          border
          px-4
          py-3
          pr-12
          outline-none
          focus:border-black
        "
      />

      <button
        type="button"
        onClick={() =>
          setVisible(!visible)
        }
        className="
          absolute
          right-4
          top-1/2
          -translate-y-1/2
        "
      >
        {visible ? (
          <EyeOff size={20} />
        ) : (
          <Eye size={20} />
        )}
      </button>

    </div>
  );
}