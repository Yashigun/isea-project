"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import AdminSidebar from "@/components/admin/AdminSidebar";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  

  useEffect(() => {
    // Wait until loading is complete
    if (loading) return;

    // If not authenticated, redirect to signup
    if (!isAuthenticated) {
      // Save the return URL for after login
      sessionStorage.setItem("returnUrl", pathname);
      router.push("/auth/signup");
      return;
    }

    // If authenticated but not admin, redirect to home
    if (!user?.is_admin) {
      router.push("/");
      return;
    }
    // If admin, we stay on the page
  }, [loading, isAuthenticated, user, router, pathname]);

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }

  // If not admin, render nothing (will redirect)
  if (!user?.is_admin) {
    return null;
  }
  

  return (
    <div className="flex min-h-screen bg-gray-50">
      <AdminSidebar />
      <main className="flex-1 p-6 lg:p-10 overflow-y-auto max-h-screen">
        {children}
      </main>
    </div>
  );
}