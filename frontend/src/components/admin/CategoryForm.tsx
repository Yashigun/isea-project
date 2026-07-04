"use client";

import { useState } from "react";
import { Category } from "@/services/category";

interface CategoryFormProps {
  initialData?: Category | null;
  onSubmit: (data: { name: string; slug: string; description?: string; is_active?: boolean }) => Promise<void>;
}

export default function CategoryForm({ initialData, onSubmit }: CategoryFormProps) {
  const [name, setName] = useState(initialData?.name || "");
  const [slug, setSlug] = useState(initialData?.slug || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [isActive, setIsActive] = useState(initialData?.is_active ?? true);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onSubmit({ name, slug, description: description || undefined, is_active: isActive });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-xl font-semibold">{initialData ? "Edit Category" : "New Category"}</h2>
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
        <label className="block text-sm font-medium">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 mt-1"
          rows={3}
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