import os

import streamlit as st


def get_setting(name: str, default: str) -> str:
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


BACKEND_URL = get_setting("ASTICLE_API_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 8
