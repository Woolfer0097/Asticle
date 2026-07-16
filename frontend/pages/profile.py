import requests
import streamlit as st

from api.client import get_error_message, get_my_user
from auth.state import clear_auth, get_token, save_auth

from patterns.header import header

header()

st.title("Профиль")

try:
    response = get_my_user()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

profile = response.json()
token = get_token()
if token:
    save_auth(token, profile)

st.write(f"**Никнейм:** {profile.get('nickname', 'Не указано')}")
st.write(f"**Почта:** {profile.get('email', 'Не указана')}")
st.write(f"**Роль:** {profile.get('role', 'user')}")

if st.button("Выйти", type="primary"):
    clear_auth()
    st.switch_page("pages/login.py")
