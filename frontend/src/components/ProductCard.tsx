import Link from "next/link";

import { Product } from "@/types/product";

import AddToCartButton from "./common/AddToCartButton";
import ProductPrice from "./common/ProductPrice";
import ProductImage from "./ProductImage";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({
  product,
}: ProductCardProps) {
  const primaryImage =
    product.primary_image ||
    product.images?.find(
      (image) => image.is_primary,
    )?.url ||
    product.images?.[0]?.url ||
    null;

  return (
    <article
      className="
        group
        min-w-0
        rounded-[20px]
        p-1.5
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-[0_20px_35px_rgba(220,38,38,0.15)]
        sm:rounded-[24px]
        sm:p-2
        lg:rounded-[28px]
        lg:p-3
      "
    >
      <ProductImage
        image={primaryImage}
        name={product.name}
        productPublicId={product.public_id}
        href={`/products/${product.slug}`}
      />

      <div
        className="
          mt-2
          space-y-2
          sm:mt-3
          sm:space-y-3
          lg:mt-4
          lg:space-y-4
        "
      >
        <Link
          href={`/products/${product.slug}`}
          className="block min-w-0"
        >
          <div className="min-w-0">
            <h3 className="truncate text-base font-medium sm:text-lg lg:text-xl">
              {product.name}
            </h3>

            <ProductPrice
              price={product.price}
              discountPrice={
                product.discount_price ??
                undefined
              }
            />
          </div>
        </Link>

        <AddToCartButton
          productPublicId={product.public_id}
        />
      </div>
    </article>
  );
}

