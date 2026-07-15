import requests
import streamlit as st

from patterns.header import header
from api.client import get_error_message, create_article

header()
st.title("Добавление статьи")

with st.form("create_article_form"):
    title = st.text_input("Название статьи", key="title")
    photo_path = st.text_input("Фото статьи", key="photo_path", value="-")
    health = st.text_input("Здоровье статьи", key="health", value="-")
    damage = st.text_input("Урон статьи", key="damage", value="-")
    armor = st.text_input("Бронирование статьи", key="armor", value="-")
    history = st.text_input(
        "Историческая справка о статье",
        key="history",
        value="Историческая справка о данном статье отсутствует",
    )
    recommendation = st.text_input(
        "Рекомендация по игре на статье",
        key="recommendation",
        value="Рекомендации по игре на данном статье отсутстуют",
    )
    category = st.text_input("Тип статьи", key="category")
    nation = st.text_input("Нация статьи", key="nation")
    level = st.text_input("Уровень статьи", key="level")

    submitted = st.form_submit_button("Добавить статью")

if submitted:
    if (
        not title.strip()
        or not category.strip()
        or not nation.strip()
        or not level.strip()
    ):
        st.error(
            "Заполните обязательно поля: Название статьи, Тип статьи, Нация статьи, Уровень статьи."
        )
        st.stop()

    try:
        response = create_article(
            title=title.strip(),
            photo_path=photo_path.strip(),
            health=health.strip(),
            damage=damage.strip(),
            armor=armor.strip(),
            history=history.strip(),
            recommendation=recommendation.strip(),
            category=category.strip(),
            nation=nation.strip(),
            level=level.strip(),
        )
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Статья успешно добавлен")
        st.switch_page("pages/articles.py")
    else:
        st.error(get_error_message(response))
