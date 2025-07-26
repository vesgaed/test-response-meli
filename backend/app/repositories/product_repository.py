import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.services import recommender

class ProductRepository:
    """
    Handles data operations by reading from JSON files.
    This layer abstracts the data source from the rest of the application.
    """
    def __init__(self, data_path: Path = Path("app/data")):
        """
        Initializes the repository by loading all data files into memory.
        Using pandas DataFrames for efficient in-memory data manipulation.
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
        """Returns a simplified DataFrame of all products for the ML model."""
        return self.products_df.copy()

    def find_product_details_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Finds a product by its ID and enriches it with related data.
        This method simulates a database JOIN operation by combining data
        from multiple pandas DataFrames.
        """
        # --- Lógica Corregida ---
        # 1. Filtra el DataFrame para encontrar el producto.
        product_df_filtered = self.products_df[self.products_df['id'] == item_id]
        
        # 2. VERIFICA si el DataFrame resultante está vacío ANTES de acceder a cualquier fila.
        if product_df_filtered.empty:
            # Si no se encontró el producto, retorna None inmediatamente.
            # La API convertirá esto en un 404 Not Found.
            return None
        
        # 3. Solo si el producto fue encontrado, obtén la primera (y única) fila.
        product_series = product_df_filtered.iloc[0]
        # -------------------------

        # --- Data Enrichment (esta parte no cambia) ---
        
        # Get Category
        category = self.categories_df.loc[product_series['category_id']].to_dict()
        category['id'] = product_series['category_id']

        # Get Seller
        seller = self.sellers_df.loc[product_series['seller_id']].to_dict()
        seller['id'] = product_series['seller_id']

        # Get Reviews and calculate average rating
        product_reviews = self.reviews_df[self.reviews_df['product_id'] == item_id]
        average_rating = product_reviews['rating'].mean() if not product_reviews.empty else 0.0
        
        # Get Accepted Payment Methods
        payment_method_ids = product_series['accepted_payment_method_ids']
        accepted_payments = self.payment_methods_df.loc[payment_method_ids].reset_index().to_dict('records')
        
        all_products_df = self.get_all_products_for_recommendation()
        product_category_id = product_series['category_id']
        recommended_ids = recommender.generate_recommendations(item_id, product_category_id, all_products_df)
        
        related_products = self.find_products_by_ids(recommended_ids)
        # Assemble the final response dictionary
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
        """Finds multiple products and returns them in a summary format."""
        
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
        Finds all products, with optional filtering by category name and brand.
        Returns a summary list for the main page.
        """
        # Inicia con una copia de todos los productos.
        filtered_df = self.products_df.copy()

        # Asegúrate de que la columna 'brand' exista antes de filtrar
        if brand and 'brand' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['brand'] == brand]

        # Si se necesita filtrar por categoría, ahora sí hacemos el merge.
        if category:
            categories_for_merge = self.categories_df.reset_index()
            merged_df = pd.merge(
                filtered_df,
                categories_for_merge,
                left_on='category_id',
                right_on='id',
                suffixes=('', '_cat')
            )
            # Aplicamos el filtro de categoría sobre la tabla unida.
            filtered_df = merged_df[merged_df['name'] == category]

        # Si no hay resultados después de filtrar, devuelve una lista vacía.
        if filtered_df.empty:
            return []
            
        # El resto de la función para crear el resumen
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