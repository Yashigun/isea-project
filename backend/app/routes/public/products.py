from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from app.dependencies import (
    get_product_service,
)

from app.schemas.product import (
    ProductResponseSchema,
)

from app.schemas.response import (
    SuccessResponse,
)

from app.services.storefront.product_service import (
    ProductService,
)

router = APIRouter(
    prefix="/products",
    tags=["Public Products"],
)


@router.get(
    "",
    response_model=SuccessResponse[
        list[ProductResponseSchema]
    ],
    summary="List Products",
)
def list_products(
    service: ProductService = Depends(
        get_product_service,
    ),
):

    products = service.list_products()

    return SuccessResponse(
        message="Products retrieved successfully.",
        data=products,
    )


@router.get(
    "/search",
    response_model=SuccessResponse[
        list[ProductResponseSchema]
    ],
    summary="Search Products",
)
def search_products(
    query: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="Search query",
    ),
    service: ProductService = Depends(
        get_product_service,
    ),
):

    products = service.search_products(
        query,
    )

    return SuccessResponse(
        message="Products retrieved successfully.",
        data=products,
    )


@router.get(
    "/category/{slug}",
    response_model=SuccessResponse[
        list[ProductResponseSchema]
    ],
    summary="Products By Category",
)
def get_products_by_category(
    slug: str,
    service: ProductService = Depends(
        get_product_service,
    ),
):

    products = service.get_products_by_category(
        slug,
    )

    return SuccessResponse(
        message="Products retrieved successfully.",
        data=products,
    )


@router.get(
    "/{slug}",
    response_model=SuccessResponse[
        ProductResponseSchema
    ],
    summary="Product Details",
)
def get_product(
    slug: str,
    service: ProductService = Depends(
        get_product_service,
    ),
):

    product = service.get_product_by_slug(
        slug,
    )

    if product is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return SuccessResponse(
        message="Product retrieved successfully.",
        data=product,
    )


@router.get(
    "/{slug}/related",
    response_model=SuccessResponse[
        list[ProductResponseSchema]
    ],
    summary="Related Products",
)
def related_products(
    slug: str,
    service: ProductService = Depends(
        get_product_service,
    ),
):

    products = service.get_related_products(
        slug,
    )

    return SuccessResponse(
        message="Related products retrieved successfully.",
        data=products,
    )