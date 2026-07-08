import { Category } from "@/types/category";

import CollectionCard from "./CollectionCard";

interface CollectionGridProps {
  categories: Category[];
}

export default function CollectionGrid({
  categories,
}: CollectionGridProps) {
  return (
    <div
      className="
        grid
        grid-cols-1
        gap-5
        sm:grid-cols-2
        sm:gap-6
        lg:grid-cols-4
        lg:gap-8
      "
    >
      {categories.map((category) => (
        <CollectionCard
          key={category.public_id}
          category={category}
        />
      ))}
    </div>
  );
}
