import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def generate_recommendations(
    product_id: str,
    category_id: int, # <-- Nuevo parámetro
    products_df: pd.DataFrame,
    top_n: int = 5
) -> List[str]:
    """
    Generates relevant product recommendations by first filtering by category,
    then calculating content similarity.
    """
    # 1. Filtrar productos que pertenecen a la MISMA CATEGORÍA.
    category_products_df = products_df[products_df['category_id'] == category_id].copy()

    # Si no hay otros productos en la categoría, no hay nada que recomendar.
    if len(category_products_df) < 2:
        return []

    # 2. Ahora, aplicar la similitud de texto SOLO DENTRO de esa categoría.
    category_products_df['combined_features'] = category_products_df['title'] + ' ' + category_products_df.get('description', '')
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(category_products_df['combined_features'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Encuentra el índice del producto dentro del DataFrame filtrado
    try:
        idx = category_products_df.index[category_products_df['id'] == product_id].tolist()[0]
        # Mapea el índice del DataFrame original al índice del DataFrame filtrado
        local_idx = category_products_df.index.get_loc(idx)
    except (IndexError, KeyError):
        return []

    sim_scores = list(enumerate(cosine_sim[local_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtiene los índices locales de los productos más similares
    top_similar_local_indices = [i[0] for i in sim_scores[1:top_n + 1]]
    
    # Obtiene los IDs reales de los productos recomendados
    recommended_product_ids = category_products_df.iloc[top_similar_local_indices]['id'].tolist()
    
    return recommended_product_ids