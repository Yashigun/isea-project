import { categories } from "./categories";

import { Product } from "@/types/product";

export const products: Product[] = [
  {
    id: "1",
    name: "Buddy Bunny",
    slug: "buddy-bunny",
    shortDescription: "Cute crochet bunny",
    description: "A handmade crochet bunny.",
    price: 1499,
    discountPrice: 1299,
    images: [
      "/images/products/bunny-1.jpg",
      "/images/products/bunny-2.jpg",
    ],
    featured: true,
    stock: 10,
    rating: 5,
    category: categories[0],
  },

  {
    id: "2",
    name: "Sunflower Bunny",
    slug: "sunflower-bunny",
    shortDescription: "Crochet sunflower bunny",
    description: "Soft and handmade.",
    price: 1699,
    images: [
      "/images/products/bunny-3.jpg",
    ],
    featured: true,
    stock: 6,
    rating: 4.9,
    category: categories[0],
  },
];