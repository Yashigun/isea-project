import { categories } from "./categories";

import { Product } from "@/types/product";

export const products: Product[] = [
  {
    id: "1",
    name: "Golden Leaf Necklace",
    slug: "golden-leaf-necklace",
    description: "Elegant everyday necklace.",
    price: 1299,
    image: "/images/products/product-1.jpg",
    rating: 4.9,
    featured: true,
    category: categories[1],
  },
  {
    id: "2",
    name: "Rose Charm Bracelet",
    slug: "rose-charm-bracelet",
    description: "Minimal handmade bracelet.",
    price: 899,
    image: "/images/products/product-2.jpg",
    rating: 4.8,
    featured: true,
    category: categories[0],
  },
  {
    id: "3",
    name: "Pearl Bloom Ring",
    slug: "pearl-bloom-ring",
    description: "Classic pearl ring.",
    price: 1099,
    image: "/images/products/product-3.jpg",
    rating: 5,
    featured: true,
    category: categories[3],
  },
];