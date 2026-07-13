"use client";

import Link from "next/link";
import Image from "next/image";
import {
  Search,
  ShoppingBag,
  UserRound,
  X,
  Menu,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { cartService } from "@/services/cart";
import { productService } from "@/services/product";
import { Product } from "@/types/product";

export default function Navbar() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  const [cartCount, setCartCount] = useState(0);
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Product[]>([]);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      queueMicrotask(() => setCartCount(0));
      return;
    }

    cartService
      .get()
      .then((cart) => setCartCount(cart.total_items))
      .catch(() => setCartCount(0));
  }, [isAuthenticated]);

  useEffect(() => {
    const onCartUpdated = (event: Event) => {
      const customEvent = event as CustomEvent<{
        totalItems?: number;
      }>;

      if (
        typeof customEvent.detail?.totalItems === "number"
      ) {
        setCartCount(customEvent.detail.totalItems);
      } else if (isAuthenticated) {
        cartService
          .get()
          .then((cart) =>
            setCartCount(cart.total_items)
          )
          .catch(() => setCartCount(0));
      }
    };

    window.addEventListener(
      "cart:updated",
      onCartUpdated
    );

    return () => {
      window.removeEventListener(
        "cart:updated",
        onCartUpdated
      );
    };
  }, [isAuthenticated]);

  useEffect(() => {
    if (!searchOpen || query.trim().length < 2) {
      queueMicrotask(() => setResults([]));
      return;
    }

    const timer = window.setTimeout(async () => {
      setSearching(true);

      try {
        setResults(
          await productService.getAll({
            search: query.trim(),
          })
        );
      } catch (error) {
        console.error("Search failed:", error);
      } finally {
        setSearching(false);
      }
    }, 250);

    return () => window.clearTimeout(timer);
  }, [query, searchOpen]);

  const handleProfileClick = () => {
    if (isAuthenticated) {
      if (user?.is_admin) {
        router.push("/admin");
      } else {
        router.push("/profile");
      }
    } else {
      sessionStorage.setItem(
        "returnUrl",
        window.location.pathname
      );

      router.push("/auth/signup");
    }
  };

  const handleCartClick = () => {
    if (isAuthenticated) {
      router.push("/cart");
    } else {
      sessionStorage.setItem(
        "returnUrl",
        window.location.pathname
      );

      router.push("/auth/signup");
    }
  };

  return (
    <>
      <header className="sticky top-0 z-50 bg-[#fffaf6]/70 backdrop-blur-md">
        <div className="relative flex h-24 items-center justify-between px-4 sm:h-28 sm:px-8 lg:h-32 lg:px-16 xl:px-24">
          {/* Left Navigation */}

          <nav className="hidden items-center gap-10 lg:flex">
            <Link
              href="/"
              className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
            >
              Home
            </Link>
            <Link
              href="/products"
              className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
            >
              Shop
            </Link>

            <Link
              href="/about"
              className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
            >
              About
            </Link>

            <Link
              href="/contact"
              className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
            >
              Contact
            </Link>
          </nav>

          {/* Logo */}

          <div className="absolute left-4 sm:left-8 lg:left-1/2 lg:-translate-x-1/2">
            <Link href="/" aria-label="Vimsy Home">
              <Image
                src="/logo.svg"
                alt="Vimsy"
                width={200}
                height={110}
                priority
                className="h-auto w-[150px] sm:w-[180px] lg:w-[230px]"
              />
            </Link>
          </div>

          {/* Right Icons */}

          <div className="hidden items-center gap-7 lg:flex">
            <button
              type="button"
              aria-label="Search"
              className="transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              onClick={() => setSearchOpen(true)}
            >
              <Search size={22} />
            </button>

            <button
              type="button"
              aria-label="Account"
              className="transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              onClick={handleProfileClick}
            >
              <UserRound size={22} />
            </button>

            <button
              type="button"
              aria-label={`Cart with ${cartCount} items`}
              className="relative flex h-9 w-9 items-center justify-center transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              onClick={handleCartClick}
            >
              <ShoppingBag size={22} />

              {cartCount > 0 && (
                <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-black px-1 text-[10px] font-medium leading-none text-white">
                  {cartCount > 99 ? "99+" : cartCount}
                </span>
              )}
            </button>
          </div>

          {/* Mobile / Tablet Hamburger */}

          <div className="ml-auto flex items-center lg:hidden">
            <button
              type="button"
              aria-label={
                mobileMenuOpen
                  ? "Close navigation menu"
                  : "Open navigation menu"
              }
              aria-expanded={mobileMenuOpen}
              onClick={() =>
                setMobileMenuOpen((current) => !current)
              }
              className="p-2 transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
            >
              {mobileMenuOpen ? (
                <X size={26} />
              ) : (
                <Menu size={26} />
              )}
            </button>
          </div>
        </div>

        {/* Mobile / Tablet Navigation */}

        {mobileMenuOpen && (
          <div className="border-t border-black/10 px-4 pb-6 sm:px-8 lg:hidden">
            <nav className="flex flex-col">
              <Link
                href="/"
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                Home
              </Link>
              <Link
                href="/products"
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                Shop
              </Link>

              <Link
                href="/about"
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                About
              </Link>

              <Link
                href="/contact"
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                Contact
              </Link>

              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  setSearchOpen(true);
                }}
                className="flex items-center gap-3 border-b border-black/10 py-4 text-left text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                <Search size={21} />
                Search
              </button>

              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleProfileClick();
                }}
                className="flex items-center gap-3 border-b border-black/10 py-4 text-left text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                <UserRound size={21} />
                Account
              </button>

              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleCartClick();
                }}
                className="flex items-center justify-between py-4 text-left text-lg font-medium transition-colors duration-300 ease-in-out hover:text-[#ac142a]"
              >
                <span className="flex items-center gap-3">
                  <ShoppingBag size={21} />
                  Cart
                </span>

                {cartCount > 0 && (
                  <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-black px-1 text-[10px] font-medium leading-none text-white">
                    {cartCount > 99 ? "99+" : cartCount}
                  </span>
                )}
              </button>
            </nav>
          </div>
        )}
      </header>

      {/* Search Overlay */}

      {searchOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-white/20 px-4 backdrop-blur-md">
          {/* Search Container */}

          <div className="w-full max-w-xl animate-in rounded-full border border-white/40 bg-white/90 px-6 py-3 shadow-2xl transition-all duration-300 fade-in zoom-in-95">
            {/* Search Input */}

            <div className="flex items-center gap-3">
              <Search
                size={21}
                className="shrink-0 text-gray-500"
              />

              <input
                autoFocus
                value={query}
                onChange={(event) =>
                  setQuery(event.target.value)
                }
                placeholder="Search products"
                className="h-11 min-w-0 flex-1 border-0 bg-transparent text-lg outline-none"
              />

              <button
                type="button"
                aria-label="Close search"
                onClick={() => {
                  setSearchOpen(false);
                  setQuery("");
                }}
                className="shrink-0 rounded-full p-2 transition-colors duration-300 hover:bg-gray-100"
              >
                <X size={19} />
              </button>
            </div>

            {/* Search Results */}

            {(searching ||
              query.trim().length >= 2 ||
              results.length > 0) && (
              <div className="mt-3 max-h-[40vh] overflow-y-auto border-t border-gray-100 pt-2">
                {searching && (
                  <p className="px-2 py-4 text-sm text-gray-500">
                    Searching...
                  </p>
                )}

                {!searching &&
                  query.trim().length >= 2 &&
                  results.length === 0 && (
                    <p className="px-2 py-4 text-sm text-gray-500">
                      No products found.
                    </p>
                  )}

                {results.map((product) => (
                  <Link
                    key={product.public_id}
                    href={`/products/${product.slug}`}
                    onClick={() => {
                      setSearchOpen(false);
                      setQuery("");
                    }}
                    className="flex items-center justify-between rounded-xl px-3 py-3 transition-colors duration-200 hover:bg-gray-50"
                  >
                    <span>{product.name}</span>

                    <span className="text-sm font-medium">
                      ₹
                      {product.discount_price ??
                        product.price}
                    </span>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}