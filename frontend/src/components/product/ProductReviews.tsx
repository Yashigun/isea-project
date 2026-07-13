"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import type {
  ChangeEvent,
  FormEvent,
} from "react";

import {
  ImagePlus,
  Star,
  X,
} from "lucide-react";

import { useAuth } from "@/context/AuthContext";

import {
  getReviewErrorMessage,
  reviewService,
} from "@/services/review";

import type {
  Review,
} from "@/services/review";


interface ProductReviewsProps {
  productPublicId: string;
}


const MAX_REVIEW_IMAGES = 2;

/*
 * Keep this value synchronized with your backend validator.
 *
 * Change it if your backend uses a different maximum file size.
 */
const MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024;


const ALLOWED_IMAGE_TYPES = new Set([
  "image/jpeg",
  "image/png",
  "image/webp",
]);


interface SelectedImage {
  file: File;
  previewUrl: string;
}


function createSelectedImage(
  file: File,
): SelectedImage {
  return {
    file,
    previewUrl: URL.createObjectURL(file),
  };
}


function revokeSelectedImages(
  images: SelectedImage[],
): void {
  for (const image of images) {
    URL.revokeObjectURL(image.previewUrl);
  }
}


export default function ProductReviews({
  productPublicId,
}: ProductReviewsProps) {
  const { isAuthenticated } = useAuth();

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const selectedImagesRef = useRef<SelectedImage[]>([]);

  const [reviews, setReviews] = useState<Review[]>([]);

  const [rating, setRating] = useState(0);

  const [title, setTitle] = useState("");

  const [age, setAge] = useState("");

  const [reviewText, setReviewText] = useState("");

  const [selectedImages, setSelectedImages] = useState<
    SelectedImage[]
  >([]);

  const [loadingReviews, setLoadingReviews] = useState(true);

  const [submitting, setSubmitting] = useState(false);

  const [error, setError] = useState<string | null>(null);


  /*
   * Keep the ref synchronized so unmount cleanup can access
   * the latest preview URLs.
   */
  useEffect(() => {
    selectedImagesRef.current = selectedImages;
  }, [selectedImages]);


  /*
   * Cleanup browser object URLs when the component unmounts.
   */
  useEffect(() => {
    return () => {
      revokeSelectedImages(selectedImagesRef.current);
    };
  }, []);


  const loadReviews = useCallback(async () => {
    setLoadingReviews(true);

    try {
      const data = await reviewService.getProductReviews(
        productPublicId,
      );

      setReviews(data);

    } catch (requestError: unknown) {
      console.error(
        "Failed to load product reviews:",
        requestError,
      );

      setError(
        getReviewErrorMessage(
          requestError,
          "Could not load reviews.",
        ),
      );

    } finally {
      setLoadingReviews(false);
    }
  }, [productPublicId]);


  useEffect(() => {
    void loadReviews();
  }, [loadReviews]);


  const resetForm = useCallback(() => {
    setRating(0);

    setTitle("");

    setAge("");

    setReviewText("");

    setSelectedImages((currentImages) => {
      revokeSelectedImages(currentImages);

      return [];
    });

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }, []);


  const handleImageSelection = (
    event: ChangeEvent<HTMLInputElement>,
  ) => {
    setError(null);

    const files = Array.from(
      event.target.files ?? [],
    );

    /*
     * Reset the native input immediately.
     *
     * This allows the customer to select the same file again
     * after removing it.
     */
    event.target.value = "";

    if (files.length === 0) {
      return;
    }

    if (
      selectedImages.length + files.length >
      MAX_REVIEW_IMAGES
    ) {
      setError(
        `You can attach a maximum of ${MAX_REVIEW_IMAGES} images.`,
      );

      return;
    }

    for (const file of files) {
      if (!ALLOWED_IMAGE_TYPES.has(file.type)) {
        setError(
          "Only JPEG, PNG, and WebP images are allowed.",
        );

        return;
      }

      if (file.size <= 0) {
        setError("Empty image files are not allowed.");

        return;
      }

      if (file.size > MAX_IMAGE_SIZE_BYTES) {
        setError(
          "Each image must be 5 MB or smaller.",
        );

        return;
      }
    }

    /*
     * Prevent duplicate file selection in the same review.
     *
     * This is a UI convenience only.
     * Backend validation remains authoritative.
     */
    const existingFileKeys = new Set(
      selectedImages.map(
        ({ file }) =>
          `${file.name}:${file.size}:${file.lastModified}`,
      ),
    );

    const uniqueFiles = files.filter((file) => {
      const fileKey =
        `${file.name}:${file.size}:${file.lastModified}`;

      return !existingFileKeys.has(fileKey);
    });

    if (uniqueFiles.length !== files.length) {
      setError("The same image cannot be selected twice.");

      return;
    }

    const newImages = uniqueFiles.map(
      createSelectedImage,
    );

    setSelectedImages((currentImages) => [
      ...currentImages,
      ...newImages,
    ]);
  };


  const removeSelectedImage = (
    previewUrl: string,
  ) => {
    setSelectedImages((currentImages) => {
      const imageToRemove = currentImages.find(
        (image) => image.previewUrl === previewUrl,
      );

      if (imageToRemove) {
        URL.revokeObjectURL(imageToRemove.previewUrl);
      }

      return currentImages.filter(
        (image) => image.previewUrl !== previewUrl,
      );
    });
  };


  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (submitting) {
      return;
    }

    setError(null);


    if (!isAuthenticated) {
      setError("Please sign in to write a review.");

      return;
    }


    const normalizedTitle = title.trim();

    const normalizedReview = reviewText.trim();

    const normalizedAge = age.trim();


    if (rating < 1 || rating > 5) {
      setError("Please select a rating.");

      return;
    }


    if (
      normalizedTitle.length < 2 ||
      normalizedTitle.length > 150
    ) {
      setError(
        "Title must contain between 2 and 150 characters.",
      );

      return;
    }


    if (
      normalizedReview.length < 2 ||
      normalizedReview.length > 5000
    ) {
      setError(
        "Review must contain between 2 and 5000 characters.",
      );

      return;
    }


    if (normalizedAge.length > 20) {
      setError(
        "Age must contain 20 characters or fewer.",
      );

      return;
    }


    setSubmitting(true);


    try {
      /*
       * Request 1:
       * Create/update the customer's review.
       */
      const createdReview = await reviewService.create(
        productPublicId,
        {
          rating,
          title: normalizedTitle,
          review: normalizedReview,
          age: normalizedAge || null,
        },
      );


      /*
       * Request 2:
       * Upload images only when images were selected.
       *
       * The backend returns the review again with its
       * eagerly-loaded images.
       */
      const finalReview =
        selectedImages.length > 0
          ? await reviewService.uploadImages(
              createdReview.public_id,
              selectedImages.map(({ file }) => file),
            )
          : createdReview;


      /*
       * Update local state instead of making another GET request.
       *
       * If this is a new review, prepend it.
       *
       * If the customer already had a review and the backend
       * updated it, replace the existing review.
       */
      setReviews((currentReviews) => {
        const reviewExists = currentReviews.some(
          (item) => item.public_id === finalReview.public_id,
        );

        if (reviewExists) {
          return currentReviews.map((item) =>
            item.public_id === finalReview.public_id
              ? finalReview
              : item,
          );
        }

        return [
          finalReview,
          ...currentReviews,
        ];
      });


      resetForm();

    } catch (requestError: unknown) {
      console.error(
        "Failed to submit review:",
        requestError,
      );

      setError(
        getReviewErrorMessage(
          requestError,
          "Could not submit review.",
        ),
      );

    } finally {
      setSubmitting(false);
    }
  };


  return (
    <div className="grid gap-8 sm:gap-10 lg:grid-cols-[1fr_420px]">

      {/* REVIEWS */}

      <section>
        <h2 className="text-2xl font-medium sm:text-3xl">
          Customer Reviews
        </h2>


        <div className="mt-5 space-y-4 sm:mt-6">

          {loadingReviews ? (
            <p className="rounded-lg bg-gray-50 p-4 text-gray-500 sm:p-6">
              Loading reviews...
            </p>

          ) : reviews.length === 0 ? (
            <p className="rounded-lg bg-gray-50 p-4 text-gray-500 sm:p-6">
              No reviews yet.
            </p>

          ) : (
            reviews.map((item) => (
              <article
                key={item.public_id}
                className="rounded-lg border bg-white p-5 sm:p-6"
              >
                {/*
                  Desktop:
                  text content | images

                  Mobile:
                  text content
                  images
                */}
                <div className="flex flex-col gap-5 md:flex-row md:items-start md:justify-between">

                  {/* LEFT SIDE: REVIEW CONTENT */}
                  <div className="min-w-0 flex-1">

                    {/* CUSTOMER NAME */}
                    <p className="break-words font-medium text-gray-900">
                      {item.customer.first_name}

                      {item.customer.last_name
                        ? ` ${item.customer.last_name}`
                        : ""}

                      {item.age
                        ? `, ${item.age}`
                        : ""}
                    </p>


                    {/* RATING */}
                    <div
                      className="mt-2 flex items-center gap-1 text-amber-500"
                      aria-label={`${item.rating} out of 5 stars`}
                    >
                      {[1, 2, 3, 4, 5].map((value) => (
                        <Star
                          key={value}
                          size={18}
                          fill={
                            value <= item.rating
                              ? "currentColor"
                              : "none"
                          }
                          aria-hidden="true"
                        />
                      ))}
                    </div>


                    {/* TITLE */}
                    <h3 className="mt-4 font-semibold">
                      {item.title}
                    </h3>


                    {/* REVIEW */}
                    <p className="mt-2 break-words leading-7 text-gray-600">
                      {item.review}
                    </p>

                  </div>


                  {/* RIGHT SIDE: REVIEW IMAGES */}
                  {item.images?.length > 0 && (
                    <div
                      className="
                        flex shrink-0 flex-wrap gap-3
                        md:max-w-[340px]
                        md:justify-end
                      "
                    >
                      {item.images.map((image) => (
                        <a
                          key={image.public_id}
                          href={image.image_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="
                            block
                            overflow-hidden
                            rounded-xl
                            border
                            border-gray-200
                          "
                        >
                          <img
                            src={image.image_url}
                            alt={`${item.customer.first_name}'s review attachment`}
                            loading="lazy"
                            decoding="async"
                            className="
                              h-40
                              w-40
                              object-cover
                              transition-transform
                              duration-200
                              hover:scale-105

                              sm:h-44
                              sm:w-44

                              md:h-40
                              md:w-40
                            "
                          />
                        </a>
                      ))}
                    </div>
                  )}

                </div>
              </article>
            ))
          )}

        </div>
      </section>


      {/* REVIEW FORM */}

      <form
        onSubmit={handleSubmit}
        className="rounded-lg border bg-white p-4 sm:p-6"
      >

        <h3 className="text-lg font-medium sm:text-xl">
          Write a Review
        </h3>


        {error && (
          <p
            role="alert"
            className="mt-3 break-words text-sm text-red-600"
          >
            {error}
          </p>
        )}


        {/* RATING */}

        <fieldset
          disabled={submitting}
          className="mt-5"
        >
          <legend className="text-sm font-medium">
            Rating
          </legend>

          <div className="mt-2 flex items-center gap-1">

            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                onClick={() => setRating(value)}
                aria-label={`${value} star rating`}
                aria-pressed={rating === value}
                className="rounded-full p-1 text-amber-500 transition hover:scale-110 focus:outline-none focus:ring-2 focus:ring-black"
              >
                <Star
                  size={26}
                  fill={
                    value <= rating
                      ? "currentColor"
                      : "none"
                  }
                  aria-hidden="true"
                />
              </button>
            ))}

          </div>
        </fieldset>


        {/* TITLE */}

        <label
          htmlFor="review-title"
          className="mt-4 block text-sm font-medium"
        >
          Title
        </label>

        <input
          id="review-title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
          minLength={2}
          maxLength={150}
          disabled={submitting}
          autoComplete="off"
          className="mt-2 w-full rounded-lg border px-3 py-2 disabled:opacity-60"
        />


        {/* REVIEW */}

        <label
          htmlFor="review-text"
          className="mt-4 block text-sm font-medium"
        >
          Review
        </label>

        <textarea
          id="review-text"
          value={reviewText}
          onChange={(event) => setReviewText(event.target.value)}
          required
          minLength={2}
          maxLength={5000}
          disabled={submitting}
          rows={5}
          className="mt-2 w-full rounded-lg border px-3 py-2 disabled:opacity-60"
        />


        {/* IMAGE UPLOAD */}

        <label
          htmlFor="review-images"
          className="mt-4 flex items-center gap-2 text-sm font-medium"
        >
          <ImagePlus
            size={18}
            aria-hidden="true"
          />

          Attach images
        </label>


        <input
          ref={fileInputRef}
          id="review-images"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          disabled={
            submitting ||
            selectedImages.length >= MAX_REVIEW_IMAGES
          }
          onChange={handleImageSelection}
          className="mt-2 w-full max-w-full text-sm disabled:opacity-60"
        />


        <p className="mt-1 text-xs text-gray-500">
          {selectedImages.length}/{MAX_REVIEW_IMAGES} selected.
          JPEG, PNG, or WebP. Maximum 5 MB each.
        </p>


        {/* IMAGE PREVIEWS */}

        {selectedImages.length > 0 && (
          <div className="mt-4 grid grid-cols-2 gap-3">

            {selectedImages.map((image) => (
              <div
                key={image.previewUrl}
                className="relative overflow-hidden rounded-lg border"
              >
                <img
                  src={image.previewUrl}
                  alt={`Selected file: ${image.file.name}`}
                  className="h-32 w-full object-cover"
                />

                <button
                  type="button"
                  disabled={submitting}
                  onClick={() =>
                    removeSelectedImage(image.previewUrl)
                  }
                  aria-label={`Remove ${image.file.name}`}
                  className="absolute right-2 top-2 rounded-full bg-black/70 p-1 text-white transition hover:bg-black disabled:opacity-50"
                >
                  <X
                    size={16}
                    aria-hidden="true"
                  />
                </button>
              </div>
            ))}

          </div>
        )}


        {/* SUBMIT */}

        <button
          type="submit"
          disabled={submitting}
          className="mt-6 w-full rounded-full bg-black px-5 py-3 text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting
            ? selectedImages.length > 0
              ? "Submitting review..."
              : "Submitting..."
            : "Submit Review"}
        </button>

      </form>

    </div>
  );
}