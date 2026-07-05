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
        gap-8
        sm:grid-cols-2
        lg:grid-cols-3
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