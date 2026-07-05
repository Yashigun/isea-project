"use client";

import { ShoppingBag } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { cartService } from "@/services/cart";
import { useState } from "react";
import type { MouseEvent } from "react";

interface AddToCartButtonProps {
  productPublicId?: string;
  quantity?: number;
}

export default function AddToCartButton({
  productPublicId,
  quantity = 1,
}: AddToCartButtonProps) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [added, setAdded] = useState(false);

  const handleClick = async (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    event.stopPropagation();

    if (!isAuthenticated) {
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
      return;
    }

    if (!productPublicId) {
      console.warn("AddToCartButton: productPublicId is required");
      return;
    }

    setLoading(true);
    try {
      const cart = await cartService.addItem(productPublicId, quantity);
      setAdded(true);
      window.dispatchEvent(
        new CustomEvent("cart:updated", { detail: { totalItems: cart.total_items } })
      );
    } catch (error) {
      console.error("Failed to add to cart:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={loading}
      className="flex w-full items-center justify-center gap-2 rounded-full border border-black py-3 transition-all duration-300 hover:bg-black hover:text-white disabled:opacity-50"
    >
      <ShoppingBag size={18} />
      {loading ? "Adding..." : added ? "Added to Cart" : "Add to Cart"}
    </button>
  );
}
