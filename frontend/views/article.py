from __future__ import annotations

import requests
import streamlit as st

from components.articles import render_article_detail
from services.articles import fetch_article, fetch_favourite_ids
from ui.layout import render_header
from views.shared import handle_delete_article, handle_edit_article, handle_toggle_favourite


def render_article_page(home_page: st.Page, edit_page: st.Page | None) -> None:
    render_header()

    selected_id = st.session_state.get("selected_article_id")
    if selected_id is None:
        st.info("Выберите статью на главной странице.")
        st.page_link(home_page, label="Перейти на главную")
        return

    try:
        article = fetch_article(int(selected_id))
        favourite_ids = fetch_favourite_ids()
    except (requests.RequestException, RuntimeError) as exc:
        st.error(str(exc) or "Не удалось загрузить статью.")
        return

    def close_article() -> None:
        st.session_state["selected_article_id"] = None
        st.switch_page(home_page)

    render_article_detail(
        article,
        favourite_ids,
        handle_toggle_favourite,
        lambda selected_article: handle_edit_article(selected_article, edit_page),
        lambda selected_article: handle_delete_article(selected_article, home_page),
        close_article,
    )
