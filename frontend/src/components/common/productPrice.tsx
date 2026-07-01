interface ProductPriceProps {
  price: number;
}

export default function ProductPrice({
  price,
}: ProductPriceProps) {
  return (
    <p className="text-xl font-semibold">
      ₹{price.toLocaleString("en-IN")}
    </p>
  );
}