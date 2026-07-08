import api from "@/lib/axios";

export interface ReviewImage {
  public_id: string;
  image_url: string;
  cloudinary_public_id: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  created_at: string;
}

export interface Review {
  public_id: string;
  rating: number;
  title: string;
  review: string;
  age: string | null;
  customer: {
    public_id: string;
    first_name: string;
    last_name: string | null;
  };
  images: ReviewImage[];
  created_at: string;
}

export const reviewService = {
  async listAll(limit?: number): Promise<Review[]> {
    const response = await api.get("/reviews/", { params: limit ? { limit } : undefined });
    return response.data;
  },

  async getProductReviews(productPublicId: string): Promise<Review[]> {
    const response = await api.get(`/reviews/product/${productPublicId}`);
    return response.data;
  },

  async create(productPublicId: string, data: { rating: number; title: string; review: string; age?: string | null }): Promise<Review> {
    const response = await api.post(`/reviews/product/${productPublicId}`, data);
    return response.data;
  },

  async uploadImages(reviewPublicId: string, images: File[]): Promise<Review> {
    const formData = new FormData();

    images.forEach((image) => {
      formData.append("files", image);
    });

    const response = await api.post(
      `/reviews/${reviewPublicId}/images`,
      formData,
    );

    return response.data;
  },

  async update(reviewPublicId: string, data: { rating?: number; title?: string; review?: string; age?: string | null }): Promise<Review> {
    const response = await api.put(`/reviews/${reviewPublicId}`, data);
    return response.data;
  },

  async delete(reviewPublicId: string): Promise<void> {
    await api.delete(`/reviews/${reviewPublicId}`);
  },
};