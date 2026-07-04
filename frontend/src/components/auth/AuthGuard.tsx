"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

interface AuthGuardProps {
  children: React.ReactNode;
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      // Save the current path to redirect after login
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return <div>Loading...</div>; // or a spinner
  }

  if (!isAuthenticated) {
    return null; // or a fallback while redirecting
  }

  return <>{children}</>;
}