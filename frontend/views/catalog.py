from __future__ import annotations

import requests
import streamlit as st

from services.articles import fetch_articles, fetch_favourite_ids
from ui.layout import render_header
from views.shared import render_article_grid


def render_catalog(article_page: st.Page, edit_page: st.Page | None) -> None:
    render_header()

    notice = st.session_state.pop("catalog_notice", None)
    if notice:
        st.success(notice)

    try:
        articles = fetch_articles()
        favourite_ids = fetch_favourite_ids()
    except (requests.RequestException, RuntimeError) as exc:
        st.error(str(exc) or "Backend недоступен. Запустите FastAPI на 127.0.0.1:8000.")
        return

    st.markdown(
        f"""
        <div class="metric-strip">
            <div><strong>{len(articles)}</strong><span>статей</span></div>
            <div><strong>{len(favourite_ids)}</strong><span>в избранном</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not articles:
        st.info("Статей пока нет.")
        return

    render_article_grid(articles, favourite_ids, article_page, edit_page)
