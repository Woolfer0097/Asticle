import requests
import streamlit as st


from auth.state import is_authenticated
from api.client import (
    get_error_message,
    get_favourite_by_article_id,
    add_favourite,
    remove_favourite,
    delete_article,
)


def render_article_card(article: dict) -> None:
    article_id = article.get("id")

    with st.container(border=True):
        if article.get("photo_path") != "-":
            st.image(article.get("photo_path"), use_container_width=True)
        else:
            st.info("Изображение не добавлено")

        left, right = st.columns(2, vertical_alignment="bottom")
        left.subheader(article.get("title"))
        left.write(f'Уровень: {article.get("level")}')
        left.write(f'Тип: {article.get("category")}')
        left.write(f'Нация: {article.get("nation")}')

        if right.button("Подробнее", key=f"card_details_{article_id}"):
            st.session_state["selected_article_id"] = article_id
            st.switch_page("pages/article.py")


def render_favorite_button(article: dict, key_prefix: str) -> None:
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    article_id = article.get("id")
    is_favorite = get_favourite_by_article_id(article_id)
    button_text = (
        "Убрать из избранного" if is_favorite.status_code == 200 else "В избранное"
    )

    if st.button(button_text, key=f"{key_prefix}_favorite_{article_id}", type="primary"):
        try:
            if is_favorite.status_code == 200:
                response = remove_favourite(article_id)
            else:
                response = add_favourite(article_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.rerun()
        else:
            st.error(get_error_message(response))


@st.dialog("Вы уверены, что хотите удалить этот статью? Возврат будет невозможен!")
def delete_yes(article_id: int):
    if st.button("Да", key=f"card_delete_yes_{article_id}", type="primary"):
        response = delete_article(article_id)
        if response.ok:
            st.rerun()
        else:
            st.error(get_error_message(response))


def render_article_card_for_edit(article: dict) -> None:
    article_id = article.get("id")

    with st.container(border=True):
        if article.get("photo_path") != "-":
            st.image(article.get("photo_path"), use_container_width=True)
        else:
            st.info("Изображение не добавлено")

        left, right = st.columns(2, vertical_alignment="bottom")
        left.subheader(article.get("title"))
        left.write(f'Уровень: {article.get("level")}')
        left.write(f'Тип: {article.get("category")}')
        left.write(f'Нация: {article.get("nation")}')

        if right.button("Редактировать", key=f"card_edit_{article_id}"):
            st.session_state["selected_article_id"] = article_id
            st.switch_page("pages/admin/update_article.py")
        if right.button("Удалить", key=f"card_delete_{article_id}", type="primary"):
            delete_yes(article_id)
