"use client";

import Image from "next/image";

import WishlistButton from "./common/WishlistButton";

interface ProductImageProps {
  image: string;
  name: string;
}

export default function ProductImage({
  image,
  name,
}: ProductImageProps) {
  return (
    <div className="group relative overflow-hidden rounded-[32px]">

      <Image
        src={image}
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
      />

      <WishlistButton />

    </div>
  );
}