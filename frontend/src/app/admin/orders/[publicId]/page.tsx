"use client";

import {
  useEffect,
  useState,
} from "react";

import Image from "next/image";
import Link from "next/link";
import { useParams } from "next/navigation";

import {
  ArrowLeft,
  CalendarDays,
  Clock3,
  CreditCard,
  Mail,
  MapPin,
  Package,
  Phone,
  ReceiptText,
  UserRound,
} from "lucide-react";

import {Order, orderService} from "@/services/order";

const getImage = (
  image: string | null | undefined
) => {
  if (!image) {
    return "/placeholder.jpg";
  }

  if (image.startsWith("//")) {
    return "https:" + image;
  }

  return image.replace(
    "http://res.cloudinary.com",
    "https://res.cloudinary.com"
  );
};




const getStatusClasses = (status: string) => {
  switch (status) {
    case "delivered":
      return "bg-green-100 text-green-700";

    case "cancelled":
    case "refunded":
      return "bg-red-100 text-red-700";

    case "processing":
    case "shipped":
      return "bg-blue-100 text-blue-700";

    case "confirmed":
      return "bg-purple-100 text-purple-700";

    default:
      return "bg-yellow-100 text-yellow-700";
  }
};

const formatPaymentMethod = (
  method: string | undefined
) => {
  if (!method) {
    return "Not available";
  }

  return method
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
};

