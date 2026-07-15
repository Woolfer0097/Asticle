import requests
import streamlit as st

from api.client import get_error_message, get_articles

from patterns.article import render_article_card
from patterns.header import header

header()

st.title("Список статей")

try:
    response = get_articles()
except requests.RequestException:
    st.error("Backend недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

articles = response.json()

if not articles:
    st.info("В каталоге пока нет записей.")
    st.stop()

columns = st.columns(4)

for index, article in enumerate(articles):
    with columns[index % 4]:
        render_article_card(article)
