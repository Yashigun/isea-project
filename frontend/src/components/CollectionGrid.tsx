"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import {
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import { Category } from "@/types/category";

import CollectionCard from "./CollectionCard";

interface CollectionGridProps {
  categories: Category[];
}

export default function CollectionGrid({
  categories,
}: CollectionGridProps) {
  const sliderRef =
    useRef<HTMLDivElement | null>(null);

  const [canScrollLeft, setCanScrollLeft] =
    useState(false);

  const [canScrollRight, setCanScrollRight] =
    useState(false);

  const updateScrollButtons =
    useCallback(() => {
      const slider = sliderRef.current;

      if (!slider) {
        return;
      }

      const maximumScrollLeft =
        slider.scrollWidth -
        slider.clientWidth;

      setCanScrollLeft(
        slider.scrollLeft > 2,
      );

      setCanScrollRight(
        slider.scrollLeft <
          maximumScrollLeft - 2,
      );
    }, []);

  useEffect(() => {
    const slider = sliderRef.current;

    if (!slider) {
      return;
    }

    updateScrollButtons();

    slider.addEventListener(
      "scroll",
      updateScrollButtons,
      {
        passive: true,
      },
    );

    window.addEventListener(
      "resize",
      updateScrollButtons,
    );

    const resizeObserver =
      new ResizeObserver(
        updateScrollButtons,
      );

    resizeObserver.observe(slider);

    return () => {
      slider.removeEventListener(
        "scroll",
        updateScrollButtons,
      );

      window.removeEventListener(
        "resize",
        updateScrollButtons,
      );

      resizeObserver.disconnect();
    };
  }, [
    categories.length,
    updateScrollButtons,
  ]);

  const scrollSlider = (
    direction: "left" | "right",
  ) => {
    const slider = sliderRef.current;

    if (!slider) {
      return;
    }

    /*
      Mobile:
      approximately 2 cards.

      Desktop:
      scroll roughly one visible group.
    */

    const scrollDistance =
      slider.clientWidth * 0.8;

    slider.scrollBy({
      left:
        direction === "left"
          ? -scrollDistance
          : scrollDistance,
      behavior: "smooth",
    });
  };

  if (categories.length === 0) {
    return null;
  }

  return (
    <div className="relative">
      {/* LEFT ARROW */}

      {canScrollLeft && (
        <button
          type="button"
          onClick={() =>
            scrollSlider("left")
          }
          aria-label="Previous collections"
          className="
            absolute
            left-1
            top-[42%]
            z-20
            flex
            h-9
            w-9
            -translate-y-1/2
            items-center
            justify-center
            rounded-full
            border
            border-black/10
            bg-white/85
            shadow-md
            backdrop-blur-sm
            transition
            hover:scale-105
            hover:bg-white
            sm:-left-4
            sm:h-10
            sm:w-10
          "
        >
          <ChevronLeft
            size={20}
            aria-hidden="true"
          />
        </button>
      )}

      {/* COLLECTION SLIDER */}

      <div
        ref={sliderRef}
        className="
          flex
          snap-x
          snap-mandatory
          gap-3
          overflow-x-auto
          scroll-smooth
          pb-12
          pt-2
          pl-4

          [scrollbar-width:none]
          [&::-webkit-scrollbar]:hidden

          sm:gap-5
          lg:gap-6
        "
      >
        {categories.map((category) => (
          <div
            key={category.public_id}
            className="
              w-[calc((100%-0.75rem)/2)]
              shrink-0
              snap-start

              sm:w-[calc((100%-2.5rem)/3)]

              lg:w-[calc((100%-4.5rem)/4)]
            "
          >
            <CollectionCard
              category={category}
            />
          </div>
        ))}
      </div>

      {/* RIGHT ARROW */}

      {canScrollRight && (
        <button
          type="button"
          onClick={() =>
            scrollSlider("right")
          }
          aria-label="Next collections"
          className="
            absolute
            right-1
            top-[42%]
            z-20
            flex
            h-9
            w-9
            -translate-y-1/2
            items-center
            justify-center
            rounded-full
            border
            border-black/10
            bg-white/85
            shadow-md
            backdrop-blur-sm
            transition
            hover:scale-105
            hover:bg-white
            sm:-right-4
            sm:h-10
            sm:w-10
          "
        >
          <ChevronRight
            size={20}
            aria-hidden="true"
          />
        </button>
      )}
    </div>
  );
}