export default function AdminOrderDetailsPage() {
  const params = useParams();

  const publicId = params.publicId as string;

  const [order, setOrder] =
    useState<Order | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    const loadOrder = async () => {
      setLoading(true);
      setError("");

      try {
        const result =
          await orderService.getAdmin(publicId);

        setOrder(result);
      } catch (error) {
        console.error(
          "Failed to load admin order:",
          error
        );

        setError(
          "Could not load this order."
        );
      } finally {
        setLoading(false);
      }
    };

    if (publicId) {
      void loadOrder();
    }
  }, [publicId]);

  if (loading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <p className="text-sm text-gray-500">
          Loading order details...
        </p>
      </div>
    );
  }

  if (error || !order) {
    return (
      <div className="mx-auto max-w-6xl">
        <div className="rounded-xl border bg-white p-8 text-center">
          <p className="text-sm text-red-600">
            {error || "Order not found."}
          </p>

          <Link
            href="/admin/orders"
            className="mt-5 inline-flex items-center gap-2 text-sm font-medium hover:underline"
          >
            <ArrowLeft size={16} />

            Back to Orders
          </Link>
        </div>
      </div>
    );
  }

  const createdAt = new Date(order.created_at);

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <Link
            href="/admin/orders"
            className="inline-flex items-center gap-2 text-sm text-gray-500 transition hover:text-black"
          >
            <ArrowLeft size={17} />

            Back to Orders
          </Link>

          <h1 className="mt-4 text-2xl font-bold sm:text-3xl">
            Order Details
          </h1>

          <p className="mt-1 break-all text-sm text-gray-500">
            {order.public_id}
          </p>
        </div>

        <span
          className={`w-fit rounded-full px-3 py-1.5 text-sm font-medium capitalize ${getStatusClasses(
            order.status
          )}`}
        >
          {order.status}
        </span>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          icon={<CalendarDays size={20} />}
          label="Order Date"
          value={createdAt.toLocaleDateString()}
        />

        <SummaryCard
          icon={<Clock3 size={20} />}
          label="Order Time"
          value={createdAt.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        />

        <SummaryCard
          icon={<CreditCard size={20} />}
          label="Payment Method"
          value={formatPaymentMethod(
            order.payment?.payment_method
          )}
        />

        <SummaryCard
          icon={<ReceiptText size={20} />}
          label="Total Payment"
          value={`₹${order.total_amount}`}
        />
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border bg-white p-5 shadow-sm sm:p-6">
          <div className="flex items-center gap-2">
            <UserRound size={21} />

            <h2 className="text-lg font-semibold">
              Customer Information
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            <InfoRow
              icon={<UserRound size={17} />}
              label="Customer Name"
              value={`${order.customer.first_name} ${
                order.customer.last_name ?? ""
              }`.trim()}
            />

            <InfoRow
              icon={<Mail size={17} />}
              label="Email Address"
              value={order.customer.email}
            />

            <InfoRow
              icon={<Phone size={17} />}
              label="Phone Number"
              value={
                order.shipping_phone ||
                "Not available"
              }
            />
          </div>
        </div>

        <div className="rounded-xl border bg-white p-5 shadow-sm sm:p-6">
          <div className="flex items-center gap-2">
            <MapPin size={21} />

            <h2 className="text-lg font-semibold">
              Shipping Address
            </h2>
          </div>

          <div className="mt-5 rounded-lg bg-gray-50 p-4 text-sm leading-7 text-gray-700">
            <p className="font-medium text-black">
              {order.shipping_name}
            </p>

            <p>{order.address_line_1}</p>

            {order.address_line_2 && (
              <p>{order.address_line_2}</p>
            )}

            <p>
              {order.city}, {order.state}
            </p>

            <p>
              {order.country} - {order.postal_code}
            </p>

            <p className="mt-2">
              {order.shipping_phone}
            </p>
          </div>
        </div>
      </section>

      <section className="rounded-xl border bg-white p-5 shadow-sm sm:p-6">
        <div className="flex items-center gap-2">
          <Package size={22} />

          <h2 className="text-xl font-semibold">
            Products
          </h2>
        </div>

        {!order.items ||
        order.items.length === 0 ? (
          <div className="mt-5 rounded-lg bg-gray-50 p-8 text-center">
            <p className="text-sm text-gray-500">
              No products found.
            </p>
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            {order.items.map((item) => (
              <div
                key={item.public_id}
                className="flex flex-col gap-4 rounded-xl border p-4 sm:flex-row sm:items-center"
              >
                {item.product ? (
                  <Link
                    href={`/products/${item.product.slug}`}
                    className="flex-shrink-0"
                  >
                    <Image
                      src={getImage(
                        item.product.primary_image
                      )}
                      alt={item.product_name}
                      width={88}
                      height={88}
                      className="h-[88px] w-[88px] rounded-lg object-cover"
                    />
                  </Link>
                ) : (
                  <Image
                    src="/placeholder.jpg"
                    alt={item.product_name}
                    width={88}
                    height={88}
                    className="h-[88px] w-[88px] rounded-lg object-cover"
                  />
                )}

                <div className="min-w-0 flex-1">
                  <h3 className="font-semibold">
                    {item.product_name}
                  </h3>

                  <div className="mt-2 flex flex-wrap gap-x-6 gap-y-1 text-sm text-gray-500">
                    <span>
                      Unit Price: ₹{item.unit_price}
                    </span>

                    <span>
                      Quantity: {item.quantity}
                    </span>
                  </div>
                </div>

                <div className="sm:text-right">
                  <p className="text-xs text-gray-500">
                    Subtotal
                  </p>

                  <p className="mt-1 font-semibold">
                    ₹{item.subtotal}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_380px]">
        <div className="rounded-xl border bg-white p-5 shadow-sm sm:p-6">
          <h2 className="text-lg font-semibold">
            Order Information
          </h2>

          <div className="mt-5 space-y-4">
            <InfoRow
              label="Order ID"
              value={order.public_id}
            />

            <InfoRow
              label="Payment Status"
              value={
                order.payment?.payment_status
                  ? order.payment.payment_status
                      .replaceAll("_", " ")
                  : "Not available"
              }
            />

            <InfoRow
              label="Payment Method"
              value={formatPaymentMethod(
                order.payment?.payment_method
              )}
            />

            <InfoRow
              label="Order Status"
              value={order.status}
            />

            {order.order_notes && (
              <InfoRow
                label="Order Notes"
                value={order.order_notes}
              />
            )}
          </div>
        </div>

        <div className="rounded-xl border bg-white p-5 shadow-sm sm:p-6">
          <h2 className="text-lg font-semibold">
            Payment Summary
          </h2>

          <div className="mt-5 space-y-3">
            <PaymentRow
              label="Subtotal"
              value={`₹${order.subtotal}`}
            />

            <PaymentRow
              label="Discount"
              value={`₹${order.discount}`}
            />

            <PaymentRow
              label="Shipping"
              value={`₹${order.shipping_cost}`}
            />

            <PaymentRow
              label="Tax"
              value={`₹${order.tax}`}
            />

            <div className="border-t pt-4">
              <PaymentRow
                label="Total Payment"
                value={`₹${order.total_amount}`}
                strong
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function SummaryCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="rounded-lg bg-gray-100 p-2.5 text-gray-700">
          {icon}
        </div>

        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
            {label}
          </p>

          <p className="mt-1 break-words font-semibold">
            {value}
          </p>
        </div>
      </div>
    </div>
  );
}

function InfoRow({
  icon,
  label,
  value,
}: {
  icon?: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-start gap-3">
      {icon && (
        <div className="mt-0.5 text-gray-400">
          {icon}
        </div>
      )}

      <div className="min-w-0">
        <p className="text-xs text-gray-500">
          {label}
        </p>

        <p className="mt-0.5 break-words text-sm font-medium capitalize">
          {value}
        </p>
      </div>
    </div>
  );
}

function PaymentRow({
  label,
  value,
  strong = false,
}: {
  label: string;
  value: string;
  strong?: boolean;
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <span
        className={
          strong
            ? "text-base font-semibold"
            : "text-sm text-gray-600"
        }
      >
        {label}
      </span>

      <span
        className={
          strong
            ? "text-lg font-bold"
            : "text-sm font-medium"
        }
      >
        {value}
      </span>
    </div>
  );
}
