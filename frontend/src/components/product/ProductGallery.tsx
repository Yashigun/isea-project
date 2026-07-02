"use client";

import { useState } from "react";
import Image from "next/image";

interface ProductGalleryProps {
  images: string[];
  name: string;
}

export default function ProductGallery({
  images,
  name,
}: ProductGalleryProps) {
  const [selected, setSelected] = useState(images[0]);

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

      {images.length > 1 && (

        <div className="flex gap-4">

          {images.map((image) => (

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