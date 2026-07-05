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
}

export default function ProductInfo({
  publicId,
  name,
  price,
  discountPrice,
  shortDescription,
}: ProductInfoProps) {
  const [quantity, setQuantity] = useState(1);

  return (
    <div className="space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-5xl font-medium">{name}</h1>
          <div className="mt-4">
            <ProductPrice price={price} discountPrice={discountPrice ?? undefined} />
          </div>
        </div>
        <WishlistButton productPublicId={publicId} />
      </div>
      <p className="leading-8 text-gray-600">{shortDescription}</p>
      <QuantitySelector quantity={quantity} setQuantity={setQuantity} />
      <AddToCartButton productPublicId={publicId} quantity={quantity} />
    </div>
  );
}