from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.dependencies import (
    get_category_service,
)

from app.schemas.category import (
    CategoryResponseSchema,
)

from app.schemas.product import (
    ProductResponseSchema,
)

from app.schemas.response import (
    SuccessResponse,
)

from app.services.storefront.category_service import (
    CategoryService,
)

router = APIRouter(
    prefix="/categories",
    tags=["Public Categories"],
)


@router.get(
    "",
    response_model=SuccessResponse[
        list[CategoryResponseSchema]
    ],
    summary="List Categories",
)
def list_categories(
    service: CategoryService = Depends(
        get_category_service,
    ),
):

    categories = service.list_categories()

    return SuccessResponse(
        message="Categories retrieved successfully.",
        data=categories,
    )


@router.get(
    "/{slug}",
    response_model=SuccessResponse[
        CategoryResponseSchema
    ],
    summary="Get Category",
)
def get_category(
    slug: str,
    service: CategoryService = Depends(
        get_category_service,
    ),
):

    category = service.get_category_by_slug(
        slug,
    )

    if category is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return SuccessResponse(
        message="Category retrieved successfully.",
        data=category,
    )


@router.get(
    "/{slug}/products",
    response_model=SuccessResponse[
        list[ProductResponseSchema]
    ],
    summary="List Category Products",
)
def get_category_products(
    slug: str,
    service: CategoryService = Depends(
        get_category_service,
    ),
):

    products = service.get_category_products(
        slug,
    )

    return SuccessResponse(
        message="Products retrieved successfully.",
        data=products,
    )