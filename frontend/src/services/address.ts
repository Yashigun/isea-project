import api from "@/lib/axios";
import type { Address } from "@/types/address";

export type { Address };

export const addressService = {
  async getAll(): Promise<Address[]> {
    const response = await api.get("/addresses/");
    return response.data;
  },

  async create(data: Omit<Address, "public_id" | "created_at" | "updated_at">): Promise<Address> {
    const response = await api.post("/addresses/", data);
    return response.data;
  },

  async update(publicId: string, data: Partial<Omit<Address, "public_id" | "created_at" | "updated_at">>): Promise<Address> {
    const response = await api.put(`/addresses/${publicId}`, data);
    return response.data;
  },

  async delete(publicId: string): Promise<void> {
    await api.delete(`/addresses/${publicId}`);
  },

  async setDefault(publicId: string): Promise<void> {
    await api.post(`/addresses/${publicId}/set-default`);
  },
};
