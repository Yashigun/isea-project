import api from "@/lib/axios";

export interface Address {
  public_id: string;
  address_line_1: string;
  address_line_2: string | null;
  city: string;
  state: string;
  country: string;
  postal_code: string;
  is_default: boolean;
}

export const addressService = {
  async getAll(): Promise<Address[]> {
    const response = await api.get("/addresses");
    return response.data;
  },

  async create(data: Omit<Address, "public_id">): Promise<Address> {
    const response = await api.post("/addresses", data);
    return response.data;
  },

  async update(publicId: string, data: Partial<Omit<Address, "public_id">>): Promise<Address> {
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