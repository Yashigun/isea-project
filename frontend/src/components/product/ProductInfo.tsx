"use client";

import { useState } from "react";
import ProductPrice from "../common/ProductPrice";
import WishlistButton from "../common/WishlistButton";
import AddToCartButton from "../common/AddToCartButton";
import QuantitySelector from "./QuantitySelector";

interface ProductInfoProps {
  publicId: string;
  name: string;
  price: number;
  discountPrice: number | null;
  shortDescription: string | null;
  description: string | null;
}

export default function ProductInfo({
  publicId,
  name,
  price,
  discountPrice,
  shortDescription,
  description,
}: ProductInfoProps) {
  const [quantity, setQuantity] = useState(1);

  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h1 className="text-3xl font-medium sm:text-4xl lg:text-5xl">{name}</h1>
          <div className="mt-3 sm:mt-4">
            <ProductPrice price={price} discountPrice={discountPrice ?? undefined} />
          </div>
        </div>
        <WishlistButton productPublicId={publicId} />
      </div>
      <p className="leading-7 text-gray-600 sm:leading-8">{shortDescription}</p>
      <QuantitySelector quantity={quantity} setQuantity={setQuantity} />
      <AddToCartButton productPublicId={publicId} quantity={quantity} />
      {description && (
        <div className="border-t border-gray-200 pt-5 sm:pt-6">
          <h2 className="text-lg font-medium sm:text-xl">Description</h2>
          <p className="mt-3 whitespace-pre-line leading-7 text-gray-600 sm:leading-8">
            {description}
          </p>
        </div>
      )}
    </div>
  );
}