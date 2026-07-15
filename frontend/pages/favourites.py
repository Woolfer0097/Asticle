import requests
import streamlit as st

from api.client import get_error_message, get_favourites, get_article

from patterns.article import render_article_card
from patterns.header import header

from patterns.cookie import controller

header()

st.title("Избранное")

try:
    response = get_favourites()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

favourites = response.json()

if not favourites:
    st.info("В избранном пока ничего нет.")
    st.stop()

for favourite in favourites:
    article_id = favourite.get("article_id")
    article = get_article(article_id).json()
    render_article_card(article)
