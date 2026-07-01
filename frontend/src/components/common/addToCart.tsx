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
        items-center
        gap-2
        rounded-full
        border
        border-black
        px-5
        py-2
        text-sm
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