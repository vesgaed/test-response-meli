# backend/tests/api/endpoints/test_products.py

from fastapi.testclient import TestClient
from app.main import app
from app.api.endpoints.products import get_repository
from app.repositories.product_repository import ProductRepository

# --- Test Setup for Performance ---
# A single, shared instance of the repository is created once to ensure
# data files are read from disk only at the start of the test session.
repository_instance = ProductRepository()

def get_repository_override():
    """Returns the shared repository instance for testing."""
    return repository_instance

# The dependency override is applied to the app before creating the client.
app.dependency_overrides[get_repository] = get_repository_override

client = TestClient(app)


# --- Tests for the Product Detail Endpoint ---

def test_get_item_details_success():
    """
    Tests the happy path for the get_item_details endpoint.
    Verifies that a valid product ID returns a 200 OK and a complete,
    well-structured JSON payload, including the new 'description' and
    'related_products' fields.
    """
    response = client.get("/api/v1/items/SMA001") # Apple iPhone 15

    # Assert that the request was successful
    assert response.status_code == 200
    data = response.json()

    # Assert the payload contains all expected top-level keys
    assert data["id"] == "SMA001"
    assert "description" in data
    assert "related_products" in data
    assert data["seller"]["name"] == "Tienda Oficial Apple"
    
    # Assert that related_products is a list
    assert isinstance(data["related_products"], list)
    
    # If recommendations are returned, verify they are relevant (same category)
    if data["related_products"]:
        first_related_product_id = data["related_products"][0]["id"]
        related_product_response = client.get(f"/api/v1/items/{first_related_product_id}")
        related_product_data = related_product_response.json()
        
        # Check that the recommended product is in the same category as the original
        assert related_product_data["category"]["id"] == data["category"]["id"]


def test_get_item_details_not_found():
    """
    Tests the error path for the get_item_details endpoint.
    Verifies that a non-existent product ID returns a 404 Not Found.
    """
    response = client.get("/api/v1/items/ID_DOES_NOT_EXIST")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product with ID 'ID_DOES_NOT_EXIST' not found."


# --- Tests for the Product Listing & Filtering Endpoint ---

def test_get_all_items_no_filter():
    """
    Tests fetching all products without any filters.
    Verifies it returns a 200 OK and the correct number of products.
    """
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # This assertion assumes you have 20 products in your JSON data file.
    assert len(data) == 20


def test_get_all_items_filter_by_category():
    """
    Tests filtering products by a valid category ('Smartphones').
    """
    response = client.get("/api/v1/items?category=Smartphones")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # A simple check to confirm all titles match the category's typical brands
    assert all("Apple" in p["title"] or "Samsung" in p["title"] or "Motorola" in p["title"] for p in data)


def test_get_all_items_filter_by_brand():
    """
    Tests filtering products by a valid brand ('Samsung').
    """
    response = client.get("/api/v1/items?brand=Samsung")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("Samsung" in p["title"] for p in data)


def test_get_all_items_filter_by_category_and_brand():
    """
    Tests filtering products by both category and brand ('Muebles', 'Maderkit').
    """
    response = client.get("/api/v1/items?category=Muebles&brand=Maderkit")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("Maderkit" in p["title"] for p in data)


def test_get_all_items_filter_no_results():
    """
    Tests a filter combination that should return no results.
    Verifies that the API correctly returns a 200 OK with an empty list.
    """
    response = client.get("/api/v1/items?brand=NonExistentBrand")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0