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
        gap-8
        sm:grid-cols-2
        lg:grid-cols-4
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