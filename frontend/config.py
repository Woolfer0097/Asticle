import os


BACKEND_URL = os.getenv("ASTICLE_API_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 8
