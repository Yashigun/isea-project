"use client";

import Link from "next/link";
import Image from "next/image";
import { Search, ShoppingBag, UserRound } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();

  const handleProfileClick = () => {
    if (isAuthenticated) {
      // If admin, go to admin, else profile
      if (user?.is_admin) {
        router.push("/admin");
      } else {
        router.push("/profile");
      }
    } else {
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
    }
  };

  const handleCartClick = () => {
    if (isAuthenticated) {
      router.push("/cart");
    } else {
      sessionStorage.setItem("returnUrl", window.location.pathname);
      router.push("/auth/signup");
    }
  };

  const handleWishlistClick = () => {
    // If we have a wishlist page, similar logic
  };

  return (
    <header className="sticky top-0 z-50">
      <div className="relative flex h-32 items-center justify-between px-8 lg:px-16 xl:px-24">
        {/* Left Navigation */}
        <nav className="flex items-center gap-10">
          <Link href="/" className="text-sm font-medium transition hover:opacity-70">
            Shop
          </Link>
          <Link href="/blog" className="text-sm font-medium transition hover:opacity-70">
            Blog
          </Link>
          <Link href="/contact" className="text-sm font-medium transition hover:opacity-70">
            Contact
          </Link>
        </nav>

        {/* Logo */}
        <div className="absolute left-1/2 -translate-x-1/2">
          <Link href="/" aria-label="Vimsy Home">
            <Image
              src="/logo.svg"
              alt="Vimsy"
              width={200}
              height={110}
              priority
              className="h-auto w-[190px] lg:w-[230px]"
            />
          </Link>
        </div>

        {/* Right Icons */}
        <div className="flex items-center gap-7">
          <button aria-label="Search" className="transition hover:opacity-70">
            <Search size={22} />
          </button>

          <button
            aria-label="Account"
            className="transition hover:opacity-70"
            onClick={handleProfileClick}
          >
            <UserRound size={22} />
          </button>

          <button
            aria-label="Cart"
            className="relative transition hover:opacity-70"
            onClick={handleCartClick}
          >
            <ShoppingBag size={22} />
            <span className="absolute -right-2 -top-2 flex h-5 w-5 items-center justify-center rounded-full bg-black text-[10px] text-white">
              0
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}