import { Star } from "lucide-react";

import type { Review } from "@/services/review";
import ReviewImageLightbox from "@/components/ReviewImageLightbox";

interface ReviewSummaryProps {
  reviews: Review[];
  showGallery?: boolean;
}


const RATING_VALUES = [5, 4, 3, 2, 1];


export default function ReviewSummary({
  reviews,
  showGallery = false,
}: ReviewSummaryProps) {
  const reviewCount = reviews.length;


  const averageRating =
    reviewCount > 0
      ? reviews.reduce(
          (total, review) => total + review.rating,
          0,
        ) / reviewCount
      : 0;


  const ratingBreakdown = RATING_VALUES.map(
    (ratingValue) => {
      const count = reviews.filter(
        (review) => review.rating === ratingValue,
      ).length;


      const percentage =
        reviewCount > 0
          ? (count / reviewCount) * 100
          : 0;


      return {
        rating: ratingValue,
        percentage,
      };
    },
  );


  const galleryImages = reviews.flatMap((review) =>
    (review.images ?? []).map((image) => ({
      ...image,

      customerName: [
        review.customer.first_name,
        review.customer.last_name,
      ]
        .filter(Boolean)
        .join(" "),
    })),
  );


  return (
    <div className="w-full">

      {/* SUMMARY ROW */}

      <div className="flex flex-col gap-8 md:flex-row md:items-center">


        {/* AVERAGE RATING */}

        <div className="shrink-0">

          <div className="flex items-end gap-2">

            <span className="text-5xl font-medium tracking-tight text-gray-900">
              {averageRating.toFixed(1)}
            </span>


            <Star
              size={23}
              fill="currentColor"
              className="mb-1 text-amber-500"
              aria-hidden="true"
            />

          </div>


          <p className="mt-2 text-sm text-gray-600">
            {reviewCount.toLocaleString()}{" "}
            {reviewCount === 1
              ? "review"
              : "reviews"}
          </p>

        </div>


        {/* RATING BREAKDOWN */}

        <div className="w-full max-w-md">

          {ratingBreakdown.map(
            ({
              rating,
              percentage,
            }) => (

              <div
                key={rating}
                className="mb-2 flex items-center gap-3"
              >

                {/* STAR NUMBER */}

                <span className="w-3 shrink-0 text-sm text-gray-700">
                  {rating}
                </span>


                {/* STARS */}

                <div className="flex w-[92px] shrink-0">

                  {[1, 2, 3, 4, 5].map(
                    (value) => (

                      <Star
                        key={value}
                        size={17}
                        fill="currentColor"
                        className={
                          value <= rating
                            ? "text-amber-500"
                            : "text-gray-300"
                        }
                        aria-hidden="true"
                      />

                    ),
                  )}

                </div>


                {/* BAR */}

                <div className="h-2.5 min-w-0 flex-1 overflow-hidden rounded-full bg-gray-200">

                  <div
                    className="h-full rounded-full bg-amber-400"
                    style={{
                      width: `${percentage}%`,
                    }}
                  />

                </div>


                {/* PERCENT */}

                <span className="w-10 shrink-0 text-right text-sm text-gray-600">
                  {Math.round(percentage)}%
                </span>

              </div>

            ),
          )}

        </div>


        {/* IMAGE GALLERY */}

        {showGallery && galleryImages.length > 0 && (
        <div className="min-w-0 flex-1">

            <div className="flex flex-wrap items-center gap-2">

            {galleryImages
                .slice(0, 5)
                .map((image) => (

                <div
                    key={image.public_id}
                    className="h-20 w-20 shrink-0 overflow-hidden rounded-lg border border-gray-200 bg-gray-100"
                >
                    <ReviewImageLightbox
                    src={image.image_url}
                    alt={`Review uploaded by ${image.customerName}`}
                    thumbnailClassName="h-20 w-20"
                    />
                </div>

                ))}

            </div>


            <p className="mt-2 text-xs text-gray-500">
            {galleryImages.length.toLocaleString()}{" "}
            customer{" "}
            {galleryImages.length === 1
                ? "photo"
                : "photos"}
            </p>

        </div>
        )}

      </div>

    </div>
  );
}