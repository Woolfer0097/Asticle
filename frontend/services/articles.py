from typing import Any

import requests
import streamlit as st

from api import client
from auth.state import get_token, is_authenticated


def fetch_articles() -> list[dict[str, Any]]:
    response = client.get_articles()
    if not response.ok:
        raise RuntimeError(client.error_message(response))
    return client.read_json(response, [])


def fetch_article(article_id: int) -> dict[str, Any]:
    response = client.get_article(article_id)
    if not response.ok:
        raise RuntimeError(client.error_message(response))
    return response.json()


def fetch_favourite_ids() -> set[int]:
    token = get_token()
    if not token:
        return set()

    response = client.get_favourites(token)
    if response.status_code == 401:
        return set()
    if not response.ok:
        return set()

    return {
        int(item["article_id"])
        for item in client.read_json(response, [])
        if item.get("article_id") is not None
    }


def toggle_favourite(article_id: int, favourite_ids: set[int]) -> requests.Response | None:
    token = get_token()
    if not is_authenticated() or not token:
        st.warning("Войдите через страницу «Профиль», чтобы добавлять статьи в избранное.")
        return None

    if article_id in favourite_ids:
        return client.remove_favourite(token, article_id)

    return client.add_favourite(token, article_id)


def upload_cover(article_id: int, uploaded_file: Any) -> bool:
    if uploaded_file is None:
        return True

    response = client.upload_article_cover(article_id, uploaded_file)
    if response.ok:
        return True

    st.error(client.error_message(response))
    return False
