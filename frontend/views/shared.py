from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from api.client import delete_article, error_message
from components.articles import render_article_card
from services.articles import toggle_favourite


def handle_toggle_favourite(article_id: int, favourite_ids: set[int]) -> None:
    try:
        response = toggle_favourite(article_id, favourite_ids)
    except requests.RequestException:
        st.error("Не удалось обновить избранное.")
        return

    if response is None:
        return

    if response.ok:
        st.rerun()
    else:
        st.error(error_message(response))


def handle_edit_article(article: dict[str, Any], edit_page: st.Page | None) -> None:
    if edit_page is None:
        st.warning("Войдите в аккаунт, чтобы редактировать статьи.")
        return

    st.session_state["selected_edit_article_id"] = article.get("id")
    st.switch_page(edit_page)


def handle_delete_article(
    article: dict[str, Any],
    destination_page: st.Page | None = None,
) -> None:
    article_id = article.get("id")
    if article_id is None:
        st.error("Не удалось определить статью для удаления.")
        return

    try:
        response = delete_article(int(article_id))
    except requests.RequestException:
        st.error("Не удалось удалить статью.")
        return

    if response.ok:
        st.session_state["selected_article_id"] = None
        st.session_state["catalog_notice"] = "Статья удалена."
        if destination_page is not None:
            st.switch_page(destination_page)
        st.rerun()
    else:
        st.error(error_message(response))


def render_article_grid(
    articles: list[dict[str, Any]],
    favourite_ids: set[int],
    article_page: st.Page,
    edit_page: st.Page | None,
) -> None:
    columns = st.columns(3)
    for index, article in enumerate(articles):
        with columns[index % 3]:
            render_article_card(
                article,
                favourite_ids,
                handle_toggle_favourite,
                lambda selected_article: handle_edit_article(
                    selected_article,
                    edit_page,
                ),
                handle_delete_article,
                article_page,
            )
