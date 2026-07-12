
import api from "@/lib/axios";

export interface OrderProduct {
  public_id: string;
  name: string;
  slug: string;
  price: number;
  discount_price?: number | null;
  primary_image?: string | null;
}

export interface OrderItem {
  public_id: string;
  product_name: string;
  unit_price: number;
  quantity: number;
  subtotal: number;
  product?: OrderProduct | null;
}

export interface Order {
  public_id: string;
  status:
    | "pending"
    | "confirmed"
    | "processing"
    | "shipped"
    | "delivered"
    | "cancelled"
    | "refunded";
  total_amount: number;
  subtotal: number;
  discount: number;
  shipping_cost: number;
  tax: number;
  created_at: string;
  customer: {
    public_id: string;
    first_name: string;
    last_name: string | null;
    email: string;
  };
  items: OrderItem[];
}

export const orderService = {
  // Customer
  async list(): Promise<Order[]> {
    const response = await api.get("/orders/");
    return response.data;
  },

  async get(publicId: string): Promise<Order> {
    const response = await api.get(`/orders/${publicId}`);
    return response.data;
  },

  async create(data: {
    shipping_address_public_id: string;
    phone_public_id: string;
    payment_method:
      | "card"
      | "upi"
      | "net_banking"
      | "cod";
    order_notes?: string;
  }): Promise<Order> {
    const response = await api.post("/orders/", data);
    return response.data;
  },

  async cancel(publicId: string): Promise<Order> {
    const response = await api.post(`/orders/${publicId}/cancel`);
    return response.data;
  },

  // Admin
  async listAll(status?: string): Promise<Order[]> {
    const response = await api.get("/admin/orders/", {
      params: { status },
    });
    return response.data;
  },

  async updateStatus(
    publicId: string,
    status: string
  ): Promise<Order> {
    const response = await api.patch(
      `/admin/orders/${publicId}/status`,
      null,
      {
        params: { status },
      }
    );

    return response.data;
  },
};