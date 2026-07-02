import { products } from "@/data/products";

export async function getProducts() {
    return products;
}

export async function getProductBySlug(
    slug: string,
) {
    return products.find(
        product => product.slug === slug
    );
}

export async function getProductsByCategory(
    slug: string,
) {
    return products.filter(
        product =>
            product.category.slug === slug
    );
}