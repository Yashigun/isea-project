import ProductGrid from "../ProductGrid";

import { Product } from "@/types/product";

interface RelatedProductsProps {
  products: Product[];
}

export default function RelatedProducts({
  products,
}: RelatedProductsProps) {
  return (
    <div className="space-y-8">

      <h2 className="text-3xl font-medium">
        You may also like
      </h2>

      <ProductGrid
        products={products}
      />

    </div>
  );
}