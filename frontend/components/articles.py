from collections.abc import Callable
from textwrap import shorten
from typing import Any

import streamlit as st

from api.client import media_url
from auth.state import can_manage_article


def render_cover(article: dict[str, Any]) -> None:
    src = media_url(article.get("cover_url"))
    if src:
        st.image(src, width="stretch")
    else:
        st.markdown(
            '<div class="article-cover">Без обложки</div>',
            unsafe_allow_html=True,
        )


def render_article_card(
    article: dict[str, Any],
    favourite_ids: set[int],
    on_toggle_favourite: Callable[[int, set[int]], None],
    on_edit_article: Callable[[dict[str, Any]], None],
    on_delete_article: Callable[[dict[str, Any]], None],
    article_page: st.Page,
) -> None:
    article_id = int(article["id"])
    is_favourite = article_id in favourite_ids
    content = article.get("content") or ""

    with st.container(border=True):
        render_cover(article)
        st.subheader(article.get("title") or "Без названия")
        st.caption(f"Просмотры: {article.get('views', 0)}")
        st.write(shorten(content.replace("\n", " "), width=180, placeholder="..."))

        left, right = st.columns(2)
        if left.button("Открыть", key=f"open_{article_id}", width="stretch"):
            st.session_state["selected_article_id"] = article_id
            st.switch_page(article_page)

        fav_label = "Убрать" if is_favourite else "В избранное"
        if right.button(fav_label, key=f"fav_{article_id}", width="stretch"):
            on_toggle_favourite(article_id, favourite_ids)

        if can_manage_article(article):
            manage_left, manage_right = st.columns(2)
            if manage_left.button(
                "Редактировать",
                key=f"edit_{article_id}",
                icon=":material/edit:",
                width="stretch",
            ):
                on_edit_article(article)

            if manage_right.button(
                "Удалить",
                key=f"delete_{article_id}",
                icon=":material/delete:",
                width="stretch",
            ):
                on_delete_article(article)


def render_article_detail(
    article: dict[str, Any],
    favourite_ids: set[int],
    on_toggle_favourite: Callable[[int, set[int]], None],
    on_edit_article: Callable[[dict[str, Any]], None],
    on_delete_article: Callable[[dict[str, Any]], None],
    on_close: Callable[[], None],
) -> None:
    article_id = int(article["id"])
    is_favourite = article_id in favourite_ids

    left, right = st.columns([0.95, 1.25], gap="large")

    with left:
        render_cover(article)

    with right:
        st.title(article.get("title") or "Без названия")
        st.markdown(
            f"""
            <div class="metric-strip">
                <div><strong>{article.get("views", 0)}</strong><span>просмотров</span></div>
                <div><strong>{len(article.get("content") or "")}</strong><span>символов</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(article.get("content") or "Текст статьи пока пуст.")

        c1, c2 = st.columns(2)
        if c1.button("Закрыть", width="stretch"):
            on_close()

        fav_label = "Убрать из избранного" if is_favourite else "Добавить в избранное"
        if c2.button(fav_label, type="primary", width="stretch"):
            on_toggle_favourite(article_id, favourite_ids)

        if can_manage_article(article):
            manage_left, manage_right = st.columns(2)
            if manage_left.button(
                "Редактировать",
                key=f"detail_edit_{article_id}",
                icon=":material/edit:",
                width="stretch",
            ):
                on_edit_article(article)

            if manage_right.button(
                "Удалить",
                key=f"detail_delete_{article_id}",
                icon=":material/delete:",
                width="stretch",
            ):
                on_delete_article(article)
