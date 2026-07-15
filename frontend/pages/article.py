import requests
import streamlit as st

from api.client import get_error_message, get_article

from patterns.header import header
from patterns.article import render_favorite_button

header()

article_id = st.session_state.get("selected_article_id")

if article_id is None:
    st.info("Сначала выберите запись в списке.")
    st.page_link("pages/articles.py", label="Перейти в список")
    st.stop()

try:
    response = get_article(article_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

article = response.json()
left, right = st.columns(2, vertical_alignment="center")

if article.get("photo_path") == "-":
    left.info("Изображение не добавлено")
else:
    left.image(article.get("photo_path"), use_container_width=True)

col_info, col_favourite = right.columns(2, vertical_alignment="center")
col_info.title(article.get("title"))
col_info.write(f"Уровень: {article.get('level')}")
col_info.write(f"Тип: {article.get('category')}")
col_info.write(f"Нация: {article.get('nation')}")
col_info.write(f"Здоровье: {article.get('health')}")
col_info.write(f"Урон: {article.get('damage')}")
col_info.write(f"Бронирование: {article.get('armor')}")

with col_favourite:
    render_favorite_button(article, key_prefix="details")

st.subheader("Историческая справка")
st.write(article.get("history"))

st.subheader("Рекомендации")
st.write(article.get("recommendation"))
