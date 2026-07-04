import api from "@/lib/axios";

export interface Category {
  public_id: string;
  name: string;
  slug: string;
  description: string | null;
  is_active: boolean;
}

export const categoryService = {
  // Public
  async getAll(activeOnly = true): Promise<Category[]> {
    const response = await api.get("/categories", { params: { active_only: activeOnly } });
    return response.data;
  },

  async getBySlug(slug: string): Promise<Category> {
    const response = await api.get(`/categories/slug/${slug}`);
    return response.data;
  },

  async getByPublicId(publicId: string): Promise<Category> {
    const response = await api.get(`/categories/${publicId}`);
    return response.data;
  },

  // Admin
  async create(data: { name: string; slug: string; description?: string; is_active?: boolean }): Promise<Category> {
    const response = await api.post("/categories", data);
    return response.data;
  },

  async update(publicId: string, data: Partial<{ name: string; slug: string; description: string; is_active: boolean }>): Promise<Category> {
    const response = await api.put(`/categories/${publicId}`, data);
    return response.data;
  },

  async delete(publicId: string): Promise<void> {
    await api.delete(`/categories/${publicId}`);
  },
};