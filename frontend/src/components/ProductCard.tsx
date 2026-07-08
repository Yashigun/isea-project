
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
        rounded-[24px]
        p-2
        transition-all
        duration-300
        hover:-translate-y-2
        hover:shadow-[0_25px_45px_rgba(220,38,38,0.18)]
        sm:rounded-[30px]
        sm:p-3
        lg:rounded-[36px]
        lg:p-4
      "
    >
      <ProductImage
        image={primaryImage}
        name={product.name}
        productPublicId={product.public_id}
        href={`/products/${product.slug}`}
      />

      <div className="mt-3 space-y-3 sm:mt-4 sm:space-y-4 lg:mt-5 lg:space-y-5">
        <Link href={`/products/${product.slug}`} className="block">
          <div>
            <h3 className="text-lg font-medium sm:text-xl lg:text-2xl">
              {product.name}
            </h3>
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

