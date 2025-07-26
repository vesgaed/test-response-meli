# This module configures and provides the rate limiter for the FastAPI application.
# It uses SlowAPI to protect endpoints against excessive requests and potential abuse.
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)