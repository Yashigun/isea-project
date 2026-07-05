export interface OrderItem {
  public_id: string;
  product_name: string;
  unit_price: number;
  quantity: number;
  subtotal: number;
}

export interface Order {
  public_id: string;
  status: "pending" | "confirmed" | "processing" | "shipped" | "delivered" | "cancelled" | "refunded";
  total_amount: number;
  subtotal: number;
  discount: number;
  shipping_cost: number;
  tax: number;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}