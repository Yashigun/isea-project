import api from "@/lib/axios";

export interface Phone {
  public_id: string;
  phone_number: string;
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

export const phoneService = {
  async getAll(): Promise<Phone[]> {
    const response = await api.get("/phones/");
    return response.data;
  },

  async create(data: Omit<Phone, "public_id" | "created_at" | "updated_at">): Promise<Phone> {
    const response = await api.post("/phones/", data);
    return response.data;
  },

  async update(publicId: string, data: Partial<Omit<Phone, "public_id" | "created_at" | "updated_at">>): Promise<Phone> {
    const response = await api.put(`/phones/${publicId}`, data);
    return response.data;
  },

  async delete(publicId: string): Promise<void> {
    await api.delete(`/phones/${publicId}`);
  },

  async setDefault(publicId: string): Promise<void> {
    await api.post(`/phones/${publicId}/set-default`);
  },
};
