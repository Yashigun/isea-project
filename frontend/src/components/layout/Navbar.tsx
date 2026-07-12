
"use client";

import Link from "next/link";
import Image from "next/image";
import {
<<<<<<< HEAD
=======
  Menu,
>>>>>>> feature
  Search,
  ShoppingBag,
  UserRound,
  X,
<<<<<<< HEAD
  Menu,
=======
>>>>>>> feature
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import {
  useCallback,
  useEffect,
  useState,
} from "react";
import { cartService } from "@/services/cart";
import { productService } from "@/services/product";
import { Product } from "@/types/product";

export default function Navbar() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  const [cartCount, setCartCount] = useState(0);
<<<<<<< HEAD
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Product[]>([]);
  const [searching, setSearching] = useState(false);
=======
>>>>>>> feature

  const [searchOpen, setSearchOpen] =
    useState(false);

  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);

  const [query, setQuery] = useState("");

  const [results, setResults] = useState<Product[]>(
    []
  );

  const [searching, setSearching] =
    useState(false);

  // --------------------------------------------------
  // Cart Count
  // --------------------------------------------------

  const refreshCartCount = useCallback(async () => {
    if (!isAuthenticated) {
      setCartCount(0);
      return;
    }

    try {
      const cart = await cartService.get();

      setCartCount(cart.total_items);
    } catch (error) {
      console.error(
        "Failed to refresh cart count:",
        error
      );

      setCartCount(0);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    void refreshCartCount();
  }, [refreshCartCount]);

  useEffect(() => {
    const onCartUpdated = (event: Event) => {
      const customEvent = event as CustomEvent<{
        totalItems?: number;
      }>;

      const totalItems =
        customEvent.detail?.totalItems;

      if (typeof totalItems === "number") {
        setCartCount(totalItems);
        return;
      }

      void refreshCartCount();
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
  }, [refreshCartCount]);

  // Refresh when returning to the tab/window.
  useEffect(() => {
    const handleFocus = () => {
      void refreshCartCount();
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        void refreshCartCount();
      }
    };

    window.addEventListener("focus", handleFocus);

    document.addEventListener(
      "visibilitychange",
      handleVisibilityChange
    );

    return () => {
      window.removeEventListener(
        "focus",
        handleFocus
      );

      document.removeEventListener(
        "visibilitychange",
        handleVisibilityChange
      );
    };
  }, [refreshCartCount]);

  // --------------------------------------------------
  // Product Search
  // --------------------------------------------------

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

        setResults([]);
      } finally {
        setSearching(false);
      }
    }, 250);

    return () => {
      window.clearTimeout(timer);
    };
  }, [query, searchOpen]);

  // --------------------------------------------------
  // Navigation
  // --------------------------------------------------

  const handleProfileClick = () => {
    setMobileMenuOpen(false);

    if (isAuthenticated) {
      if (user?.is_admin) {
        router.push("/admin");
      } else {
        router.push("/profile");
      }

      return;
    }

    sessionStorage.setItem(
      "returnUrl",
      window.location.pathname
    );

    router.push("/auth/signup");
  };

  const handleCartClick = () => {
    setMobileMenuOpen(false);

    if (isAuthenticated) {
      router.push("/cart");
      return;
    }

    sessionStorage.setItem(
      "returnUrl",
      window.location.pathname
    );

    router.push("/auth/signup");
  };

  const closeSearch = () => {
    setSearchOpen(false);
    setQuery("");
    setResults([]);
  };

  return (
    <>
      <header className="sticky top-0 z-50 bg-[#fffaf6]/70 backdrop-blur-md">
        <div className="relative mx-auto flex h-20 w-full items-center justify-between px-4 sm:h-24 sm:px-6 lg:h-32 lg:px-16 xl:px-24">
          {/* --------------------------------
              Mobile Menu Button
          -------------------------------- */}

<<<<<<< HEAD
        <div className="relative flex h-24 items-center justify-between px-4 sm:h-28 sm:px-8 lg:h-32 lg:px-16 xl:px-24">

          {/* Left Navigation */}

          <nav className="hidden items-center gap-10 lg:flex">
=======
          <button
            type="button"
            aria-label="Open navigation menu"
            aria-expanded={mobileMenuOpen}
            onClick={() =>
              setMobileMenuOpen((current) => !current)
            }
            className="inline-flex h-10 w-10 items-center justify-center rounded-full transition-colors duration-300 hover:bg-black/5 hover:text-[#ac142a] lg:hidden"
          >
            {mobileMenuOpen ? (
              <X size={22} />
            ) : (
              <Menu size={22} />
            )}
          </button>

          {/* --------------------------------
              Desktop Left Navigation
          -------------------------------- */}
>>>>>>> feature

          <nav className="hidden items-center gap-10 lg:flex">
            <Link
              href="/"
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

          {/* --------------------------------
              Logo
          -------------------------------- */}

<<<<<<< HEAD
          <div className="absolute left-4 sm:left-8 lg:left-1/2 lg:-translate-x-1/2">

=======
          <div className="absolute left-1/2 -translate-x-1/2">
>>>>>>> feature
            <Link
              href="/"
              aria-label="Vimsy Home"
            >
              <Image
                src="/logo.svg"
                alt="Vimsy"
                width={230}
                height={126}
                priority
<<<<<<< HEAD
                className="h-auto w-[150px] sm:w-[180px] lg:w-[230px]"
                style={{ height: "auto" }}
=======
                className="h-auto w-[125px] sm:w-[160px] lg:w-[230px]"
>>>>>>> feature
              />
            </Link>
          </div>

          {/* --------------------------------
              Right Icons
          -------------------------------- */}

<<<<<<< HEAD
          {/* Right Icons */}

          <div className="hidden items-center gap-7 lg:flex">

=======
          <div className="ml-auto flex items-center gap-2 sm:gap-4 lg:gap-7">
>>>>>>> feature
            <button
              type="button"
              aria-label="Search"
              className="inline-flex h-10 w-10 items-center justify-center rounded-full transition-colors duration-300 ease-in-out hover:bg-black/5 hover:text-[#ac142a]"
              onClick={() => setSearchOpen(true)}
            >
              <Search size={21} />
            </button>

            <button
              type="button"
              aria-label="Account"
              className="hidden h-10 w-10 items-center justify-center rounded-full transition-colors duration-300 ease-in-out hover:bg-black/5 hover:text-[#ac142a] sm:inline-flex"
              onClick={handleProfileClick}
            >
              <UserRound size={21} />
            </button>

            <button
              type="button"
              aria-label={`Cart with ${cartCount} items`}
              className="relative inline-flex h-10 w-10 items-center justify-center rounded-full transition-colors duration-300 ease-in-out hover:bg-black/5 hover:text-[#ac142a]"
              onClick={handleCartClick}
            >
              <ShoppingBag size={21} />

              {cartCount > 0 && (
                <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-black px-1 text-[10px] font-medium leading-none text-white">
                  {cartCount > 99 ? "99+" : cartCount}
                </span>
              )}
            </button>
          </div>
<<<<<<< HEAD


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
              className="p-2 transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
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
                className="border-b border-black/10 py-4 text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
=======
        </div>

        {/* --------------------------------
            Mobile Navigation
        -------------------------------- */}

        {mobileMenuOpen && (
          <div className="border-t border-black/5 bg-[#fffaf6]/95 px-4 py-4 backdrop-blur-md lg:hidden">
            <nav className="mx-auto flex max-w-xl flex-col">
              <Link
                href="/"
                onClick={() =>
                  setMobileMenuOpen(false)
                }
                className="rounded-lg px-3 py-3 text-base font-medium transition-colors hover:bg-black/5 hover:text-[#ac142a]"
>>>>>>> feature
              >
                Shop
              </Link>

              <Link
                href="/about"
<<<<<<< HEAD
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
=======
                onClick={() =>
                  setMobileMenuOpen(false)
                }
                className="rounded-lg px-3 py-3 text-base font-medium transition-colors hover:bg-black/5 hover:text-[#ac142a]"
>>>>>>> feature
              >
                About
              </Link>

              <Link
                href="/contact"
<<<<<<< HEAD
                onClick={() => setMobileMenuOpen(false)}
                className="border-b border-black/10 py-4 text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
=======
                onClick={() =>
                  setMobileMenuOpen(false)
                }
                className="rounded-lg px-3 py-3 text-base font-medium transition-colors hover:bg-black/5 hover:text-[#ac142a]"
>>>>>>> feature
              >
                Contact
              </Link>

<<<<<<< HEAD

              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  setSearchOpen(true);
                }}
                className="flex items-center gap-3 border-b border-black/10 py-4 text-left text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
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
                className="flex items-center gap-3 border-b border-black/10 py-4 text-left text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
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
                className="flex items-center justify-between py-4 text-left text-lg font-medium transition hover:text-[#ac142a] transition-colors duration-300 ease-in-out"
              >

                <span className="flex items-center gap-3">

                  <ShoppingBag size={21} />

                  Cart

                </span>


                <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-black px-1 text-[10px] text-white">
                  {cartCount}
                </span>

              </button>

            </nav>

          </div>

        )}

