import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.services import recommender

class ProductRepository:
    """
    Repository class responsible for managing product-related data operations.
    Loads data from JSON files and provides methods for querying, enriching, and summarizing product information.
    Abstracts the data source from the rest of the application for maintainability and testability.
    """
    def __init__(self, data_path: Path = Path("app/data")):
        """
        Loads all required data files into memory as pandas DataFrames for efficient access.
        Raises RuntimeError if any data file is missing.
        """
        self.data_path = data_path
        try:
            self.products_df = pd.read_json(data_path / "products.json")
            self.categories_df = pd.read_json(data_path / "categories.json").set_index('id')
            self.sellers_df = pd.read_json(data_path / "sellers.json").set_index('id')
            self.reviews_df = pd.read_json(data_path / "reviews.json")
            self.payment_methods_df = pd.read_json(data_path / "payment_methods.json").set_index('id')
        except FileNotFoundError as e:
            raise RuntimeError(f"Data file not found: {e}. Ensure all JSON files are in {data_path}")

    def get_all_products_for_recommendation(self) -> pd.DataFrame:
        """
        Returns a copy of the products DataFrame for use in recommendation algorithms.
        """
        return self.products_df.copy()

    def find_product_details_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed information for a product by its ID, including related category, seller, reviews, payment methods, specifications, and recommended products.
        Returns None if the product is not found.
        """
        # Filter the DataFrame to find the product by ID
        product_df_filtered = self.products_df[self.products_df['id'] == item_id]

        # Return None if the product does not exist
        if product_df_filtered.empty:
            return None

        # Extract the product data as a Series
        product_series = product_df_filtered.iloc[0]

        # Enrich product data with related information
        category = self.categories_df.loc[product_series['category_id']].to_dict()
        category['id'] = product_series['category_id']

        seller = self.sellers_df.loc[product_series['seller_id']].to_dict()
        seller['id'] = product_series['seller_id']

        product_reviews = self.reviews_df[self.reviews_df['product_id'] == item_id]
        average_rating = product_reviews['rating'].mean() if not product_reviews.empty else 0.0

        payment_method_ids = product_series['accepted_payment_method_ids']
        accepted_payments = self.payment_methods_df.loc[payment_method_ids].reset_index().to_dict('records')

        # Generate recommended product IDs using the recommender service
        all_products_df = self.get_all_products_for_recommendation()
        product_category_id = product_series['category_id']
        recommended_ids = recommender.generate_recommendations(item_id, product_category_id, all_products_df)
        related_products = self.find_products_by_ids(recommended_ids)

        # Assemble the final product details dictionary
        product_details = {
            "id": product_series['id'],
            "title": product_series['title'],
            "description": product_series['description'],
            "price": product_series['price'],
            "images": product_series['images'],
            "stock": product_series['stock'],
            "average_rating": round(average_rating, 2),
            "category": category,
            "seller": seller,
            "reviews": product_reviews[['author', 'rating', 'comment']].to_dict('records'),
            "accepted_payment_methods": accepted_payments,
            "specifications": product_series['specifications'],
            "related_products": related_products
        }

        return product_details

    def find_products_by_ids(self, item_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieves summary information for multiple products by their IDs.
        Returns a list of product summaries including average rating and main image.
        """
        
        products_subset = self.products_df[self.products_df['id'].isin(item_ids)]

        # Using a functional approach with apply to process each row
        def create_summary(row):
            product_reviews = self.reviews_df[self.reviews_df['product_id'] == row['id']]
            average_rating = product_reviews['rating'].mean() if not product_reviews.empty else 0.0
            return {
                "id": row['id'],
                "title": row['title'],
                "price": row['price'],
                "image": row['images'][0] if row['images'] else "",
                "average_rating": round(average_rating, 2)
            }
            
        return list(products_subset.apply(create_summary, axis=1))
    
    def find_all_products(self, category: Optional[str] = None, brand: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves all products, with optional filtering by category name and brand.
        Returns a list of product summaries for display on the main page.
        """
        # Start with a copy of all products
        filtered_df = self.products_df.copy()

        # Filter by brand if specified and the column exists
        if brand and 'brand' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['brand'] == brand]

        # Filter by category if specified
        if category:
            categories_for_merge = self.categories_df.reset_index()
            merged_df = pd.merge(
                filtered_df,
                categories_for_merge,
                left_on='category_id',
                right_on='id',
                suffixes=('', '_cat')
            )
            filtered_df = merged_df[merged_df['name'] == category]

        # Return an empty list if no products match the filters
        if filtered_df.empty:
            return []

        # Create summary for each product
        def create_summary(row):
            product_reviews = self.reviews_df[self.reviews_df['product_id'] == row['id']]
            average_rating = product_reviews['rating'].mean() if not product_reviews.empty else 0.0
            return {
                "id": row['id'],
                "title": row['title'],
                "price": row['price'],
                "image": row['images'][0] if row['images'] else "",
                "average_rating": round(average_rating, 2)
            }

        return list(filtered_df.apply(create_summary, axis=1))