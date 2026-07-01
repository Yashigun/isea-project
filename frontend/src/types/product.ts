import { Category } from "./category";

export interface Product {
  id: string;
  name: string;
  slug: string;
  description: string;
  price: number;
  image: string;
  rating: number;
  featured: boolean;
  category: Category;
}