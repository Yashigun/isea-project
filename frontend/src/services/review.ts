import api from "@/lib/axios";

export interface Review {
  public_id: string;
  rating: number;
  title: string;
  review: string;
  customer: customer;
  created_at: string;
}

export const reviewService = {
  async getProductReviews(productPublicId: string): Promise<Review[]> {
    const response = await api.get(`/reviews/product/${productPublicId}`);
    return response.data;
  },

  async create(productPublicId: string, data: { rating: number; title: string; review: string }): Promise<Review> {
    const response = await api.post(`/reviews/product/${productPublicId}`, data);
    return response.data;
  },

  async update(reviewPublicId: string, data: { rating?: number; title?: string; review?: string }): Promise<Review> {
    const response = await api.put(`/reviews/${reviewPublicId}`, data);
    return response.data;
  },

  async delete(reviewPublicId: string): Promise<void> {
    await api.delete(`/reviews/${reviewPublicId}`);
  },
};