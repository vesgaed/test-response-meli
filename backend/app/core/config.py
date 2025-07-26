from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables.
    """
    APP_NAME: str = "Mercado Libre Challenge API"
    API_V1_STR: str = "/api/v1"

# Instantiate settings to be imported by other modules
settings = Settings()