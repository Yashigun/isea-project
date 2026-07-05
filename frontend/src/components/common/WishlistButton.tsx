"use client";

import { Heart } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { wishlistService } from "@/services/wishlist";
import { useState, useEffect } from "react";

interface WishlistButtonProps {
  productPublicId?: string;
  initialActive?: boolean;
  onToggle?: (active: boolean) => void;
}

export default function WishlistButton({
  productPublicId,
  initialActive = false,
  onToggle,
}: WishlistButtonProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [active, setActive] = useState(initialActive);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setActive(initialActive);
  }, [initialActive]);

  const handleClick = async () => {
    if (!isAuthenticated) {
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
      return;
    }

    if (!productPublicId) {
      console.warn("WishlistButton: productPublicId is required");
      return;
    }

    setLoading(true);
    try {
      let newState = active;
      if (active) {
        await wishlistService.remove(productPublicId);
        newState = false;
      } else {
        await wishlistService.add(productPublicId);
        newState = true;
      }
      setActive(newState);
      if (onToggle) onToggle(newState);
    } catch (error) {
      console.error("Failed to toggle wishlist:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={loading}
      aria-label="Wishlist"
      className="absolute right-4 top-4 z-10 flex h-11 w-11 items-center justify-center rounded-full bg-white shadow-md transition-all duration-300 hover:scale-110 disabled:opacity-50"
    >
      <Heart
        size={20}
        className={active ? "fill-red-500 text-red-500" : "text-black"}
      />
    </button>
  );
}