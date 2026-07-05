import Link from "next/link";
import { Star } from "lucide-react";
import { Review } from "@/services/review";

interface ShopReviewsProps {
  reviews: Review[];
}

export default function ShopReviews({ reviews }: ShopReviewsProps) {
  return (
    <div>
      <div className="space-y-6">
        {reviews.length === 0 ? (
          <p className="text-gray-500">No reviews yet.</p>
        ) : (
          reviews.slice(0, 5).map((item) => (
            <article key={item.public_id} className="border-b pb-5">
              <div className="flex items-center gap-1 text-amber-500">
                {[1, 2, 3, 4, 5].map((value) => (
                  <Star
                    key={value}
                    size={16}
                    fill={value <= item.rating ? "currentColor" : "none"}
                  />
                ))}
              </div>
              <h3 className="mt-2 font-medium">{item.title}</h3>
              <p className="mt-2 leading-7 text-gray-600">{item.review}</p>
              <p className="mt-2 text-sm text-gray-400">
                {item.customer.first_name} {item.customer.last_name ?? ""}
                {item.age ? `, ${item.age}` : ""}
              </p>
            </article>
          ))
        )}
      </div>

      <Link href="/review" className="mt-6 inline-block text-sm font-medium">
        Review -&gt;
      </Link>
    </div>
  );
}
