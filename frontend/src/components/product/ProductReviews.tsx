"use client";

import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
import { ImagePlus, Star } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { reviewService, Review } from "@/services/review";

interface ProductReviewsProps {
  productPublicId: string;
}

export default function ProductReviews({ productPublicId }: ProductReviewsProps) {
  const { isAuthenticated } = useAuth();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [rating, setRating] = useState(0);
  const [title, setTitle] = useState("");
  const [age, setAge] = useState("");
  const [review, setReview] = useState("");
  const [images, setImages] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadReviews = useCallback(async () => {
    try {
      setReviews(await reviewService.getProductReviews(productPublicId));
    } catch (err) {
      console.error("Failed to load reviews:", err);
    }
  }, [productPublicId]);

  useEffect(() => {
    void Promise.resolve().then(loadReviews);
  }, [loadReviews]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);

    if (!isAuthenticated) {
      setError("Please sign in to write a review.");
      return;
    }

    if (rating < 1) {
      setError("Please select a rating.");
      return;
    }

    setLoading(true);
    try {
      await reviewService.create(productPublicId, {
        rating,
        title,
        review,
        age: age || null,
      });
      setRating(0);
      setTitle("");
      setAge("");
      setReview("");
      setImages([]);
      await loadReviews();
    } catch (err: unknown) {
      const detail =
        typeof err === "object" &&
        err !== null &&
        "response" in err &&
        typeof (err as { response?: { data?: { detail?: unknown } } }).response?.data?.detail === "string"
          ? (err as { response: { data: { detail: string } } }).response.data.detail
          : null;
      setError(detail || "Could not submit review.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-8 sm:gap-10 lg:grid-cols-[1fr_420px]">
      <div>
        <h2 className="text-2xl font-medium sm:text-3xl">Customer Reviews</h2>
        <div className="mt-5 space-y-4 sm:mt-6">
          {reviews.length === 0 ? (
            <p className="rounded-lg bg-gray-50 p-4 text-gray-500 sm:p-6">
              No reviews yet.
            </p>
          ) : (
            reviews.map((item) => (
              <article key={item.public_id} className="rounded-lg border bg-white p-4 sm:p-5">
                <div className="flex items-center gap-1 text-amber-500">
                  {[1, 2, 3, 4, 5].map((value) => (
                    <Star
                      key={value}
                      size={16}
                      fill={value <= item.rating ? "currentColor" : "none"}
                    />
                  ))}
                </div>
                <h3 className="mt-3 font-semibold">{item.title}</h3>
                <p className="mt-2 break-words leading-7 text-gray-600">{item.review}</p>
                <p className="mt-3 break-words text-sm text-gray-400">
                  {item.customer.first_name} {item.customer.last_name ?? ""}
                  {item.age ? `, ${item.age}` : ""}
                </p>
              </article>
            ))
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="rounded-lg border bg-white p-4 sm:p-6">
        <h3 className="text-lg font-medium sm:text-xl">Write a Review</h3>
        {error && <p className="mt-3 break-words text-sm text-red-600">{error}</p>}

        <p className="mt-5 text-sm font-medium">Rating</p>
        <div className="mt-2 flex items-center gap-1">
          {[1, 2, 3, 4, 5].map((value) => (
            <button
              key={value}
              type="button"
              onClick={() => setRating(value)}
              aria-label={`${value} star rating`}
              className="rounded-full p-1 text-amber-500 transition hover:scale-110"
            >
              <Star
                size={26}
                fill={value <= rating ? "currentColor" : "none"}
              />
            </button>
          ))}
        </div>

        <label className="mt-4 block text-sm font-medium">Title</label>
        <input
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
          className="mt-2 w-full rounded-lg border px-3 py-2"
        />

        <label className="mt-4 block text-sm font-medium">Review</label>
        <textarea
          value={review}
          onChange={(event) => setReview(event.target.value)}
          required
          rows={5}
          className="mt-2 w-full rounded-lg border px-3 py-2"
        />

        <label className="mt-4 flex items-center gap-2 text-sm font-medium">
          <ImagePlus size={18} />
          Attach images
        </label>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={(event) => setImages(Array.from(event.target.files ?? []).slice(0, 2))}
          className="mt-2 w-full max-w-full text-sm"
        />
        <p className="mt-1 text-xs text-gray-500">{images.length}/2 selected</p>

        <button
          type="submit"
          disabled={loading}
          className="mt-6 w-full rounded-full bg-black px-5 py-3 text-white disabled:opacity-50"
        >
          {loading ? "Submitting..." : "Submit Review"}
        </button>
      </form>
    </div>
  );
}