=======
              <button
                type="button"
                onClick={handleProfileClick}
                className="rounded-lg px-3 py-3 text-left text-base font-medium transition-colors hover:bg-black/5 hover:text-[#ac142a] sm:hidden"
              >
                Account
              </button>
            </nav>
          </div>
        )}
>>>>>>> feature
      </header>

      {/* --------------------------------
          Search Overlay
      -------------------------------- */}

      {searchOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-start justify-center overflow-y-auto bg-white/20 px-4 pb-6 pt-24 backdrop-blur-md sm:items-center sm:py-8"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeSearch();
            }
          }}
        >
          <div className="w-full max-w-xl rounded-[28px] border border-white/40 bg-white/90 px-4 py-3 shadow-2xl sm:rounded-[32px] sm:px-6">
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
                className="h-11 min-w-0 flex-1 border-0 bg-transparent text-base outline-none sm:text-lg"
              />

              <button
                type="button"
                aria-label="Close search"
                onClick={closeSearch}
                className="shrink-0 rounded-full p-2 transition-colors duration-300 hover:bg-gray-100"
              >
                <X size={19} />
              </button>
            </div>

            {(searching ||
              query.trim().length >= 2 ||
              results.length > 0) && (
              <div className="mt-3 max-h-[50vh] overflow-y-auto border-t border-gray-100 pt-2">
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

                {!searching &&
                  results.map((product) => (
                    <Link
                      key={product.public_id}
                      href={`/products/${product.slug}`}
                      onClick={closeSearch}
                      className="flex items-center justify-between gap-4 rounded-xl px-3 py-3 transition-colors duration-200 hover:bg-gray-50"
                    >
                      <span className="min-w-0 truncate">
                        {product.name}
                      </span>

                      <span className="shrink-0 text-sm font-medium">
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

