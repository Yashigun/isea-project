"use client";

import { useEffect, useMemo, useState } from "react";
import Image from "next/image";

interface ProductGalleryProps {
  images: Array<string | { url: string }>;
  name: string;
  primaryImage?: string | null;
}

export default function ProductGallery({
  images,
  name,
  primaryImage,
}: ProductGalleryProps) {
  const imageUrls = useMemo(
    () =>
      [
        primaryImage,
        ...images.map((image) => (typeof image === "string" ? image : image?.url)),
      ]
        .filter(Boolean)
        .map((image) => normalizeImage(String(image)))
        .filter((image, index, list) => list.indexOf(image) === index),
    [images, primaryImage]
  );

  const firstImage = imageUrls[0] || "/placeholder.jpg";

  const [selected, setSelected] = useState(firstImage);

  useEffect(() => {
    queueMicrotask(() => setSelected(firstImage));
  }, [firstImage]);

  return (
    <div className="space-y-5">

      <div className="overflow-hidden rounded-[32px]">

        <Image
          src={selected}
          alt={name}
          width={900}
          height={900}
          className="aspect-square w-full object-cover"
          priority
        />

      </div>

      {imageUrls.length > 1 && (

        <div className="flex gap-4">

          {imageUrls.map((image) => (

            <button
              key={image}
              onClick={() => setSelected(image)}
              className={`
                overflow-hidden
                rounded-xl
                border-2
                transition

                ${
                  selected === image
                    ? "border-black"
                    : "border-transparent"
                }
              `}
            >

              <Image
                src={image}
                alt={name}
                width={110}
                height={110}
                className="aspect-square object-cover"
              />

            </button>

          ))}

        </div>

      )}

    </div>
  );
}

function normalizeImage(image: string | null | undefined) {
  if (!image) return "/placeholder.jpg";
  if (image.startsWith("//")) return `https:${image}`;
  return image.replace("http://res.cloudinary.com", "https://res.cloudinary.com");
}
