import { Category } from "./category";

export interface ProductImage {
  public_id: string;
  url: string; // Cloudinary URL
  stored_filename: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  alt_text: string | null;
  display_order: number;
  is_primary: boolean;
  created_at: string;
  updated_at: string;
}

export interface Product {
  public_id: string;
  name: string;
  slug: string;
  price: number;
  discount_price: number | null;
  short_description: string | null;
  description: string | null;
  is_active: boolean;
  category: Category;
  images: ProductImage[];
  primary_image: string | null; // computed from images
  created_at: string;
  updated_at: string;
}