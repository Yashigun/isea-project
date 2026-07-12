
"use client";

import { Cart } from "@/services/cart";
import { Product } from "@/services/product";
import { Order } from "@/services/order";
import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  Heart,
  PackageCheck,
  ReceiptText,
  X,
} from "lucide-react";
import { wishlistService } from "@/services/wishlist";
import { useState } from "react";

interface DashboardTabProps {
  cart: Cart | null;
  wishlist: Product[];
  orders: Order[];
  onRefresh: () => void;
}

export default function DashboardTab({
  wishlist,
  orders,
  onRefresh,
}: DashboardTabProps) {
  const [removing, setRemoving] = useState<string | null>(null);

  const getImage = (image: string | null | undefined) => {
    if (!image) return "/placeholder.jpg";

    if (image.startsWith("//")) {
      return `https:${image}`;
    }

    return image.replace(
      "http://res.cloudinary.com",
      "https://res.cloudinary.com"
    );
  };

  const handleRemoveFromWishlist = async (
    productPublicId: string
  ) => {
    setRemoving(productPublicId);

    try {
      await wishlistService.remove(productPublicId);
      onRefresh();
    } catch (error) {
      console.error(
        "Failed to remove from wishlist:",
        error
      );
    } finally {
      setRemoving(null);
    }
  };

  return (
<<<<<<< HEAD
    <div className="space-y-6 sm:space-y-8">
      <h1 className="text-2xl font-bold sm:text-3xl">Dashboard</h1>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border bg-white p-4 sm:p-5">
          <div className="flex items-center gap-2">
            <PackageCheck size={22} />
            <h2 className="text-lg font-semibold sm:text-xl">Past Orders</h2>
          </div>
          <p className="mt-4 rounded-lg bg-gray-50 p-4 text-center text-gray-500 sm:mt-5 sm:p-5">
            No past orders yet.
          </p>
        </div>
        <div className="rounded-xl border bg-white p-4 sm:p-5">
          <div className="flex items-center gap-2">
            <ReceiptText size={22} />
            <h2 className="text-lg font-semibold sm:text-xl">Invoices</h2>
          </div>
          <p className="mt-4 rounded-lg bg-gray-50 p-4 text-center text-gray-500 sm:mt-5 sm:p-5">
            No invoices yet.
          </p>
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-4 flex flex-wrap items-center gap-2 sm:text-2xl">
          <Heart className="text-red-500" size={24} />
          Wishlist
          <span className="text-sm font-normal text-gray-500 ml-0 sm:ml-2">
=======
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">
        Dashboard
      </h1>

      <section className="grid gap-4 md:grid-cols-2">

        {/* --------------------------------
            Past Orders
        -------------------------------- */}

        <div className="rounded-xl border bg-white p-5">
          <div className="flex items-center gap-2">
            <PackageCheck size={22} />

            <h2 className="text-xl font-semibold">
              Past Orders
            </h2>
          </div>

          {orders.length === 0 ? (
            <p className="mt-5 rounded-lg bg-gray-50 p-5 text-center text-gray-500">
              No past orders yet.
            </p>
          ) : (
            <div className="mt-5 space-y-3">
              {orders.map((order) => (
                <Link
                  key={order.public_id}
                  href={`/orders/${order.public_id}`}
                  className="flex items-center justify-between gap-4 rounded-lg border p-4 transition hover:bg-gray-50"
                >
                  <div className="min-w-0">
                    <p className="text-xs text-gray-500">
                      Order ID
                    </p>

                    <p className="truncate font-medium">
                      {order.public_id}
                    </p>
                  </div>

                  <ArrowRight
                    size={20}
                    className="flex-shrink-0 text-gray-500"
                  />
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* --------------------------------
            Invoices
        -------------------------------- */}

        <div className="rounded-xl border bg-white p-5">
          <div className="flex items-center gap-2">
            <ReceiptText size={22} />

            <h2 className="text-xl font-semibold">
              Invoices
            </h2>
          </div>

          {orders.length === 0 ? (
            <p className="mt-5 rounded-lg bg-gray-50 p-5 text-center text-gray-500">
              No invoices yet.
            </p>
          ) : (
            <div className="mt-5 space-y-3">
              {orders.map((order) => (
                <div
                  key={order.public_id}
                  className="rounded-lg border p-4"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div className="min-w-0">
                      <p className="text-xs text-gray-500">
                        Order ID
                      </p>

                      <p className="truncate font-medium">
                        {order.public_id}
                      </p>
                    </div>

                    <div className="flex-shrink-0 text-right">
                      <p className="text-xs text-gray-500">
                        Total Amount
                      </p>

                      <p className="font-semibold">
                        ₹{order.total_amount}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* --------------------------------
          Wishlist
      -------------------------------- */}

      <section>
        <h2 className="mb-4 flex items-center gap-2 text-2xl font-semibold">
          <Heart
            className="text-red-500"
            size={24}
          />

          Wishlist

          <span className="ml-2 text-sm font-normal text-gray-500">
>>>>>>> feature
            ({wishlist.length} items)
          </span>
        </h2>

        {wishlist.length === 0 ? (
<<<<<<< HEAD
          <p className="text-gray-500 py-6 px-4 text-center bg-gray-50 rounded-xl sm:py-8">
=======
          <p className="rounded-xl bg-gray-50 py-8 text-center text-gray-500">
>>>>>>> feature
            Your wishlist is empty. Start adding items you love!
          </p>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {wishlist.map((product) => (
              <div
                key={product.public_id}
<<<<<<< HEAD
                className="bg-white rounded-xl shadow-sm border p-3 flex items-start gap-3 sm:p-4 sm:gap-4"
=======
                className="flex items-start gap-4 rounded-xl border bg-white p-4 shadow-sm"
>>>>>>> feature
              >
                <Link
                  href={`/products/${product.slug}`}
                  className="flex-shrink-0"
                >
                  <Image
                    src={getImage(
                      product.primary_image
                    )}
                    alt={product.name}
                    width={80}
                    height={80}
<<<<<<< HEAD
                    className="rounded-lg object-cover w-16 h-16 sm:w-20 sm:h-20"
=======
                    className="h-20 w-20 rounded-lg object-cover"
>>>>>>> feature
                  />
                </Link>

                <div className="min-w-0 flex-1">
                  <Link
                    href={`/products/${product.slug}`}
                  >
                    <h3 className="truncate font-medium">
                      {product.name}
                    </h3>
                  </Link>

                  <p className="text-sm font-semibold">
                    ₹{product.price}
                  </p>
                </div>

                <button
                  onClick={() =>
                    handleRemoveFromWishlist(
                      product.public_id
                    )
                  }
                  disabled={
                    removing === product.public_id
                  }
                  className="flex-shrink-0 text-gray-400 transition-colors hover:text-red-500"
                >
                  <X size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}