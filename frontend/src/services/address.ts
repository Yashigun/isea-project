import api from "@/lib/axios";
import { Address } from "@/types/address";

export const addressService = {
  async getAll(): Promise<Address[]> {
    const response = await api.get("/addresses");
    console.log("📥 Fetched addresses:", response.data);
    return response.data;
  },

  async create(data: Omit<Address, "public_id" | "created_at" | "updated_at">): Promise<Address> {
    const response = await api.post("/addresses", data);
    console.log("✅ Created address:", response.data);
    return response.data;
  },

  async update(publicId: string, data: Partial<Omit<Address, "public_id" | "created_at" | "updated_at">>): Promise<Address> {
    const response = await api.put(`/addresses/${publicId}`, data);
    console.log("✅ Updated address:", response.data);
    return response.data;
  },

  async delete(publicId: string): Promise<void> {
    await api.delete(`/addresses/${publicId}`);
    console.log("🗑️ Deleted address:", publicId);
  },

  async setDefault(publicId: string): Promise<void> {
    await api.post(`/addresses/${publicId}/set-default`);
  },
};