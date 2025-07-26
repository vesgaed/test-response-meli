import httpx
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# URL del API backend. Docker Compose nos permite usar el nombre del servicio.
BACKEND_API_URL = "http://backend:8000/api/v1"

@app.get("/")
async def home(
    request: Request,
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None)
):
    async with httpx.AsyncClient() as client:
        # Pide la lista de productos al backend
        params = {"category": category, "brand": brand}
        # Filtramos los None para no enviar query params vacíos
        active_params = {k: v for k, v in params.items() if v is not None}
        
        products_response = await client.get(f"{BACKEND_API_URL}/items", params=active_params)
        products = products_response.json() if products_response.status_code == 200 else []
        
        # Simulación: En un caso real, también pediríamos las categorías y marcas a la API
        # Por simplicidad para la prueba, los hardcodeamos aquí.
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
    async with httpx.AsyncClient() as client:
        # Pide los detalles de un producto específico al backend
        product_response = await client.get(f"{BACKEND_API_URL}/items/{item_id}")
        product = product_response.json() if product_response.status_code == 200 else None

    return templates.TemplateResponse("detail.html", {
        "request": request, 
        "product": product
    })