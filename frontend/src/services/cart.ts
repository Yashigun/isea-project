import api from "@/lib/axios";

export interface CartItem {
  public_id: string;
  product: {
    public_id: string;
    name: string;
    slug: string;
    price: number;
    discount_price: number | null;
    primary_image: string | null;
  };
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface Cart {
  public_id: string;
  items: CartItem[];
  total_items: number;
  subtotal: number;
  discount: number;
  tax: number;
  total_amount: number;
}

export const cartService = {
  async get(): Promise<Cart> {
    const response = await api.get("/cart/");
    return response.data;
  },

  async addItem(productPublicId: string, quantity: number = 1): Promise<Cart> {
    const response = await api.post("/cart/items", {
      product_public_id: productPublicId,
      quantity,
    });
    return response.data;
  },

  async updateItem(productPublicId: string, quantity: number): Promise<Cart> {
    const response = await api.put(`/cart/items/${productPublicId}`, { quantity });
    return response.data;
  },

  async removeItem(productPublicId: string): Promise<Cart> {
    const response = await api.delete(`/cart/items/${productPublicId}`);
    return response.data;
  },

  async clear(): Promise<void> {
    await api.delete("/cart/");
  },
};
