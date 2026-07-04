"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { orderService, Order } from "@/services/order";
import { categoryService, Category } from "@/services/category";
import { productService, Product } from "@/services/product";
import { wishlistService } from "@/services/wishlist"; // we'll create this
import { cartService } from "@/services/cart"; // we'll create this

export default function ProfilePage() {
  const { user, loading, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [wishlist, setWishlist] = useState<Product[]>([]);
  const [cartItems, setCartItems] = useState<any[]>([]);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push("/auth/signup");
      return;
    }
    if (!loading && user?.is_admin) {
      router.push("/admin");
      return;
    }
    if (user) {
      // Fetch user data
      orderService.list().then(setOrders).catch(console.error);
      // Wishlist and cart services need to be created
      // wishlistService.get().then(setWishlist);
      // cartService.get().then(setCartItems);
    }
  }, [loading, isAuthenticated, user, router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;
  if (user.is_admin) return null; // will redirect

  return (
    <div className="container mx-auto max-w-6xl py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Personal Info */}
        <div className="bg-white p-6 rounded-lg shadow col-span-2">
          <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
          <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <button
            onClick={logout}
            className="mt-4 bg-black text-white px-4 py-2 rounded-lg"
          >
            Logout
          </button>
        </div>

        {/* Wishlist */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Wishlist</h2>
          {wishlist.length === 0 ? (
            <p className="text-gray-500">No items in wishlist</p>
          ) : (
            <ul className="space-y-2">
              {wishlist.map((p) => (
                <li key={p.public_id}>{p.name}</li>
              ))}
            </ul>
          )}
        </div>

        {/* Cart */}
        <div className="bg-white p-6 rounded-lg shadow col-span-2">
          <h2 className="text-xl font-semibold mb-4">Cart</h2>
          {cartItems.length === 0 ? (
            <p className="text-gray-500">Cart is empty</p>
          ) : (
            <ul className="space-y-2">
              {cartItems.map((item) => (
                <li key={item.public_id}>{item.product.name} x {item.quantity}</li>
              ))}
            </ul>
          )}
        </div>

        {/* Orders */}
        <div className="bg-white p-6 rounded-lg shadow col-span-3">
          <h2 className="text-xl font-semibold mb-4">Order History</h2>
          {orders.length === 0 ? (
            <p className="text-gray-500">No orders yet</p>
          ) : (
            <table className="w-full text-sm">
              <thead className="border-b">
                <tr>
                  <th className="text-left py-2">Order ID</th>
                  <th className="text-left py-2">Total</th>
                  <th className="text-left py-2">Status</th>
                  <th className="text-left py-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.public_id} className="border-b">
                    <td className="py-2">{order.public_id.slice(0, 8)}</td>
                    <td className="py-2">₹{order.total_amount}</td>
                    <td className="py-2">{order.status}</td>
                    <td className="py-2">{new Date(order.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}