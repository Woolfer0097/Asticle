import requests
import streamlit as st

from api.client import get_error_message, login, get_my_user
from auth.state import clear_auth, is_authenticated, save_auth

from patterns.header import header
from patterns.cookie import controller

header()

st.title("Вход")

if is_authenticated():
    st.info("Вы уже вошли в аккаунт.")
    st.page_link("pages/profile.py", label="Открыть профиль")
    st.stop()

with st.form("login_form"):
    email = st.text_input("Почта", key="login_email")
    password = st.text_input(
        "Пароль",
        type="password",
        key="login_password",
    )
    submitted = st.form_submit_button("Войти")

if submitted:
    if not email.strip() or not password:
        st.error("Введите почту и пароль.")
        st.stop()

    try:
        login_response = login(email.strip(), password)
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if not login_response.ok:
        st.error(get_error_message(login_response))
        st.stop()

    access_token = login_response.json().get("access_token")

    if not access_token:
        st.error("Backend не вернул access_token.")
        st.stop()

    controller.set("access_token", access_token)

    try:
        profile_response = get_my_user()
    except requests.RequestException:
        clear_auth()
        st.error("Не удалось получить избранные пользователя.")
        st.stop()

    if not profile_response.ok:
        error_message = get_error_message(profile_response)
        clear_auth()
        st.error(error_message)
        st.stop()

    save_auth(access_token, profile_response.json())
    st.success("Вход выполнен.")
    st.switch_page("pages/profile.py")

st.page_link("pages/registration.py", label="Нет аккаунта? Зарегистрироваться")
