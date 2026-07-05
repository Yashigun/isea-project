import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";

import ProductLayout from "@/components/product/ProductLayout";
import ProductGallery from "@/components/product/ProductGallery";
import ProductInfo from "@/components/product/ProductInfo";
import RelatedProducts from "@/components/product/RelatedProducts";
import ProductReviews from "@/components/product/ProductReviews";

import { productService } from "@/services/product";

interface ProductPageProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function ProductPage({
  params,
}: ProductPageProps) {
  const { slug } = await params;

  const product = await productService.getBySlug(slug);

  if (!product) {
    return (
      <Container>
        <p>Product not found.</p>
      </Container>
    );
  }

  const relatedProducts = await productService.getRelated(
    product.public_id
  );

  return (
    <>
      <Section>
        <Container>
          <ProductLayout
            gallery={
              <ProductGallery
                images={product.images}
                name={product.name}
                primaryImage={product.primary_image}
              />
            }
            info={
              <ProductInfo
                publicId={product.public_id}
                name={product.name}
                price={product.price}
                discountPrice={product.discount_price}
                shortDescription={product.short_description}
                description={product.description}
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

      <Section>
        <Container>
          <ProductReviews productPublicId={product.public_id} />
        </Container>
      </Section>
    </>
  );
}
