import Container from "@/components/layout/Container";
import ProductGrid from "@/components/ProductGrid";
import Section from "@/components/ui/Section";
import SectionHeading from "@/components/common/SectionHeading";

import { getCategoryBySlug } from "@/services/category";
import { getProductsByCategory } from "@/services/product";

interface Props {
  params: Promise<{
    slug: string;
  }>;
}

export default async function CollectionPage({ params }: Props) {
  const { slug } = await params;

  const category = await getCategoryBySlug(slug);

  if (!category) {
    return (
      <Container>
        <div className="py-16 text-center">
          <h1 className="text-3xl font-bold">Category not found</h1>
          <p className="mt-4 text-gray-500">The category you are looking for does not exist.</p>
        </div>
      </Container>
    );
  }

  // Get products using the category's public_id
  const products = await getProductsByCategory(category.public_id);

  return (
    <Section>
      <Container>
        <SectionHeading
          title={category.name}
          subtitle={category.description || undefined}
        />
        <ProductGrid products={products} />
      </Container>
    </Section>
  );
}