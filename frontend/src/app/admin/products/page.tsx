"use client";

import { useEffect, useState } from "react";
import { productService, Product } from "@/services/product";
import { categoryService, Category } from "@/services/category";
import DataTable from "@/components/admin/DataTable";
import ProductForm from "@/components/admin/ProductForm";
import Modal from "@/components/admin/Modal";

export default function AdminProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [productsData, categoriesData] = await Promise.all([
        productService.getAll(),
        categoryService.getAll(false),
      ]);
      setProducts(productsData);
      setCategories(categoriesData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void Promise.resolve().then(fetchData);
  }, []);

  const handleDelete = async (publicId: string) => {
    if (!confirm("Delete this product?")) return;
    await productService.delete(publicId);
    await fetchData();
  };

  const handleSubmit = async (data: {
    category_public_id: string;
    name: string;
    slug: string;
    price: number;
    discount_price?: number | null;
    short_description?: string | null;
    description?: string | null;
    is_active?: boolean;
  }) => {
    let savedProduct;
    if (editingProduct) {
      savedProduct = await productService.update(editingProduct.public_id, data);
    } else {
      savedProduct = await productService.create(data);
    }
    setModalOpen(false);
    setEditingProduct(null);
    await fetchData();
    return savedProduct;
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Products</h1>
        <button
          onClick={() => {
            setEditingProduct(null);
            setModalOpen(true);
          }}
          className="bg-black text-white px-4 py-2 rounded-lg"
        >
          Add Product
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <DataTable
          columns={[
            { key: "name", label: "Name" },
            { key: "price", label: "Price" },
            { key: "is_active", label: "Active", render: (val) => (val ? "✅" : "❌") },
          ]}
          data={products}
          onEdit={(p) => {
            setEditingProduct(p);
            setModalOpen(true);
          }}
          onDelete={(p) => handleDelete(p.public_id)}
        />
      )}

      <Modal open={modalOpen} onClose={() => { setModalOpen(false); setEditingProduct(null); }}>
        <ProductForm
          categories={categories}
          initialData={editingProduct}
          onSubmit={handleSubmit}
        />
      </Modal>
    </div>
  );
}
