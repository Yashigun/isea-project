import Image from "next/image";
import Link from "next/link";

import { Category } from "@/types/category";

interface CollectionCardProps {
  category: Category;
}

export default function CollectionCard({
  category,
}: CollectionCardProps) {
  const imageSrc =
    normalizeImage(category.image);

  return (
    <Link
      href={`/collections/${category.slug}`}
      className="
        group
        block
        min-w-0
        overflow-hidden
        rounded-[18px]
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-[0_20px_40px_rgba(220,38,38,0.14)]
        sm:rounded-[22px]
        lg:rounded-[26px]
      "
    >
      <div
        className="
          overflow-hidden
          rounded-[18px]
          sm:rounded-[22px]
          lg:rounded-[26px]
        "
      >
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

      <div className="mt-2 flex min-w-0 items-center justify-between gap-1 sm:mt-3 lg:mt-4">
        <h3
          className="
            mb-2
            ml-1
            min-w-0
            truncate
            text-sm
            font-medium
            sm:mb-3
            sm:ml-2
            sm:text-lg
            lg:ml-3
            lg:text-xl
          "
        >
          {category.name}
        </h3>

        <span
          className="
            mb-2
            mr-1
            shrink-0
            text-[10px]
            transition-transform
            duration-300
            group-hover:translate-x-1
            sm:mb-3
            sm:mr-2
            sm:text-xs
            lg:mr-3
            lg:text-sm
          "
        >
          Explore →
        </span>
      </div>
    </Link>
  );
}

function normalizeImage(
  image: string | null | undefined,
) {
  if (!image) {
    return "/placeholder.jpg";
  }

  if (image.startsWith("//")) {
    return `https:${image}`;
  }

  return image.replace(
    "http://res.cloudinary.com",
    "https://res.cloudinary.com",
  );
}