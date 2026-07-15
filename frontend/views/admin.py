import requests
import streamlit as st

from api.client import (
    create_article,
    delete_article,
    error_message,
    get_users,
    read_json,
    update_article,
)
from auth.state import current_profile, get_token, is_admin, is_authenticated
from services.articles import fetch_articles, upload_cover
from ui.layout import render_header


def render_create_article_page(home_page: st.Page) -> None:
    render_header()

    if not is_authenticated():
        st.error("Создание статей доступно только авторизованным пользователям.")
        return

    render_create_article_form(home_page)


def render_edit_articles_page() -> None:
    render_header()

    if not is_authenticated():
        st.error("Редактирование статей доступно только авторизованным пользователям.")
        return

    try:
        articles = fetch_articles()
    except (requests.RequestException, RuntimeError) as exc:
        st.error(str(exc) or "Не удалось загрузить статьи.")
        return

    editable = editable_articles(articles)
    selected_article_id = st.session_state.get("selected_edit_article_id")
    if selected_article_id is None:
        st.info("Выберите статью через кнопку редактирования в каталоге или на странице статьи.")
        return

    article = find_article_for_edit(editable, selected_article_id)
    if article is None:
        st.error("Эта статья недоступна для редактирования.")
        return

    render_edit_article_form(article)


def render_users_page() -> None:
    render_header()

    if not is_authenticated():
        st.error("Список пользователей доступен только администратору.")
        return

    if not is_admin():
        st.error("Список пользователей доступен только администратору.")
        return

    render_users_table()


def editable_articles(articles: list[dict]) -> list[dict]:
    if is_admin():
        return articles

    profile = current_profile() or {}
    user_id = profile.get("id")
    return [article for article in articles if article.get("owner_id") == user_id]


def find_article_for_edit(articles: list[dict], article_id: object) -> dict | None:
    try:
        selected_id = int(article_id)
    except (TypeError, ValueError):
        return None

    return next(
        (article for article in articles if int(article["id"]) == selected_id),
        None,
    )


def render_create_article_form(home_page: st.Page) -> None:
    st.subheader("Новая статья")
    with st.form("create_article_form", clear_on_submit=True):
        title = st.text_input("Заголовок")
        content = st.text_area("Текст", height=220)
        cover = st.file_uploader(
            "Обложка",
            type=["png", "jpg", "jpeg", "webp"],
            key="create_cover",
        )
        submitted = st.form_submit_button("Создать", type="primary")

    if not submitted:
        return

    if not title.strip() or not content.strip():
        st.error("Заголовок и текст обязательны.")
        return

    response = create_article(title.strip(), content.strip())
    if not response.ok:
        st.error(error_message(response))
        return

    article = response.json()
    if upload_cover(int(article["id"]), cover):
        st.session_state["catalog_notice"] = "Статья успешно добавлена."
        st.switch_page(home_page)


def render_edit_article_form(article: dict) -> None:
    article_id = int(article["id"])
    st.subheader(article.get("title") or "Редактирование статьи")

    with st.form("edit_article_form"):
        title = st.text_input("Заголовок", value=article.get("title") or "")
        content = st.text_area(
            "Текст",
            value=article.get("content") or "",
            height=240,
        )
        cover = st.file_uploader(
            "Новая обложка",
            type=["png", "jpg", "jpeg", "webp"],
            key=f"edit_cover_{article_id}",
        )
        left, right = st.columns(2)
        save = left.form_submit_button("Сохранить", type="primary")
        delete = right.form_submit_button("Удалить")

    if save:
        response = update_article(article_id, title.strip(), content.strip())
        if not response.ok:
            st.error(error_message(response))
            return
        if upload_cover(article_id, cover):
            st.success("Изменения сохранены.")
            st.rerun()

    if delete:
        response = delete_article(article_id)
        if response.ok:
            st.session_state["selected_article_id"] = None
            st.session_state["selected_edit_article_id"] = None
            st.success("Статья удалена.")
            st.rerun()
        else:
            st.error(error_message(response))


def render_users_table() -> None:
    token = get_token()
    if not token:
        st.error("Нет токена авторизации.")
        return

    try:
        response = get_users(token)
    except requests.RequestException:
        st.error("Не удалось загрузить пользователей.")
        return

    if not response.ok:
        st.error(error_message(response))
        return

    users = read_json(response, [])
    if not users:
        st.info("Пользователей нет.")
        return

    st.dataframe(
        [
            {
                "id": user.get("id"),
                "alias": user.get("alias"),
                "email": user.get("email"),
                "role": user.get("role"),
                "active": user.get("is_active"),
            }
            for user in users
        ],
        hide_index=True,
        width="stretch",
    )
