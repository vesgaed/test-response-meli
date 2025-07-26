import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def generate_recommendations(
    product_id: str,
    category_id: int,
    products_df: pd.DataFrame,
    top_n: int = 5
) -> List[str]:
    """
    Generates product recommendations based on content similarity within the same category.
    This function filters products by category, computes text-based similarity, and returns the most relevant product IDs.
    Args:
        product_id (str): The ID of the reference product.
        category_id (int): The category to filter products by.
        products_df (pd.DataFrame): DataFrame containing product data.
        top_n (int): Number of recommendations to return.
    Returns:
        List[str]: List of recommended product IDs.
    """
    # Filter products to include only those in the specified category
    category_products_df = products_df[products_df['category_id'] == category_id].copy()

    # If there are fewer than two products, no recommendations can be made
    if len(category_products_df) < 2:
        return []

    # Combine title and description for feature extraction
    category_products_df['combined_features'] = category_products_df['title'] + ' ' + category_products_df.get('description', '')

    # Compute TF-IDF matrix and cosine similarity for content-based filtering
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(category_products_df['combined_features'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the reference product within the filtered DataFrame
    try:
        idx = category_products_df.index[category_products_df['id'] == product_id].tolist()[0]
        local_idx = category_products_df.index.get_loc(idx)
    except (IndexError, KeyError):
        return []

    # Sort products by similarity score (excluding the reference product itself)
    sim_scores = list(enumerate(cosine_sim[local_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Select the top N most similar products
    top_similar_local_indices = [i[0] for i in sim_scores[1:top_n + 1]]

    # Retrieve the IDs of the recommended products
    recommended_product_ids = category_products_df.iloc[top_similar_local_indices]['id'].tolist()

    return recommended_product_ids