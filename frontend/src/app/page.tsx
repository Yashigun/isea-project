
import Hero from "@/components/Hero";
import CollectionGrid from "@/components/CollectionGrid";
import ProductGrid from "@/components/ProductGrid";

import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";
import SectionHeading from "@/components/common/SectionHeading";
import ShopReviews from "@/components/ShopReviews";

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
      categoriesResult.reason
    );
  }

  if (productsResult.status === "rejected") {
    console.error(
      "Failed to fetch homepage products:",
      productsResult.reason
    );
  }

  if (reviewsResult.status === "rejected") {
    console.error(
      "Failed to fetch homepage reviews:",
      reviewsResult.reason
    );
  }

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

          <ProductGrid products={products} />
        </Container>
      </Section>

      <Section>
        <Container className="max-w-3xl">
          <SectionHeading
            title="Shop Reviews"
            subtitle="What customers are saying."
          />

          <ShopReviews reviews={reviews} />
        </Container>
      </Section>
    </>
  );
}

