import os
from collections.abc import Mapping

import streamlit as st


BACKEND_SETTING_NAMES = ("BACKEND_URL", "ASTICLE_API_URL")
SECRET_SECTIONS = ("general", "api", "backend")


def normalize_url(value: object) -> str:
    return str(value).strip().rstrip("/")


def get_secret(name: str) -> object | None:
    try:
        value = st.secrets.get(name)
        if value:
            return value

        for section_name in SECRET_SECTIONS:
            section = st.secrets.get(section_name)
            if isinstance(section, Mapping):
                value = section.get(name)
                if value:
                    return value
    except Exception:
        return None

    return None


def get_setting(names: tuple[str, ...], default: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return normalize_url(value)

    for name in names:
        value = get_secret(name)
        if value:
            return normalize_url(value)

    return normalize_url(default)


def get_backend_url() -> str:
    return get_setting(BACKEND_SETTING_NAMES, "http://127.0.0.1:8000")


BACKEND_URL = get_backend_url()
REQUEST_TIMEOUT = 8
