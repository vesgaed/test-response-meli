from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import List, Optional

from ...dependencies import limiter
from ...models.product import ProductDetail, ProductSummary
from ...repositories.product_repository import ProductRepository
from ...services import recommender

# Use dependency injection for the repository
# This makes the endpoint easier to test
def get_repository() -> ProductRepository:
    """Dependency to provide the repository instance."""
    return ProductRepository()

router = APIRouter()
@router.get(
    "/items",
    response_model=List[ProductSummary],
    summary="List and Filter Products",
    description="Fetches a list of all products, with optional filters for category and brand."
)
@limiter.limit("200/minute")
async def get_all_items(
    request: Request,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    repo: ProductRepository = Depends(get_repository)
):
    """
    Endpoint to retrieve a list of product summaries.
    Supports filtering by category name and brand.
    """
    products = repo.find_all_products(category=category, brand=brand)
    return products

@router.get(
    "/items/{item_id}",
    response_model=ProductDetail,
    summary="Get Product Details",
    description="Fetches all details for a specific product, including seller and reviews."
)
@limiter.limit("100/minute")
async def get_item_details(
    item_id: str,
    request: Request,
    repo: ProductRepository = Depends(get_repository)
):
    """
    Endpoint to retrieve the full details of a single product.
    - Handles 'Not Found' errors gracefully.
    - Protected by a rate limit of 100 requests per minute per IP.
    """
    product_details = repo.find_product_details_by_id(item_id)
    if not product_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{item_id}' not found."
        )
    return product_details

@router.get(
    "/items/{item_id}/related",
    response_model=List[ProductSummary],
    summary="Get Related Products",
    description="Fetches a list of recommended products based on content similarity using an ML model."
)
@limiter.limit("50/minute")
async def get_related_items(
    item_id: str,
    request: Request,
    repo: ProductRepository = Depends(get_repository)
):
    """
    Endpoint to retrieve AI-powered product recommendations.
    - Protected by a stricter rate limit to account for higher computational cost.
    """
    all_products_df = repo.get_all_products_for_recommendation()
    
    # Check if the base product exists
    if item_id not in all_products_df['id'].values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{item_id}' not found, cannot generate recommendations."
        )
        
    recommended_ids = recommender.generate_recommendations(item_id, all_products_df)
    
    if not recommended_ids:
        return []

    recommended_products_summary = repo.find_products_by_ids(recommended_ids)
    
    return recommended_products_summary