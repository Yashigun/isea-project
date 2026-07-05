"use client";

import { Cart } from "@/services/cart";
import { Product } from "@/services/product";
import Link from "next/link";
import Image from "next/image";
import { Heart, PackageCheck, ReceiptText, X } from "lucide-react";
import { wishlistService } from "@/services/wishlist";
import { useState } from "react";

interface DashboardTabProps {
  cart: Cart | null;
  wishlist: Product[];
  onRefresh: () => void;
}

export default function DashboardTab({
  wishlist,
  onRefresh,
}: DashboardTabProps) {
  const [removing, setRemoving] = useState<string | null>(null);
  const getImage = (image: string | null | undefined) => {
    if (!image) return "/placeholder.jpg";
    if (image.startsWith("//")) return `https:${image}`;
    return image.replace("http://res.cloudinary.com", "https://res.cloudinary.com");
  };

  const handleRemoveFromWishlist = async (productPublicId: string) => {
    setRemoving(productPublicId);
    try {
      await wishlistService.remove(productPublicId);
      onRefresh();
    } catch (error) {
      console.error("Failed to remove from wishlist:", error);
    } finally {
      setRemoving(null);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl border bg-white p-5">
          <div className="flex items-center gap-2">
            <PackageCheck size={22} />
            <h2 className="text-xl font-semibold">Past Orders</h2>
          </div>
          <p className="mt-5 rounded-lg bg-gray-50 p-5 text-center text-gray-500">
            No past orders yet.
          </p>
        </div>
        <div className="rounded-xl border bg-white p-5">
          <div className="flex items-center gap-2">
            <ReceiptText size={22} />
            <h2 className="text-xl font-semibold">Invoices</h2>
          </div>
          <p className="mt-5 rounded-lg bg-gray-50 p-5 text-center text-gray-500">
            No invoices yet.
          </p>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <Heart className="text-red-500" size={24} />
          Wishlist
          <span className="text-sm font-normal text-gray-500 ml-2">
            ({wishlist.length} items)
          </span>
        </h2>
        {wishlist.length === 0 ? (
          <p className="text-gray-500 py-8 text-center bg-gray-50 rounded-xl">
            Your wishlist is empty. Start adding items you love!
          </p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {wishlist.map((product) => (
              <div
                key={product.public_id}
                className="bg-white rounded-xl shadow-sm border p-4 flex items-start gap-4"
              >
                <Link href={`/products/${product.slug}`} className="flex-shrink-0">
                  <Image
                    src={getImage(product.primary_image)}
                    alt={product.name}
                    width={80}
                    height={80}
                    className="rounded-lg object-cover w-20 h-20"
                  />
                </Link>
                <div className="flex-1 min-w-0">
                  <Link href={`/products/${product.slug}`}>
                    <h3 className="font-medium truncate">{product.name}</h3>
                  </Link>
                  <p className="text-sm font-semibold">₹{product.price}</p>
                </div>
                <button
                  onClick={() => handleRemoveFromWishlist(product.public_id)}
                  disabled={removing === product.public_id}
                  className="text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
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
