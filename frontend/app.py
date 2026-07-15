import streamlit as st

from auth.state import init_state, is_admin, is_authenticated, load_profile
from ui.styles import configure_page
from views.admin import (
    render_create_article_page,
    render_edit_articles_page,
    render_users_page,
)
from views.article import render_article_page
from views.auth import render_auth
from views.catalog import render_catalog
from views.favourites import render_favourites


def main() -> None:
    configure_page()
    init_state()

    if is_authenticated() and not st.session_state.get("profile"):
        load_profile()

    edit_page = None
    home_page = st.Page(
        lambda: render_catalog(article_page, edit_page),
        title="Главная",
        url_path="asticle-catalog",
        default=True,
    )
    article_page = st.Page(
        lambda: render_article_page(home_page, edit_page),
        title="Статья",
        url_path="asticle-article",
        visibility="hidden",
    )
    favourites_page = st.Page(
        lambda: render_favourites(article_page, edit_page),
        title="Избранное",
        url_path="asticle-favourites",
    )
    profile_page = st.Page(
        render_auth,
        title="Профиль",
        url_path="asticle-profile",
    )

    pages = {
        "Основное": [home_page, article_page, favourites_page, profile_page],
    }

    if is_authenticated():
        create_page = st.Page(
            lambda: render_create_article_page(home_page),
            title="Создать статью",
            url_path="asticle-create",
        )
        edit_page = st.Page(
            render_edit_articles_page,
            title="Редактировать статьи",
            url_path="asticle-edit",
        )
        pages["Управление"] = [
            create_page,
            edit_page,
        ]

        if is_admin():
            users_page = st.Page(
                render_users_page,
                title="Пользователи",
                url_path="asticle-users",
            )
            pages["Администрирование"] = [users_page]

    page = st.navigation(pages, position="sidebar")
    page.run()


if __name__ == "__main__":
    main()
