"use client";

import { Heart } from "lucide-react";

interface WishlistButtonProps {
  active?: boolean;
  onClick?: () => void;
}

export default function WishlistButton({
  active = false,
  onClick,
}: WishlistButtonProps) {
  return (
    <button
      type="button"
      aria-label="Add to wishlist"
      onClick={onClick}
      className="
        absolute
        right-4
        top-4
        flex
        h-11
        w-11
        items-center
        justify-center
        rounded-full
        bg-white/95
        shadow-md
        transition-all
        duration-300
        hover:scale-110
      "
    >
      <Heart
        size={20}
        className={
          active
            ? "fill-red-500 text-red-500"
            : "text-gray-700"
        }
      />
    </button>
  );
}