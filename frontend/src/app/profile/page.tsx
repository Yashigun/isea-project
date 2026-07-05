"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { orderService, Order } from "@/services/order";

export default function ProfilePage() {
  const { user, loading, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);

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
      orderService.list().then(setOrders).catch(console.error);
    }
  }, [loading, isAuthenticated, user, router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;
  if (user.is_admin) return null;

  return (
    <div className="container mx-auto max-w-6xl py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <button
          onClick={logout}
          className="mt-4 bg-black text-white px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>
      {/* Orders list, etc. */}
    </div>
  );
}