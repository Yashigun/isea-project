import api from "@/lib/axios";


export const wishlistService = {
  async get(): Promise<any[]> {
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

