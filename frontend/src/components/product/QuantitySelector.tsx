"use client";

import { Minus, Plus } from "lucide-react";

interface QuantitySelectorProps {
  quantity: number;
  setQuantity: (quantity: number) => void;
}

export default function QuantitySelector({
  quantity,
  setQuantity,
}: QuantitySelectorProps) {
  return (
    <div className="flex w-fit items-center rounded-full border">

      <button
        onClick={() =>
          quantity > 1 &&
          setQuantity(quantity - 1)
        }
        className="px-4 py-2.5 sm:px-5 sm:py-3"
      >
        <Minus size={18} />
      </button>

      <span className="min-w-10 text-center sm:min-w-12">
        {quantity}
      </span>

      <button
        onClick={() =>
          setQuantity(quantity + 1)
        }
        className="px-4 py-2.5 sm:px-5 sm:py-3"
      >
        <Plus size={18} />
      </button>

    </div>
  );
}
