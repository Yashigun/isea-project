import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";

import ReviewSummary from "@/components/ReviewSummary";
import ShopReviews from "@/components/ShopReviews";

import { reviewService } from "@/services/review";


export default async function ReviewPage() {
  const reviews =
    await reviewService.listAll();


  const reviewCount =
    reviews.length;


  const averageRating =
    reviewCount > 0
      ? reviews.reduce(
          (total, review) =>
            total + review.rating,
          0,
        ) / reviewCount
      : 0;


  return (
    <Section>

      <Container className="max-w-7xl">


        {/* PAGE HEADER */}

        <div className="py-8 text-center sm:py-12">

          <h1 className="text-4xl font-medium tracking-tight sm:text-6xl">
            Customer Reviews
          </h1>


          <p className="mt-3 text-gray-500">

            Rated{" "}

            {averageRating.toFixed(1)}

            {" "}with{" "}

            <span className="underline underline-offset-4">

              {reviewCount.toLocaleString()}{" "}

              {reviewCount === 1
                ? "review"
                : "reviews"}

            </span>

          </p>

        </div>


        {/* SUMMARY + GALLERY */}

        <div className="py-8 sm:py-10">

          <ReviewSummary
            reviews={reviews}
            showGallery
          />

        </div>


        {/* REVIEWS TAB */}

        <div className="mt-8 border-b">

          <div className="inline-block border-b-2 border-black px-4 pb-3 text-sm font-medium sm:text-base">
            Shop reviews
          </div>

        </div>


        {/* ALL REVIEW CARDS */}

        <div className="mt-7">

          <ShopReviews
            reviews={reviews}
            showReviewLink={false}
          />

        </div>


      </Container>

    </Section>
  );
}