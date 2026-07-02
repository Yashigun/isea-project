import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";

import ProductLayout from "@/components/product/ProductLayout";
import ProductGallery from "@/components/product/ProductGallery";
import ProductInfo from "@/components/product/ProductInfo";
import RelatedProducts from "@/components/product/RelatedProducts";

import {
    getProductBySlug,
    getProductsByCategory,
} from "@/services/product";
import { products } from "@/data/products";

interface ProductPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function ProductPage({
  params,
}: ProductPageProps) {
  const { slug } = await params;

  const product =
    await getProductBySlug(slug);
    if(!product) {
    return (
      <Container>
        <p>Product not found.</p>
      </Container>
    );
  }

  const relatedProducts =
    (
        await getProductsByCategory(
            product.category.slug
        )
    )
    .filter(
        item=>item.id!==product.id
    )
    .slice(0,4);

  return (
    <>
      <Section>

        <Container>

          <ProductLayout
            gallery={
              <ProductGallery
                images={product.images}
                name={product.name}
              />
            }
            info={
              <ProductInfo
                id={product.id}
                name={product.name}
                price={product.price}
                discountPrice={product.discountPrice}
                shortDescription={product.shortDescription}
              />
            }
          />

        </Container>

      </Section>

      {relatedProducts.length > 0 && (
        <Section>

          <Container>

            <RelatedProducts
              products={relatedProducts}
            />

          </Container>

        </Section>
      )}
    </>
  );
}