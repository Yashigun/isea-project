"use client";

import { ShoppingBag } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

interface AddToCartButtonProps {
  onClick?: () => void;
}

export default function AddToCartButton({ onClick }: AddToCartButtonProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  const handleClick = () => {
    if (!isAuthenticated) {
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
      return;
    }
    if (onClick) onClick();
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      className="flex w-full items-center justify-center gap-2 rounded-full border border-black py-3 transition-all duration-300 hover:bg-black hover:text-white"
    >
      <ShoppingBag size={18} />
      Add to Cart
    </button>
  );
}