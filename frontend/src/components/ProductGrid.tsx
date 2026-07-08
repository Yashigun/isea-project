
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
        grid-cols-1
        gap-5
        sm:grid-cols-2
        sm:gap-6
        lg:grid-cols-3
        lg:gap-8
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