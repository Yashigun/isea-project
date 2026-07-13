
import { Product } from "@/types/product";

import ProductCard from "./ProductCard";

interface ProductGridProps {
  products: Product[];
}

export default function ProductGrid({
  products,
}: ProductGridProps) {
  return (
    <div
      className="
        grid
        grid-cols-2
        gap-x-3
        gap-y-5
        sm:gap-x-5
        sm:gap-y-6
        md:grid-cols-3
        lg:grid-cols-4
        lg:gap-x-6
        lg:gap-y-8
      "
    >
      {products.map((product) => (
        <ProductCard
          key={product.public_id}
          product={product}
        />
      ))}
    </div>
  );
}