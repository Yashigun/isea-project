import Container from "@/components/layout/Container";
import ProductGrid from "@/components/ProductGrid";

import Section from "@/components/ui/Section";

import SectionHeading from "@/components/common/SectionHeading";

import {
    getCategoryBySlug,
} from "@/services/category";

import {
    getProductsByCategory,
} from "@/services/product";

interface Props{
    params:Promise<{
        slug:string
    }>
}

export default async function CollectionPage({
    params,
}:Props){

    const {slug}=await params;

    const category =
        await getCategoryBySlug(slug);

    if(!category){

        return(
            <Container>

                Category not found.

            </Container>
        )

    }

    const products =
        await getProductsByCategory(slug);

    return(

        <Section>

            <Container>

                <SectionHeading
                    title={category.name}
                    subtitle={
                        category.description
                    }
                />

                <ProductGrid
                    products={products}
                />

            </Container>

        </Section>

    )

}