import Image from "next/image";
import Link from "next/link";

import { Category } from "@/types/category";

interface CollectionCardProps {
  category: Category;
}

export default function CollectionCard({
  category,
}: CollectionCardProps) {
  const imageSrc = normalizeImage(category.image);

  return (
    <Link
      href={`/collections/${category.slug}`}
      className="
        group
        block
        overflow-hidden
        rounded-[20px]
        sm:rounded-[24px]
        lg:rounded-[28px]
        transition-all
        duration-300
        hover:-translate-y-2
        hover:shadow-[0_20px_45px_rgba(220,38,38,0.16)]
      "
    >
      <div className="overflow-hidden rounded-[20px] sm:rounded-[24px] lg:rounded-[28px]">

        <Image
          src={imageSrc}
          alt={category.name}
          width={600}
          height={700}
          className="
            aspect-[4/5]
            w-full
            object-cover
            transition-transform
            duration-500
            group-hover:scale-105
          "
        />

      </div>

      <div className="mt-3 flex items-center justify-between sm:mt-4 lg:mt-5">

        <h3 className="ml-2 mb-2 text-lg font-medium sm:ml-3 sm:mb-3 sm:text-xl lg:ml-4 lg:text-2xl">
          {category.name}
        </h3>

        <span
          className="
            mr-2 mb-2
            text-xs
            sm:mr-3
            sm:mb-3
            sm:text-sm
            lg:mr-4
            transition-transform
            duration-300
            group-hover:translate-x-1
          "
        >
          Explore →
        </span>

      </div>
    </Link>
  );
}

function normalizeImage(image: string | null | undefined) {
  if (!image) return "/placeholder.jpg";
  if (image.startsWith("//")) return `https:${image}`;
  return image.replace("http://res.cloudinary.com", "https://res.cloudinary.com");
}
