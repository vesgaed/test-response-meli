from pydantic import BaseModel, Field
from typing import List, Optional

class Price(BaseModel):
    """Model for the product price."""
    amount: float
    currency: str

class Category(BaseModel):
    """Model for a product category."""
    id: int
    name: str

class SellerReputation(BaseModel):
    """Model for the seller's reputation details."""
    level: str
    score: float

class Seller(BaseModel):
    """Model for the seller information."""
    id: str
    name: str
    is_official_store: bool
    reputation: SellerReputation

class Review(BaseModel):
    """Model for a single product review."""
    author: str
    rating: int
    comment: str

class PaymentMethod(BaseModel):
    """Model for an accepted payment method."""
    id: int
    name: str

class ProductSpecifications(BaseModel):
    """
    Model for category-specific attributes.
    This uses Optional for all fields to accommodate different categories.
    """
    model: Optional[str] = None
    color: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    screen_size: Optional[float] = None
    main_camera_resolution: Optional[str] = None
    operating_system: Optional[str] = None
    material: Optional[str] = None
    dimensions: Optional[dict] = None
    style: Optional[str] = None
    requires_assembly: Optional[bool] = None
    item_type: Optional[str] = None
    units_per_package: Optional[int] = None
    size: Optional[str] = None
    page_count: Optional[int] = None
    paper_type: Optional[str] = None
    ink_color: Optional[str] = None
    tip_size: Optional[str] = None

class ProductSummary(BaseModel):
    """A simplified model for lists of products, like recommendations."""
    id: str
    title: str
    price: Price
    image: str = Field(..., description="Primary image for the product")
    average_rating: float

class ProductDetail(BaseModel):
    """
    The main model for the product detail response.
    This is the enriched object sent to the frontend.
    """
    id: str
    title: str
    price: Price
    description: str
    images: List[str]
    stock: int
    average_rating: float = Field(..., description="Calculated average rating from reviews")
    category: Category
    seller: Seller
    reviews: List[Review]
    accepted_payment_methods: List[PaymentMethod]
    specifications: ProductSpecifications
    related_products: List[ProductSummary]

