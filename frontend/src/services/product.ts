import api from "@/lib/axios";

export interface ProductImage {
  public_id: string;
  stored_filename: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  alt_text: string | null;
  display_order: number;
  is_primary: boolean;
}

export interface Product {
  public_id: string;
  name: string;
  slug: string;
  price: number;
  discount_price: number | null;
  short_description: string | null;
  description: string | null;
  is_active: boolean;
  category: { public_id: string; name: string; slug: string };
  images: ProductImage[];
}

export const productService = {
  // Public
  async getAll(params?: { category?: string; search?: string }): Promise<Product[]> {
    const response = await api.get("/products", { params });
    return response.data;
  },

  async getByPublicId(publicId: string): Promise<Product> {
    const response = await api.get(`/products/${publicId}`);
    return response.data;
  },

  async getBySlug(slug: string): Promise<Product> {
    const response = await api.get(`/products/slug/${slug}`);
    return response.data;
  },

  async getRelated(publicId: string): Promise<Product[]> {
    const response = await api.get(`/products/${publicId}/related`);
    return response.data;
  },

  // Admin
  async create(data: {
    category_public_id: string;
    name: string;
    slug: string;
    price: number;
    discount_price?: number | null;
    short_description?: string | null;
    description?: string | null;
    is_active?: boolean;
  }): Promise<Product> {
    const response = await api.post("/products", data);
    return response.data;
  },

  async update(publicId: string, data: Partial<{
    category_public_id: string;
    name: string;
    slug: string;
    price: number;
    discount_price: number | null;
    short_description: string | null;
    description: string | null;
    is_active: boolean;
  }>): Promise<Product> {
    const response = await api.put(`/products/${publicId}`, data);
    return response.data;
  },

  async delete(publicId: string): Promise<void> {
    await api.delete(`/products/${publicId}`);
  },

  async uploadImage(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append("file", file);
    const response = await api.post("/products/upload-image", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },
};