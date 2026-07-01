import { useEffect, useState } from "react";

import { getFeaturedProducts } from "@/services/product";

import { Product } from "@/types/product";

export function useProducts() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    getFeaturedProducts().then(setProducts);
  }, []);

  return products;
}