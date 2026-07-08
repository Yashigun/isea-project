import ProductGrid from "../ProductGrid";

import { Product } from "@/services/product";

interface RelatedProductsProps {
  products: Product[];
}

export default function RelatedProducts({
  products,
}: RelatedProductsProps) {
  return (
    <div className="space-y-6 sm:space-y-8">
      <h2 className="text-2xl font-medium sm:text-3xl">
        You may also like
      </h2>

      <ProductGrid products={products} />
    </div>
  );
}
