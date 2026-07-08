interface ProductPriceProps {
  price: number;
  discountPrice?: number;
}

export default function ProductPrice({
  price,
  discountPrice,
}: ProductPriceProps) {
  const formattedPrice = new Intl.NumberFormat(
    "en-IN",
    {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }
  ).format(price);

  if (!discountPrice) {
    return (
      <p className="text-base font-semibold sm:text-lg">
        {formattedPrice}
      </p>
    );
  }

  const formattedDiscount =
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(discountPrice);

  return (
    <div className="flex items-center gap-2 sm:gap-3">

      <span className="text-base font-semibold sm:text-lg">
        {formattedDiscount}
      </span>

      <span className="text-sm text-gray-400 line-through sm:text-base">
        {formattedPrice}
      </span>

    </div>
  );
}
