import { Product } from "./product";

export interface CartItem {
  public_id: string;
  product: Product;
  quantity: number;
  unit_price: number;
  subtotal: number;
  created_at: string;
  updated_at: string;
}

export interface Cart {
  public_id: string;
  items: CartItem[];
  total_items: number;
  subtotal: number;
  discount: number;
  tax: number;
  total_amount: number;
  created_at: string;
  updated_at: string;
}