"use client";

import { useState } from "react";
import { Product } from "@/services/product";
import { Category } from "@/services/category";
import { productService } from "@/services/product";

interface ProductFormProps {
  categories: Category[];
  initialData?: Product | null;
  onSubmit: (data: any) => Promise<any>;
}

export default function ProductForm({
  categories,
  initialData,
  onSubmit,
}: ProductFormProps) {
  const [categoryPublicId, setCategoryPublicId] = useState(
    initialData?.category?.public_id || ""
  );

  const [name, setName] = useState(initialData?.name || "");
  const [slug, setSlug] = useState(initialData?.slug || "");
  const [price, setPrice] = useState(initialData?.price || 0);

  const [discountPrice, setDiscountPrice] = useState<string>(
    initialData?.discount_price?.toString() ?? ""
  );

  const [shortDescription, setShortDescription] = useState(
    initialData?.short_description || ""
  );

  const [description, setDescription] = useState(
    initialData?.description || ""
  );

  const [isActive, setIsActive] = useState(
    initialData?.is_active ?? true
  );

  const [imageFiles, setImageFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setError(null);
    setLoading(true);

    try {
      // Validate required fields

      if (!categoryPublicId) {
        throw new Error("Please select a category.");
      }

      if (!name.trim()) {
        throw new Error("Product name is required.");
      }

      if (!slug.trim()) {
        // Auto-generate slug from name

        setSlug(
          name
            .trim()
            .toLowerCase()
            .replace(/\s+/g, "-")
        );
      }

      if (price <= 0) {
        throw new Error("Price must be greater than 0.");
      }


      // Build only the fields allowed by the backend schema.

      const productData: any = {
        category_public_id: categoryPublicId,

        name: name.trim(),

        slug:
          slug.trim() ||
          name
            .trim()
            .toLowerCase()
            .replace(/\s+/g, "-"),

        price: Number(price),

        is_active: isActive,
      };


      // Optional fields – only include if they have meaningful values

      if (
        shortDescription &&
        shortDescription.trim() !== ""
      ) {
        productData.short_description =
          shortDescription.trim();
      }


      if (
        description &&
        description.trim() !== ""
      ) {
        productData.description =
          description.trim();
      }


      if (
        discountPrice &&
        discountPrice.trim() !== ""
      ) {
        const discount = Number(discountPrice);

        if (discount > 0) {
          productData.discount_price = discount;
        }
      }


      // Debug: show exactly what is being sent to FastAPI

      console.log(
        "PRODUCT REQUEST DATA:",
        JSON.stringify(productData, null, 2)
      );


      // Create / Update product

      const product = await onSubmit(productData);


      // Upload selected images after product creation/update

      if (
        imageFiles.length > 0 &&
        product?.public_id
      ) {
        await Promise.all(
          imageFiles.map((file) => {
            const formData = new FormData();

            formData.append("file", file);

            return productService.uploadImage(
              formData,
              product.public_id
            );
          })
        );
      }


      // Reset form only after creating a new product

      if (!initialData) {
        setName("");
        setSlug("");
        setPrice(0);
        setDiscountPrice("");
        setShortDescription("");
        setDescription("");
        setCategoryPublicId("");
        setImageFiles([]);
        setIsActive(true);
      }

    } catch (err: any) {

      // Print complete Axios/FastAPI error information

      console.error("PRODUCT SUBMISSION ERROR:", err);

      console.error(
        "HTTP STATUS:",
        err.response?.status
      );

      console.error(
        "FULL BACKEND ERROR:",
        JSON.stringify(
          err.response?.data,
          null,
          2
        )
      );


      if (err.response) {
        const detail =
          err.response.data?.detail;


        // FastAPI validation errors

        if (Array.isArray(detail)) {
          const messages = detail.map(
            (d: any) => {
              const location = Array.isArray(d.loc)
                ? d.loc.join(".")
                : "unknown";

              const message =
                d.msg || "Validation error";

              const input =
                d.input !== undefined
                  ? ` | Input: ${JSON.stringify(d.input)}`
                  : "";

              return `${location}: ${message}${input}`;
            }
          );

          setError(messages.join("\n"));

        } else if (
          typeof detail === "string"
        ) {
          setError(detail);

        } else if (detail) {
          setError(
            JSON.stringify(
              detail,
              null,
              2
            )
          );

        } else {
          setError(
            `Request failed with status ${
              err.response.status
            }`
          );
        }

      } else if (err.request) {

        setError(
          "Network error: Could not reach the backend."
        );

      } else {

        setError(
          err.message ||
          "An unexpected error occurred."
        );

      }

    } finally {

      setLoading(false);

    }
  };


  return (

    <form
      onSubmit={handleSubmit}
      className="space-y-4 max-h-[70vh] overflow-y-auto"
    >

      <h2 className="text-xl font-semibold">
        {initialData
          ? "Edit Product"
          : "New Product"}
      </h2>


      {/* Error */}

      {error && (

        <div
          className="
            bg-red-50
            border
            border-red-200
            text-red-700
            p-3
            rounded-lg
            whitespace-pre-wrap
            text-sm
          "
        >
          {error}
        </div>

      )}


      {/* Category */}

      <div>

        <label className="block text-sm font-medium">
          Category *
        </label>

        <select
          value={categoryPublicId}
          onChange={(e) =>
            setCategoryPublicId(e.target.value)
          }
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        >

          <option value="">
            Select category
          </option>

          {categories.map((cat) => (

            <option
              key={cat.public_id}
              value={cat.public_id}
            >
              {cat.name}
            </option>

          ))}

        </select>

      </div>


      {/* Name */}

      <div>

        <label className="block text-sm font-medium">
          Name *
        </label>

        <input
          value={name}
          onChange={(e) => {
            const newName =
              e.target.value;

            setName(newName);

            // Auto-generate slug if not manually edited

            if (
              !slug ||
              slug ===
                name
                  .trim()
                  .toLowerCase()
                  .replace(/\s+/g, "-")
            ) {
              setSlug(
                newName
                  .trim()
                  .toLowerCase()
                  .replace(/\s+/g, "-")
              );
            }
          }}
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />

      </div>


      {/* Slug */}

      <div>

        <label className="block text-sm font-medium">
          Slug
        </label>

        <input
          value={slug}
          onChange={(e) =>
            setSlug(e.target.value)
          }
          className="w-full border rounded-lg px-3 py-2 mt-1"
          placeholder="Auto-generated from name"
        />

        <p className="text-xs text-gray-500 mt-1">
          Leave empty to auto-generate
        </p>

      </div>


      {/* Price */}

      <div>

        <label className="block text-sm font-medium">
          Price *
        </label>

        <input
          type="number"
          step="0.01"
          min="0.01"
          value={price}
          onChange={(e) =>
            setPrice(
              parseFloat(e.target.value) || 0
            )
          }
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />

        <p className="text-xs text-gray-500 mt-1">
          Must be greater than 0
        </p>

      </div>


      {/* Discount Price */}

      <div>

        <label className="block text-sm font-medium">
          Discount Price
        </label>

        <input
          type="number"
          step="0.01"
          min="0"
          value={discountPrice}
          onChange={(e) =>
            setDiscountPrice(e.target.value)
          }
          className="w-full border rounded-lg px-3 py-2 mt-1"
          placeholder="Leave empty for no discount"
        />

        <p className="text-xs text-gray-500 mt-1">
          Must be greater than 0 or leave empty
        </p>

      </div>


      {/* Short Description */}

      <div>

        <label className="block text-sm font-medium">
          Short Description
        </label>

        <textarea
          value={shortDescription}
          onChange={(e) =>
            setShortDescription(e.target.value)
          }
          className="w-full border rounded-lg px-3 py-2 mt-1"
          rows={2}
        />

      </div>


      {/* Description */}

      <div>

        <label className="block text-sm font-medium">
          Description
        </label>

        <textarea
          value={description}
          onChange={(e) =>
            setDescription(e.target.value)
          }
          className="w-full border rounded-lg px-3 py-2 mt-1"
          rows={4}
        />

      </div>


      {/* Images */}

      <div>

        <label className="block text-sm font-medium">
          Product Images
        </label>

        <input
          type="file"
          accept="image/*"
          multiple
          onChange={(e) =>
            setImageFiles(
              Array.from(
                e.target.files ?? []
              )
            )
          }
          className="mt-1"
        />

        <p className="text-xs text-gray-500 mt-1">
          Max size: 10MB each. Formats: JPEG, PNG, WEBP, GIF
        </p>

      </div>


      {/* Active */}

      <div className="flex items-center gap-2">

        <input
          type="checkbox"
          checked={isActive}
          onChange={(e) =>
            setIsActive(e.target.checked)
          }
          id="active"
        />

        <label
          htmlFor="active"
          className="text-sm"
        >
          Active
        </label>

      </div>


      {/* Submit */}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-black text-white py-2 rounded-lg disabled:opacity-50"
      >
        {loading
          ? "Saving..."
          : initialData
            ? "Update"
            : "Create"}
      </button>

    </form>

  );
}
