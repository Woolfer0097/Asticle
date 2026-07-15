import requests
import streamlit as st

from api.client import get_error_message, get_all_users

from patterns.user import render_user_card
from patterns.header import header

header()

st.title("Пользователи")

try:
    response = get_all_users()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

users = response.json()

if not users:
    st.info("Пользователи отсутствуют")
    st.stop()

for user in users:
    render_user_card(user)
