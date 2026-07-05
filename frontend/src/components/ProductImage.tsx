"use client";

import Image from "next/image";
import Link from "next/link";
import WishlistButton from "./common/WishlistButton";

interface ProductImageProps {
  image: string | null | undefined; // Cloudinary URL from product.images[0].url
  name: string;
  productPublicId?: string; // For wishlist toggle
  wishlistActive?: boolean;
  href?: string;
}

export default function ProductImage({
  image,
  name,
  productPublicId,
  wishlistActive = false,
  href,
}: ProductImageProps) {
  const imageSrc = normalizeImage(image);
  const imageElement = (
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
  );

  return (
    <div className="group relative overflow-hidden rounded-[32px]">
      {href ? <Link href={href}>{imageElement}</Link> : imageElement}

      {productPublicId && (
        <WishlistButton
          productPublicId={productPublicId}
          initialActive={wishlistActive}
        />
      )}
    </div>
  );
}

function normalizeImage(image: string | null | undefined) {
  if (!image) return "/placeholder.jpg";
  if (image.startsWith("//")) return `https:${image}`;
  return image.replace("http://res.cloudinary.com", "https://res.cloudinary.com");
}
