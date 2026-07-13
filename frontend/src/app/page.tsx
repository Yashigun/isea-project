
import Link from "next/link";

import Hero from "@/components/Hero";
import CollectionGrid from "@/components/CollectionGrid";
import ProductGrid from "@/components/ProductGrid";

import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";
import SectionHeading from "@/components/common/SectionHeading";
import ShopReviews from "@/components/ShopReviews";
import ReviewSummary from "@/components/ReviewSummary";

import { categoryService } from "@/services/category";
import { productService } from "@/services/product";
import { reviewService } from "@/services/review";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const [categoriesResult, productsResult, reviewsResult] =
    await Promise.allSettled([
      categoryService.getAll(),
      productService.getAll(),
      reviewService.listAll(5),
    ]);

  const categories =
    categoriesResult.status === "fulfilled"
      ? categoriesResult.value
      : [];

  const products =
    productsResult.status === "fulfilled"
      ? productsResult.value
      : [];

  const reviews =
    reviewsResult.status === "fulfilled"
      ? reviewsResult.value
      : [];

  if (categoriesResult.status === "rejected") {
    console.error(
      "Failed to fetch homepage categories:",
      categoriesResult.reason,
    );
  }

  if (productsResult.status === "rejected") {
    console.error(
      "Failed to fetch homepage products:",
      productsResult.reason,
    );
  }

  if (reviewsResult.status === "rejected") {
    console.error(
      "Failed to fetch homepage reviews:",
      reviewsResult.reason,
    );
  }

  const featuredProducts = products.slice(0, 6);

  return (
    <>
      <Hero />

      <Section>
        <Container>
          <SectionHeading
            title="Shop by Collection"
            subtitle="Browse our carefully curated collections."
          />

          <CollectionGrid categories={categories} />
        </Container>
      </Section>

      <Section>
        <Container>
          <SectionHeading
            title="Our Products"
            subtitle="Handcrafted pieces you'll love."
          />

          <ProductGrid products={featuredProducts} />

          {products.length > 4 && (
            <div className="mt-8 flex justify-center sm:mt-10">
              <Link
                href="/products"
                className="
                  mt-6
                  rounded-full
                  border
                  border-black
                  px-6
                  py-2.5
                  text-sm
                  transition
                  duration-300
                  hover:bg-black
                  hover:text-white
                  sm:mt-8
                  sm:px-7
                  sm:py-3
                  sm:text-base
                  lg:mt-10
                  lg:px-8
                "
              >
                View All Products
              </Link>
            </div>
          )}
        </Container>
      </Section>

      <Section>
        <Container className="max-w-3xl">
          <SectionHeading
            title="Shop Reviews"
            subtitle="What customers are saying."
          />

          <div className="space-y-8">
            <ReviewSummary reviews={reviews} />

            <ShopReviews
              reviews={reviews}
              limit={8}
            />
          </div>
        </Container>
      </Section>
    </>
  );
}
