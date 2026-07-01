import Image from "next/image";

import { Product } from "@/types/product";

import WishlistButton from "./common/wishlistButton";
import ProductPrice from "./common/productPrice";
import AddToCartButton from "./common/addToCart";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({
  product,
}: ProductCardProps) {
  return (
    <article
      className="
        group
        overflow-hidden
        rounded-[32px]
        bg-white
        p-4
        transition-all
        duration-300
        hover:-translate-y-2
        hover:shadow-[0_22px_45px_rgba(220,38,38,0.18)]
      "
    >
      <div className="relative">

        <Image
          src={product.image}
          alt={product.name}
          width={600}
          height={600}
          className="
            aspect-square
            w-full
            rounded-[28px]
            object-cover
          "
        />

        <WishlistButton />

      </div>

      <div className="mt-5 space-y-4">

        <div>

          <h3 className="text-2xl font-medium">
            {product.name}
          </h3>

          <ProductPrice
            price={product.price}
          />

        </div>

        <AddToCartButton />

      </div>

    </article>
  );
}