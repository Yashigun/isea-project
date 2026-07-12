"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Image from "next/image";

import {
  ArrowLeft,
  CreditCard,
  PackageCheck,
  ReceiptText,
} from "lucide-react";

import AuthGuard from "@/components/auth/AuthGuard";
import {
  Order,
  orderService,
} from "@/services/order";

export default function OrderDetailsPage() {
  const params = useParams();

  const publicId = params.publicId as string;

  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const getImage = (
    image: string | null | undefined
  ) => {
    if (!image) return "/placeholder.jpg";

    if (image.startsWith("//")) {
      return `https:${image}`;
    }

    return image.replace(
      "http://res.cloudinary.com",
      "https://res.cloudinary.com"
    );
  };

  useEffect(() => {
    const loadOrder = async () => {
      setLoading(true);
      setError("");

      try {
        const result = await orderService.get(publicId);
        setOrder(result);
      } catch (error) {
        console.error(
          "Failed to load order:",
          error
        );

        setError("Could not load this order.");
      } finally {
        setLoading(false);
      }
    };

    if (publicId) {
      loadOrder();
    }
  }, [publicId]);

  if (loading) {
    return (
      <AuthGuard>
        <div className="container mx-auto max-w-5xl px-4 py-20">
          <p className="text-center text-gray-500">
            Loading order...
          </p>
        </div>
      </AuthGuard>
    );
  }

  if (error || !order) {
    return (
      <AuthGuard>
        <div className="container mx-auto max-w-5xl px-4 py-20">
          <div className="rounded-xl border bg-white p-8 text-center">
            <p className="text-red-600">
              {error || "Order not found."}
            </p>

            <Link
              href="/profile"
              className="mt-5 inline-flex items-center gap-2 text-sm font-medium hover:underline"
            >
              <ArrowLeft size={16} />
              Back to Profile
            </Link>
          </div>
        </div>
      </AuthGuard>
    );
  }

  return (
    <AuthGuard>
      <div className="container mx-auto max-w-5xl px-4 py-10">

        <Link
          href="/profile"
          className="mb-6 inline-flex items-center gap-2 text-sm text-gray-600 transition hover:text-black"
        >
          <ArrowLeft size={18} />
          Back to Profile
        </Link>

        <div className="space-y-6">

          {/* --------------------------------
              Order Header
          -------------------------------- */}

          <section className="rounded-xl border bg-white p-6">
            <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

              <div>
                <div className="flex items-center gap-2">
                  <PackageCheck size={24} />

                  <h1 className="text-2xl font-bold">
                    Order Details
                  </h1>
                </div>

                <p className="mt-3 text-sm text-gray-500">
                  Order ID
                </p>

                <p className="font-medium">
                  {order.public_id}
                </p>
              </div>

              <div className="sm:text-right">
                <p className="text-sm text-gray-500">
                  Status
                </p>

                <p className="mt-1 capitalize font-semibold">
                  {order.status}
                </p>
              </div>

            </div>
          </section>

          {/* --------------------------------
              Ordered Products
          -------------------------------- */}

          <section className="rounded-xl border bg-white p-6">
            <h2 className="text-xl font-semibold">
              Products
            </h2>

            {!order.items || order.items.length === 0 ? (
              <p className="mt-5 rounded-lg bg-gray-50 p-5 text-center text-gray-500">
                No products found for this order.
              </p>
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
                          width={96}
                          height={96}
                          className="h-24 w-24 rounded-lg object-cover"
                        />
                      </Link>
                    ) : (
                      <Image
                        src="/placeholder.jpg"
                        alt={item.product_name}
                        width={96}
                        height={96}
                        className="h-24 w-24 rounded-lg object-cover"
                      />
                    )}

                    <div className="min-w-0 flex-1">

                      {item.product ? (
                        <Link
                          href={`/products/${item.product.slug}`}
                        >
                          <h3 className="font-semibold hover:underline">
                            {item.product_name}
                          </h3>
                        </Link>
                      ) : (
                        <h3 className="font-semibold">
                          {item.product_name}
                        </h3>
                      )}

                      <p className="mt-1 text-sm text-gray-500">
                        Unit Price: ₹{item.unit_price}
                      </p>

                      <p className="mt-1 text-sm text-gray-500">
                        Quantity: {item.quantity}
                      </p>
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

          {/* --------------------------------
              Payment
          -------------------------------- */}

          <section className="rounded-xl border bg-white p-6">
            <div className="flex items-center gap-2">
              <CreditCard size={22} />

              <h2 className="text-xl font-semibold">
                Payment
              </h2>
            </div>

            <div className="mt-5 flex items-center justify-between rounded-lg bg-gray-50 p-4">
              <span className="text-gray-600">
                Mode of Payment
              </span>

              <span className="font-medium capitalize">
                {order.payment?.payment_method
                  ? order.payment.payment_method.replaceAll("_", " ")
                  : "Not available"}
              </span>
            </div>
          </section>

          {/* --------------------------------
              Order Summary
          -------------------------------- */}

          <section className="rounded-xl border bg-white p-6">
            <div className="flex items-center gap-2">
              <ReceiptText size={22} />

              <h2 className="text-xl font-semibold">
                Order Summary
              </h2>
            </div>

            <div className="mt-5 space-y-3">

              <div className="flex justify-between gap-4">
                <span className="text-gray-600">
                  Subtotal
                </span>

                <span>
                  ₹{order.subtotal}
                </span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-gray-600">
                  Discount
                </span>

                <span>
                  ₹{order.discount}
                </span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-gray-600">
                  Shipping
                </span>

                <span>
                  ₹{order.shipping_cost}
                </span>
              </div>

              <div className="flex justify-between gap-4">
                <span className="text-gray-600">
                  Tax
                </span>

                <span>
                  ₹{order.tax}
                </span>
              </div>

              <div className="border-t pt-4">
                <div className="flex items-center justify-between gap-4">
                  <span className="text-lg font-semibold">
                    Total Amount
                  </span>

                  <span className="text-xl font-bold">
                    ₹{order.total_amount}
                  </span>
                </div>
              </div>

            </div>
          </section>

        </div>
      </div>
    </AuthGuard>
  );
}
