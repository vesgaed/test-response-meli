from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .dependencies import limiter
from .api.endpoints import products

from .core.config import settings

# --- App Initialization ---
app = FastAPI(
    title=settings.APP_NAME,
    description="API to support the item detail page, including AI-powered recommendations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],   # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],   # Permite todas las cabeceras
)

# --- Rate Limiter Configuration ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Static Files Mount ---
# This serves images from the 'public/images' directory
app.mount("/images", StaticFiles(directory="public/images"), name="images")

# --- API Router Inclusion ---
# Includes all endpoints defined in the products router
app.include_router(products.router, prefix=settings.API_V1_STR, tags=["Products"])

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the Mercado Libre Challenge API!"}