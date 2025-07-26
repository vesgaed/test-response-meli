import httpx
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Mounts the static files directory for serving CSS and images
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Backend API URL. Docker Compose allows using the service name for internal networking.
BACKEND_API_URL = "http://backend:8000/api/v1"


@app.get("/")
async def home(
    request: Request,
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None)
):
    """
    Renders the main page with a list of products, supporting optional filtering by category and brand.
    Fetches product data from the backend API and provides hardcoded categories and brands for demonstration purposes.
    """
    async with httpx.AsyncClient() as client:
        # Request the product list from the backend API
        params = {"category": category, "brand": brand}
        # Remove None values to avoid sending empty query parameters
        active_params = {k: v for k, v in params.items() if v is not None}

        products_response = await client.get(f"{BACKEND_API_URL}/items", params=active_params)
        products = products_response.json() if products_response.status_code == 200 else []

        # In a real scenario, categories and brands would be fetched from the API
        # For this test, they are hardcoded for simplicity
        categories = ["Smartphones", "Muebles", "Papelería"]
        brands = ["Apple", "Samsung", "Motorola", "Maderkit", "Madesa", "Norma", "Scribe", "Offi-Esco"]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "categories": categories,
        "brands": brands,
        "selected_category": category,
        "selected_brand": brand
    })



@app.get("/item/{item_id}")
async def item_detail(request: Request, item_id: str):
    """
    Renders the detail page for a specific product.
    Fetches product details from the backend API and passes them to the template.
    """
    async with httpx.AsyncClient() as client:
        # Request product details from the backend API
        product_response = await client.get(f"{BACKEND_API_URL}/items/{item_id}")
        product = product_response.json() if product_response.status_code == 200 else None

    return templates.TemplateResponse("detail.html", {
        "request": request,
        "product": product
    })