import { Product } from "@/types/product";
import AddToCartButton from "./common/AddToCartButton";
import ProductPrice from "./common/ProductPrice";
import ProductImage from "./ProductImage";
import Link from "next/link";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const primaryImage =
    product.primary_image ||
    product.images?.find((image) => image.is_primary)?.url ||
    product.images?.[0]?.url ||
    null;

  return (
    <article
      className="
        group
        rounded-[36px]
        p-4
        transition-all
        duration-300
        hover:-translate-y-2
        hover:shadow-[0_25px_45px_rgba(220,38,38,0.18)]
      "
    >
      <ProductImage
        image={primaryImage}
        name={product.name}
        productPublicId={product.public_id}
        href={`/products/${product.slug}`}
      />

      <div className="mt-5 space-y-5">
        <Link href={`/products/${product.slug}`} className="block">
          <div>
            <h3 className="text-2xl font-medium">{product.name}</h3>
            <ProductPrice
              price={product.price}
              discountPrice={product.discount_price ?? undefined}
            />
          </div>
        </Link>

        <AddToCartButton productPublicId={product.public_id} />
      </div>
    </article>
  );
}
