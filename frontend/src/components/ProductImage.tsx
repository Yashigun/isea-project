"use client";

import Image from "next/image";
import WishlistButton from "./common/WishlistButton";

interface ProductImageProps {
  image: string | null | undefined; // Cloudinary URL from product.images[0].url
  name: string;
  productPublicId?: string; // For wishlist toggle
  wishlistActive?: boolean;
}

export default function ProductImage({
  image,
  name,
  productPublicId,
  wishlistActive = false,
}: ProductImageProps) {
  // Use placeholder if image is missing
  const imageSrc = image || "/placeholder.jpg";

  return (
    <div className="group relative overflow-hidden rounded-[32px]">
      <Image
        src={imageSrc}
        alt={name}
        width={600}
        height={600}
        className="
          aspect-square
          w-full
          object-cover
          transition-transform
          duration-500
          group-hover:scale-105
        "
        priority
      />

      {productPublicId && (
        <WishlistButton
          productPublicId={productPublicId}
          initialActive={wishlistActive}
        />
      )}
    </div>
  );
}