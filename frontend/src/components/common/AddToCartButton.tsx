"use client";

import { ShoppingBag } from "lucide-react";

interface AddToCartButtonProps {
  onClick?: () => void;
}

export default function AddToCartButton({
  onClick,
}: AddToCartButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="
        flex
        w-full
        items-center
        justify-center
        gap-2
        rounded-full
        border
        border-black
        py-3
        transition-all
        duration-300
        hover:bg-black
        hover:text-white
      "
    >
      <ShoppingBag size={18} />

      Add to Cart
    </button>
  );
}