"use client";

import { Cart } from "@/services/cart";
import { Product } from "@/services/product";
import Link from "next/link";
import Image from "next/image";
import { Heart, ShoppingBag, X } from "lucide-react";
import { cartService } from "@/services/cart";
import { wishlistService } from "@/services/wishlist";
import { useState } from "react";

interface DashboardTabProps {
  cart: Cart | null;
  wishlist: Product[];
  onRefresh: () => void;
}

export default function DashboardTab({
  cart,
  wishlist,
  onRefresh,
}: DashboardTabProps) {
  const [removing, setRemoving] = useState<string | null>(null);

  const handleRemoveFromCart = async (productPublicId: string) => {
    setRemoving(productPublicId);
    try {
      await cartService.removeItem(productPublicId);
      onRefresh();
    } catch (error) {
      console.error("Failed to remove from cart:", error);
    } finally {
      setRemoving(null);
    }
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

      {/* Wishlist Section */}
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
                    src={product.primary_image || "/placeholder.jpg"}
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

      {/* Cart Section */}
      <section>
        <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          <ShoppingBag size={24} />
          Cart
          <span className="text-sm font-normal text-gray-500 ml-2">
            ({cart?.total_items || 0} items)
          </span>
        </h2>
        {!cart || cart.items.length === 0 ? (
          <p className="text-gray-500 py-8 text-center bg-gray-50 rounded-xl">
            Your cart is empty. Start shopping!
          </p>
        ) : (
          <div className="space-y-3">
            {cart.items.map((item) => (
              <div
                key={item.product.public_id}
                className="bg-white rounded-xl shadow-sm border p-4 flex items-center gap-4"
              >
                <Link href={`/products/${item.product.slug}`} className="flex-shrink-0">
                  <Image
                    src={item.product.primary_image || "/placeholder.jpg"}
                    alt={item.product.name}
                    width={80}
                    height={80}
                    className="rounded-lg object-cover w-20 h-20"
                  />
                </Link>
                <div className="flex-1 min-w-0">
                  <Link href={`/products/${item.product.slug}`}>
                    <h3 className="font-medium truncate">{item.product.name}</h3>
                  </Link>
                  <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
                  <p className="text-sm font-semibold">₹{item.subtotal}</p>
                </div>
                <button
                  onClick={() => handleRemoveFromCart(item.product.public_id)}
                  disabled={removing === item.product.public_id}
                  className="text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
                >
                  <X size={18} />
                </button>
              </div>
            ))}
            <div className="bg-gray-50 rounded-xl p-4 flex justify-between items-center">
              <span className="font-semibold">Total:</span>
              <span className="text-xl font-bold">₹{cart.total_amount}</span>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}