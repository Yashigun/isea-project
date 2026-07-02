import { categories } from "@/data/categories";

export async function getCategories() {
    return categories;
}

export async function getCategoryBySlug(
    slug: string,
) {
    return categories.find(
        category => category.slug === slug
    );
}