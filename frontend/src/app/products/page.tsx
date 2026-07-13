import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";
import SectionHeading from "@/components/common/SectionHeading";
import ProductCatalog from "@/components/ProductCatalog";

import { categoryService } from "@/services/category";
import { productService } from "@/services/product";

export const dynamic = "force-dynamic";

export default async function ProductsPage() {
  const [productsResult, categoriesResult] =
    await Promise.allSettled([
      productService.getAll(),
      categoryService.getAll(),
    ]);

  const products =
    productsResult.status === "fulfilled"
      ? productsResult.value
      : [];

  const categories =
    categoriesResult.status === "fulfilled"
      ? categoriesResult.value
      : [];

  if (productsResult.status === "rejected") {
    console.error(
      "Failed to fetch products:",
      productsResult.reason,
    );
  }

  if (categoriesResult.status === "rejected") {
    console.error(
      "Failed to fetch categories:",
      categoriesResult.reason,
    );
  }

  return (
    <Section>
      <Container>
        <SectionHeading
          title="Shop"
          subtitle="Browse all our handcrafted products."
        />

        <ProductCatalog
          products={products}
          categories={categories}
        />
      </Container>
    </Section>
  );
}