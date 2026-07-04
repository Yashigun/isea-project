"use client";

import { useEffect, useState } from "react";
import { categoryService, Category } from "@/services/category";
import DataTable from "@/components/admin/DataTable";
import CategoryForm from "@/components/admin/CategoryForm";
import Modal from "@/components/admin/Modal";

export default function AdminCategories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const data = await categoryService.getAll(false);
      setCategories(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleDelete = async (publicId: string) => {
    if (!confirm("Delete this category?")) return;
    await categoryService.delete(publicId);
    await fetchCategories();
  };

  const handleSubmit = async (data: any) => {
    if (editingCategory) {
      await categoryService.update(editingCategory.public_id, data);
    } else {
      await categoryService.create(data);
    }
    setModalOpen(false);
    setEditingCategory(null);
    await fetchCategories();
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Categories</h1>
        <button
          onClick={() => {
            setEditingCategory(null);
            setModalOpen(true);
          }}
          className="bg-black text-white px-4 py-2 rounded-lg"
        >
          Add Category
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "name", label: "Name" },
            { key: "slug", label: "Slug" },
            { key: "is_active", label: "Active", render: (val) => (val ? "✅" : "❌") },
          ]}
          data={categories}
          onEdit={(cat) => {
            setEditingCategory(cat);
            setModalOpen(true);
          }}
          onDelete={(cat) => handleDelete(cat.public_id)}
        />
      )}

      <Modal open={modalOpen} onClose={() => { setModalOpen(false); setEditingCategory(null); }}>
        <CategoryForm initialData={editingCategory} onSubmit={handleSubmit} />
      </Modal>
    </div>
  );
}