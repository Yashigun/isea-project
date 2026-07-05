import api from "@/lib/axios";
import { Product } from "./product";

export const wishlistService = {
  async get(): Promise<Product[]> {
    const response = await api.get("/wishlist");
    return response.data;
  },

  async add(productPublicId: string): Promise<void> {
    await api.post(`/wishlist/${productPublicId}`);
  },

  async remove(productPublicId: string): Promise<void> {
    await api.delete(`/wishlist/${productPublicId}`);
  },
};
