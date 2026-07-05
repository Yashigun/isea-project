"use client";

import { useState } from "react";
import { Product } from "@/services/product";
import { Category } from "@/services/category";
import { productService } from "@/services/product";

interface ProductFormProps {
  categories: Category[];
  initialData?: Product | null;
  onSubmit: (data: any) => Promise<void>;
}

export default function ProductForm({ categories, initialData, onSubmit }: ProductFormProps) {
  const [categoryPublicId, setCategoryPublicId] = useState(initialData?.category?.public_id || "");
  const [name, setName] = useState(initialData?.name || "");
  const [slug, setSlug] = useState(initialData?.slug || "");
  const [price, setPrice] = useState(initialData?.price || 0);
  const [discountPrice, setDiscountPrice] = useState<string>(initialData?.discount_price?.toString() ?? "");
  const [shortDescription, setShortDescription] = useState(initialData?.short_description || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [isActive, setIsActive] = useState(initialData?.is_active ?? true);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      let imageUrl = null;
      if (imageFile) {
        const uploadRes = await productService.uploadImage(imageFile);
        imageUrl = uploadRes.url;
      }
      const data: any = {
        category_public_id: categoryPublicId,
        name,
        slug,
        price: Number(price),
        is_active: isActive,
      };
      if (discountPrice) data.discount_price = Number(discountPrice);
      if (shortDescription) data.short_description = shortDescription;
      if (description) data.description = description;
      // For now, we ignore imageUrl because we need to add image to product separately.
      // In a real implementation, you'd have a separate endpoint to add images to product.
      await onSubmit(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-h-[70vh] overflow-y-auto">
      <h2 className="text-xl font-semibold">{initialData ? "Edit Product" : "New Product"}</h2>
      <div>
        <label className="block text-sm font-medium">Category</label>
        <select
          value={categoryPublicId}
          onChange={(e) => setCategoryPublicId(e.target.value)}
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        >
          <option value="">Select category</option>
          {categories.map((cat) => (
            <option key={cat.public_id} value={cat.public_id}>
              {cat.name}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium">Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Slug</label>
        <input
          value={slug}
          onChange={(e) => setSlug(e.target.value)}
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Price</label>
        <input
          type="number"
          step="0.01"
          value={price}
          onChange={(e) => setPrice(parseFloat(e.target.value))}
          required
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Discount Price</label>
        <input
          type="number"
          step="0.01"
          value={discountPrice}
          onChange={(e) => setDiscountPrice(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mt-1"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Short Description</label>
        <textarea
          value={shortDescription}
          onChange={(e) => setShortDescription(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mt-1"
          rows={2}
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mt-1"
          rows={4}
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Product Image</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImageFile(e.target.files?.[0] || null)}
          className="mt-1"
        />
      </div>
      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={isActive}
          onChange={(e) => setIsActive(e.target.checked)}
          id="active"
        />
        <label htmlFor="active" className="text-sm">Active</label>
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-black text-white py-2 rounded-lg disabled:opacity-50"
      >
        {loading ? "Saving..." : initialData ? "Update" : "Create"}
      </button>
    </form>
  );
}