import Hero from "@/components/Hero";
import CollectionGrid from "@/components/CollectionGrid";
import ProductGrid from "@/components/ProductGrid";

import Container from "@/components/layout/Container";

import Section from "@/components/ui/Section";

import SectionHeading from "@/components/common/SectionHeading";

import { getCategories } from "@/services/category";
import { getProducts } from "@/services/product";

export default async function HomePage() {
  const categories = await getCategories();

  const products = await getProducts();

  return (
    <>
      <Hero />
      <Section>

        <Container>

          <SectionHeading
            title="Our Products"
            subtitle="Handcrafted pieces you'll love."
          />

          <ProductGrid
            products={products}
          />

        </Container>

      </Section>

      <Section>
        

        <Container>

          <SectionHeading
            title="Shop by Collection"
            subtitle="Browse our carefully curated collections."
          />

          <CollectionGrid
            categories={categories}
          />

        </Container>

      </Section>

      

    </>
  );
}