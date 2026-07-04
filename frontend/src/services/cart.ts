import api from "@/lib/axios";

export const cartService = {
  async get(): Promise<any> {
    const response = await api.get("/cart");
    return response.data;
  },
  async addItem(productPublicId: string, quantity: number): Promise<any> {
    const response = await api.post("/cart/items", { product_public_id: productPublicId, quantity });
    return response.data;
  },
  async updateItem(productPublicId: string, quantity: number): Promise<any> {
    const response = await api.put(`/cart/items/${productPublicId}`, { quantity });
    return response.data;
  },
  async removeItem(productPublicId: string): Promise<any> {
    const response = await api.delete(`/cart/items/${productPublicId}`);
    return response.data;
  },
  async clear(): Promise<void> {
    await api.delete("/cart");
  },
};