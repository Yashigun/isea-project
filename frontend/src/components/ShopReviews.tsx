import Link from "next/link";
import { Star } from "lucide-react";
import { Review } from "@/services/review";

interface ShopReviewsProps {
  reviews: Review[];
}

export default function ShopReviews({ reviews }: ShopReviewsProps) {
  return (
    <div>
      <div className="space-y-4 sm:space-y-5 lg:space-y-6">
        {reviews.length === 0 ? (
          <p className="text-sm text-gray-500 sm:text-base">No reviews yet.</p>
        ) : (
          reviews.slice(0, 5).map((item) => (
            <article
              key={item.public_id}
              className="border-b pb-4 sm:pb-5"
            >
              <div className="flex items-center gap-1 text-amber-500">
                {[1, 2, 3, 4, 5].map((value) => (
                  <Star
                    key={value}
                    size={16}
                    fill={value <= item.rating ? "currentColor" : "none"}
                  />
                ))}
              </div>

              <h3 className="mt-2 text-sm font-medium sm:text-base">
                {item.title}
              </h3>

              <p className="mt-2 text-sm leading-6 text-gray-600 sm:text-base sm:leading-7">
                {item.review}
              </p>

              <p className="mt-2 text-xs text-gray-400 sm:text-sm">
                {item.customer.first_name} {item.customer.last_name ?? ""}
                {item.age ? `, ${item.age}` : ""}
              </p>
            </article>
          ))
        )}
      </div>

      <Link
        href="/review"
        className="mt-5 inline-block text-sm font-medium sm:mt-6"
      >
        Review -&gt;
      </Link>
    </div>
  );
}

