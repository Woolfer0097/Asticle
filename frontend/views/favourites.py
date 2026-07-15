from __future__ import annotations

import requests
import streamlit as st

from auth.state import is_authenticated
from services.articles import fetch_articles, fetch_favourite_ids
from ui.layout import render_header
from views.shared import render_article_grid


def render_favourites(article_page: st.Page, edit_page: st.Page | None) -> None:
    render_header()

    if not is_authenticated():
        st.warning("Войдите, чтобы открыть избранное.")
        return

    try:
        articles = fetch_articles()
        favourite_ids = fetch_favourite_ids()
    except (requests.RequestException, RuntimeError) as exc:
        st.error(str(exc) or "Не удалось загрузить избранное.")
        return

    favourite_articles = [
        article for article in articles if int(article["id"]) in favourite_ids
    ]

    st.subheader("Избранное")
    if not favourite_articles:
        st.info("Здесь пока нет статей.")
        return

    render_article_grid(favourite_articles, favourite_ids, article_page, edit_page)
