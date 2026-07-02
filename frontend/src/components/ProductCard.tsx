import { Product } from "@/types/product";

import AddToCartButton from "./common/AddToCartButton";
import ProductPrice from "./common/ProductPrice";
import ProductImage from "./ProductImage";
import Link from "next/dist/client/link";


interface ProductCardProps {
  product: Product;
}

export default function ProductCard({
  product,
}: ProductCardProps) {
  return (
    <Link href={`/products/${product.slug}`} className="block">
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
          image={product.images[0]}
          name={product.name}
        />

        <div className="mt-5 space-y-5">

          <div>

            <h3 className="text-2xl font-medium">
              {product.name}
            </h3>

            <ProductPrice
              price={product.price}
              discountPrice={product.discountPrice}
            />

          </div>

          <AddToCartButton />

        </div>
      </article>
    </Link>
  );
}