import axios from "axios";
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

export interface ReviewCustomer {
  public_id: string;
  first_name: string;
  last_name: string | null;
}

export interface Review {
  public_id: string;
  rating: number;
  title: string;
  review: string;
  age: string | null;
  customer: ReviewCustomer;
  images: ReviewImage[];
  created_at: string;
}

export interface CreateReviewPayload {
  rating: number;
  title: string;
  review: string;
  age?: string | null;
}

export interface UpdateReviewPayload {
  rating?: number;
  title?: string;
  review?: string;
  age?: string | null;
}

function encodePathSegment(value: string): string {
  return encodeURIComponent(value);
}

export function getReviewErrorMessage(
  error: unknown,
  fallback = "Something went wrong.",
): string {
  if (!axios.isAxiosError(error)) {
    return fallback;
  }

  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => {
        if (
          typeof item === "object" &&
          item !== null &&
          "msg" in item &&
          typeof item.msg === "string"
        ) {
          return item.msg;
        }

        return null;
      })
      .filter((message): message is string => message !== null);

    if (messages.length > 0) {
      return messages.join(" ");
    }
  }

  return fallback;
}

export const reviewService = {
  async listAll(limit?: number): Promise<Review[]> {
    const response = await api.get<Review[]>("/reviews/", {
      params: limit !== undefined ? { limit } : undefined,
    });

    return response.data;
  },

  async getProductReviews(
    productPublicId: string,
    limit = 100,
  ): Promise<Review[]> {
    const response = await api.get<Review[]>(
      `/reviews/product/${encodePathSegment(productPublicId)}`,
      {
        params: { limit },
      },
    );

    return response.data;
  },

  async create(
    productPublicId: string,
    data: CreateReviewPayload,
  ): Promise<Review> {
    const response = await api.post<Review>(
      `/reviews/product/${encodePathSegment(productPublicId)}`,
      data,
    );

    return response.data;
  },

  async uploadImages(
    reviewPublicId: string,
    images: File[],
  ): Promise<Review> {
    if (images.length === 0) {
      throw new Error("At least one image is required.");
    }

    const formData = new FormData();

    images.forEach((image) => {
      formData.append("files", image, image.name);
    });

    const response = await api.post<Review>(
      `/reviews/${encodePathSegment(reviewPublicId)}/images`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );

    return response.data;
  },

  async update(
    reviewPublicId: string,
    data: UpdateReviewPayload,
  ): Promise<Review> {
    const response = await api.put<Review>(
      `/reviews/${encodePathSegment(reviewPublicId)}`,
      data,
    );

    return response.data;
  },

  /**
   * This endpoint must only be called from an admin UI.
   *
   * Authorization is still enforced by the backend.
   * Hiding a delete button in the frontend is not security.
   */
  async deleteByAdmin(reviewPublicId: string): Promise<void> {
    await api.delete(
      `/reviews/${encodePathSegment(reviewPublicId)}`,
    );
  },
};