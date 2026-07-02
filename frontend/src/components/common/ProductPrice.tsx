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
      <p className="text-lg font-semibold">
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
    <div className="flex items-center gap-3">

      <span className="text-lg font-semibold">
        {formattedDiscount}
      </span>

      <span className="text-gray-400 line-through">
        {formattedPrice}
      </span>

    </div>
  );
}