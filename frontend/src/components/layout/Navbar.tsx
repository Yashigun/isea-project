"use client";

import Link from "next/link";
import Image from "next/image";
import { Search, ShoppingBag, UserRound, X } from "lucide-react";
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

      if (typeof customEvent.detail?.totalItems === "number") {
        setCartCount(customEvent.detail.totalItems);
      } else if (isAuthenticated) {
        cartService
          .get()
          .then((cart) => setCartCount(cart.total_items));
      }
    };

    window.addEventListener("cart:updated", onCartUpdated);

    return () =>
      window.removeEventListener("cart:updated", onCartUpdated);
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
      // If admin, go to admin, else profile
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
      <header className="sticky top-0 z-50 bg-[#fffaf6/70] backdrop-blur-md">

        <div className="relative flex h-32 items-center justify-between px-8 lg:px-16 xl:px-24">

          {/* Left Navigation */}

          <nav className="flex items-center gap-10">

            <Link
              href="/"
              className="text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
            >
              Shop
            </Link>

            <Link
              href="/about"
              className="text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
            >
              About
            </Link>

            <Link
              href="/contact"
              className="text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
            >
              Contact
            </Link>

          </nav>


          {/* Logo */}

          <div className="absolute left-1/2 -translate-x-1/2">

            <Link
              href="/"
              aria-label="Vimsy Home"
            >

              <Image
                src="/logo.svg"
                alt="Vimsy"
                width={200}
                height={110}
                priority
                className="h-auto w-[190px] lg:w-[230px]"
                style={{ height: "auto" }}
              />

            </Link>

          </div>


          {/* Right Icons */}

          <div className="flex items-center gap-7">

            <button
              aria-label="Search"
              className="transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
              onClick={() => setSearchOpen(true)}
            >
              <Search size={22} />
            </button>


            <button
              aria-label="Account"
              className="transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
              onClick={handleProfileClick}
            >
              <UserRound size={22} />
            </button>


            <button
              aria-label="Cart"
              className="relative transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
              onClick={handleCartClick}
            >

              <ShoppingBag size={22} />

              <span className="absolute -right-2 -top-2 flex h-5 w-5 items-center justify-center rounded-full bg-black text-[10px] text-white">
                {cartCount}
              </span>

            </button>

          </div>

        </div>

      </header>


      {/* Search Overlay */}

      {searchOpen && (

        <div
          className="
            fixed
            inset-0
            z-[100]
            flex
            items-center
            justify-center
            bg-white/20
            px-4
            backdrop-blur-md
          "
        >

          {/* Search Container */}

          <div
            className="
              w-full
              max-w-xl
              rounded-full
              border
              border-white/40
              bg-white/90
              px-6
              py-3
              shadow-2xl
              transition-all
              duration-300
              animate-in
              fade-in
              zoom-in-95
            "
          >

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
                className="
                  h-11
                  flex-1
                  border-0
                  bg-transparent
                  text-lg
                  outline-none
                "
              />


              <button
                type="button"
                aria-label="Close search"
                onClick={() => {
                  setSearchOpen(false);
                  setQuery("");
                }}
                className="
                  shrink-0
                  rounded-full
                  p-2
                  transition-colors
                  duration-300
                  hover:bg-gray-100
                "
              >

                <X size={19} />

              </button>

            </div>


            {/* Search Results */}

            {(searching ||
              query.trim().length >= 2 ||
              results.length > 0) && (

              <div
                className="
                  mt-3
                  max-h-[40vh]
                  overflow-y-auto
                  border-t
                  border-gray-100
                  pt-2
                "
              >

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
                    onClick={() =>
                      setSearchOpen(false)
                    }
                    className="
                      flex
                      items-center
                      justify-between
                      rounded-xl
                      px-3
                      py-3
                      transition-colors
                      duration-200
                      hover:bg-gray-50
                    "
                  >

                    <span>
                      {product.name}
                    </span>

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