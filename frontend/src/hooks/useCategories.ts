import { useEffect, useState } from "react";

import { getCategories } from "@/services/category";

import { Category } from "@/types/category";

export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    getCategories().then(setCategories);
  }, []);

  return categories;
}