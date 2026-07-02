import { Category } from "./category";

export interface Product {
  id: string;

  name: string;

  slug: string;

  shortDescription: string;

  description: string;

  price: number;

  discountPrice?: number;

  images: string[];

  category: Category;

  featured: boolean;

  stock: number;

  rating: number;
}