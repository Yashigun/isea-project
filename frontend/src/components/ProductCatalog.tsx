"use client";

import {
  useMemo,
  useState,
} from "react";

import ProductGrid from "@/components/ProductGrid";

import type { Product } from "@/services/product";
import type { Category } from "@/services/category";

interface ProductCatalogProps {
  products: Product[];
  categories: Category[];
}

type SortOption =
  | "featured"
  | "price-low-high"
  | "price-high-low"
  | "name-a-z";

function getProductPrice(product: Product): number {
  return Number(product.price);
}

export default function ProductCatalog({
  products,
  categories,
}: ProductCatalogProps) {
  const maximumPrice = useMemo(() => {
    if (products.length === 0) {
      return 0;
    }

    return Math.ceil(
      Math.max(
        ...products.map((product) =>
          getProductPrice(product),
        ),
      ),
    );
  }, [products]);

  const [selectedCategory, setSelectedCategory] =
    useState<string>("all");

  const [maximumSelectedPrice, setMaximumSelectedPrice] =
    useState<number>(maximumPrice);

  const [sortBy, setSortBy] =
    useState<SortOption>("featured");

  const filteredProducts = useMemo(() => {
    const result = products.filter((product) => {
      const matchesCategory =
        selectedCategory === "all" ||
        product.category?.public_id === selectedCategory;

      const matchesPrice =
        getProductPrice(product) <= maximumSelectedPrice;

      return matchesCategory && matchesPrice;
    });

    return [...result].sort((firstProduct, secondProduct) => {
      switch (sortBy) {
        case "price-low-high":
          return (
            getProductPrice(firstProduct) -
            getProductPrice(secondProduct)
          );

        case "price-high-low":
          return (
            getProductPrice(secondProduct) -
            getProductPrice(firstProduct)
          );

        case "name-a-z":
          return firstProduct.name.localeCompare(
            secondProduct.name,
          );

        case "featured":
        default:
          return 0;
      }
    });
  }, [
    products,
    selectedCategory,
    maximumSelectedPrice,
    sortBy,
  ]);

  const clearFilters = () => {
    setSelectedCategory("all");
    setMaximumSelectedPrice(maximumPrice);
    setSortBy("featured");
  };

  return (
    <div>
      {/* TOP BAR */}

      <div className="mb-6 flex flex-wrap items-center justify-between gap-4 border-b pb-4">
        <p className="text-sm text-gray-500">
          {filteredProducts.length}{" "}
          {filteredProducts.length === 1
            ? "product"
            : "products"}
        </p>

        <label className="flex items-center gap-2 text-sm">
          <span>Sort by</span>

          <select
            value={sortBy}
            onChange={(event) =>
              setSortBy(event.target.value as SortOption)
            }
            className="rounded-lg border bg-white px-3 py-2"
          >
            <option value="featured">
              Featured
            </option>

            <option value="price-low-high">
              Price: Low to High
            </option>

            <option value="price-high-low">
              Price: High to Low
            </option>

            <option value="name-a-z">
              Name: A to Z
            </option>
          </select>
        </label>
      </div>

      {/* SIDEBAR + PRODUCTS */}

      <div className="grid items-start gap-8 lg:grid-cols-[240px_minmax(0,1fr)]">
        {/* FILTER SIDEBAR */}

        <aside className="rounded-xl border bg-white p-5">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-medium">
              Filters
            </h2>

            <button
              type="button"
              onClick={clearFilters}
              className="text-xs text-gray-500 underline underline-offset-4 hover:text-black"
            >
              Clear
            </button>
          </div>

          {/* CATEGORY FILTER */}

          <fieldset className="mt-6">
            <legend className="text-sm font-medium">
              Category
            </legend>

            <div className="mt-3 space-y-2">
              <label className="flex cursor-pointer items-center gap-2 text-sm">
                <input
                  type="radio"
                  name="product-category"
                  value="all"
                  checked={selectedCategory === "all"}
                  onChange={() => setSelectedCategory("all")}
                  className="accent-[#ac142a]"
                />

                <span>All categories</span>
              </label>

              {categories.map((category) => (
                <label
                  key={category.public_id}
                  className="flex cursor-pointer items-center gap-2 text-sm"
                >
                  <input
                    type="radio"
                    name="product-category"
                    value={category.public_id}
                    checked={selectedCategory === category.public_id}
                    onChange={() =>
                      setSelectedCategory(category.public_id)
                    }
                    className="accent-[#ac142a]"
                  />

                  <span>
                    {category.name}
                  </span>
                </label>
              ))}
            </div>
          </fieldset>

          {/* PRICE FILTER */}

          <div className="mt-7 border-t pt-6">
            <div className="flex items-center justify-between gap-3">
              <label
                htmlFor="maximum-product-price"
                className="text-sm font-medium"
              >
                Maximum price
              </label>

              <span className="text-sm text-gray-500">
                ₹{maximumSelectedPrice.toLocaleString("en-IN")}
              </span>
            </div>

            <input
              id="maximum-product-price"
              type="range"
              min={0}
              max={maximumPrice}
              step={1}
              value={maximumSelectedPrice}
              disabled={maximumPrice === 0}
              onChange={(event) =>
                setMaximumSelectedPrice(Number(event.target.value))
              }
              style={{
                background: `linear-gradient(
                  to right,
                  #ac142a 0%,
                  #ac142a ${
                    maximumPrice > 0
                      ? (maximumSelectedPrice / maximumPrice) * 100
                      : 0
                  }%,
                  #d1d5db ${
                    maximumPrice > 0
                      ? (maximumSelectedPrice / maximumPrice) * 100
                      : 0
                  }%,
                  #d1d5db 100%
                )`,
              }}
              className="
                mt-4
                h-1
                w-full
                cursor-pointer
                appearance-none
                rounded-full

                [&::-webkit-slider-runnable-track]:h-1
                [&::-webkit-slider-runnable-track]:rounded-full
                [&::-webkit-slider-runnable-track]:bg-transparent

                [&::-webkit-slider-thumb]:-mt-1.5
                [&::-webkit-slider-thumb]:h-4
                [&::-webkit-slider-thumb]:w-4
                [&::-webkit-slider-thumb]:appearance-none
                [&::-webkit-slider-thumb]:rounded-full
                [&::-webkit-slider-thumb]:bg-[#B10F1F]

                [&::-moz-range-track]:h-1
                [&::-moz-range-track]:rounded-full
                [&::-moz-range-track]:bg-transparent

                [&::-moz-range-thumb]:h-4
                [&::-moz-range-thumb]:w-4
                [&::-moz-range-thumb]:rounded-full
                [&::-moz-range-thumb]:border-0
                [&::-moz-range-thumb]:bg-[#B10F1F]

                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            />

            <div className="mt-2 flex justify-between text-xs text-[#ac142a]">
              <span>₹100</span>

              <span>
                ₹{maximumPrice.toLocaleString("en-IN")}
              </span>
            </div>
          </div>
        </aside>

        {/* PRODUCT RESULTS */}

        <main className="min-w-0">
          {filteredProducts.length === 0 ? (
            <div className="rounded-xl border border-dashed px-5 py-16 text-center">
              <p className="text-gray-500">
                No products match the selected filters.
              </p>

              <button
                type="button"
                onClick={clearFilters}
                className="mt-4 text-sm font-medium underline underline-offset-4"
              >
                Clear filters
              </button>
            </div>
          ) : (
            <ProductGrid products={filteredProducts} />
          )}
        </main>
      </div>
    </div>
  );
}