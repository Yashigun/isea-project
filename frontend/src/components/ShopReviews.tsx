import Link from "next/link";
import { Star } from "lucide-react";

import type { Review } from "@/services/review";
import ReviewImageLightbox from "@/components/ReviewImageLightbox";


interface ShopReviewsProps {
  reviews: Review[];
  limit?: number;
  showReviewLink?: boolean;
}


export default function ShopReviews({
  reviews,
  limit,
  showReviewLink = true,
}: ShopReviewsProps) {
  const visibleReviews =
    typeof limit === "number"
      ? reviews.slice(0, limit)
      : reviews;


  return (
    <div>

      {visibleReviews.length === 0 ? (

        <p className="text-sm text-gray-500 sm:text-base">
          No reviews yet.
        </p>

      ) : (

        <div className="grid grid-cols-1 items-start gap-4 sm:grid-cols-2 md:grid-cols-3 md:gap-5 lg:grid-cols-4 lg:gap-6">

          {visibleReviews.map((item) => (

            <article
              key={item.public_id}
              className="mb-4 inline-block w-full break-inside-avoid overflow-hidden rounded-xl border bg-white md:mb-5 lg:mb-6"
            >

              {/* REVIEW IMAGES */}

              {item.images?.length > 0 && (
                <div
                  className={
                    item.images.length === 1
                      ? "h-72 w-full overflow-hidden bg-gray-100"
                      : "grid h-72 w-full grid-cols-2 gap-px overflow-hidden bg-gray-200"
                  }
                >
                  {item.images.map((image) => (
                    <div
                      key={image.public_id}
                      className="h-full min-w-0 overflow-hidden bg-gray-100"
                    >
                      <ReviewImageLightbox
                        src={image.image_url}
                        alt={`${item.customer.first_name}'s review attachment`}
                        thumbnailClassName="h-full w-full object-cover"
                      />
                    </div>
                  ))}
                </div>
              )}


              {/* REVIEW CONTENT */}

              <div className="p-4 sm:p-5">


                {/* STARS */}

                <div className="flex items-center gap-1 text-amber-500">

                  {[1, 2, 3, 4, 5].map((value) => (

                    <Star
                      key={value}
                      size={16}
                      fill={
                        value <= item.rating
                          ? "currentColor"
                          : "none"
                      }
                    />

                  ))}

                </div>


                {/* TITLE */}

                <h3 className="mt-2 text-sm font-medium sm:text-base">
                  {item.title}
                </h3>


                {/* REVIEW */}

                <p className="mt-2 break-words text-sm leading-6 text-gray-600 sm:text-base sm:leading-7">
                  {item.review}
                </p>


                {/* CUSTOMER */}

                <p className="mt-2 text-xs text-gray-400 sm:text-sm">

                  {item.customer.first_name}{" "}

                  {item.customer.last_name ?? ""}


                  {item.age
                    ? `, ${item.age}`
                    : ""}

                </p>

              </div>

            </article>

          ))}

        </div>

      )}


      {showReviewLink &&
        reviews.length > 0 && (

          <Link
            href="/review"
            className="mt-5 inline-block text-sm font-medium sm:mt-6"
          >
            Review -&gt;
          </Link>

        )}

    </div>
  );
}