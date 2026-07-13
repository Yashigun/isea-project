"use client";

import {
  useEffect,
  useState,
} from "react";

import { X } from "lucide-react";


interface ReviewImageLightboxProps {
  src: string;
  alt: string;
  thumbnailClassName?: string;
}


export default function ReviewImageLightbox({
  src,
  alt,
  thumbnailClassName = "",
}: ReviewImageLightboxProps) {
  const [isOpen, setIsOpen] = useState(false);


  useEffect(() => {
    if (!isOpen) {
      return;
    }


    const handleKeyDown = (
      event: KeyboardEvent,
    ) => {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    };


    const previousOverflow =
      document.body.style.overflow;


    document.body.style.overflow =
      "hidden";


    window.addEventListener(
      "keydown",
      handleKeyDown,
    );


    return () => {
      document.body.style.overflow =
        previousOverflow;

      window.removeEventListener(
        "keydown",
        handleKeyDown,
      );
    };
  }, [isOpen]);


  return (
    <>
      {/* THUMBNAIL */}
        <button
        type="button"
        onClick={() => setIsOpen(true)}
        aria-label={`View ${alt}`}
        className="group block h-full w-full overflow-hidden"
        >
        <img
            src={src}
            alt={alt}
            loading="lazy"
            decoding="async"
            className={`block h-full w-full object-cover transition-transform duration-300 ease-out group-hover:scale-105 ${thumbnailClassName}`}
        />
        </button>


      {/* LIGHTBOX */}

      {isOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Review image preview"
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 p-4 backdrop-blur-md sm:p-6"
        >

          {/* CLOSE BUTTON */}

          <button
            type="button"
            onClick={() => setIsOpen(false)}
            aria-label="Close image preview"
            className="absolute right-4 top-4 z-10 rounded-full bg-black/40 p-2 text-white transition hover:bg-black/60 sm:right-6 sm:top-6"
          >
            <X size={24} />
          </button>


          {/* IMAGE CONTAINER */}

          <div
            onClick={(event) =>
              event.stopPropagation()
            }
            className="flex max-h-[80vh] max-w-[90vw] items-center justify-center overflow-hidden rounded-xl bg-white/5 shadow-2xl sm:max-w-3xl"
          >
            <img
              src={src}
              alt={alt}
              className="max-h-[80vh] max-w-full object-contain"
            />
          </div>

        </div>
      )}
    </>
  );
}