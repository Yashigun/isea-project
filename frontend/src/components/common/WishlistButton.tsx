"use client";

import { Heart } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

interface WishlistButtonProps {
  active?: boolean;
  onClick?: () => void;
}

export default function WishlistButton({ active = false, onClick }: WishlistButtonProps) {
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
      aria-label="Wishlist"
      className="absolute right-4 top-4 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-white shadow-md transition-all duration-300 hover:scale-110"
    >
      <Heart size={20} className={active ? "fill-red-500 text-red-500" : "text-black"} />
    </button>
  );
}