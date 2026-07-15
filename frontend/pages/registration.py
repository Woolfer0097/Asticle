import requests
import streamlit as st

from api.client import get_error_message, register

from patterns.header import header

header()


st.title("Регистрация")

with st.form("registration_form"):
    nickname = st.text_input("Никнейм", key="registration_nickname")
    email = st.text_input("Почта", key="registration_email")
    password = st.text_input(
        "Пароль",
        type="password",
        key="registration_password",
    )
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not nickname.strip() or not email.strip() or not password:
        st.error("Заполните все поля.")
        st.stop()

    try:
        response = register(
            nickname=nickname.strip(),
            email=email.strip(),
            password=password,
        )
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Регистрация выполнена. Теперь войдите в аккаунт.")
        st.switch_page("pages/login.py")
    else:
        st.error(get_error_message(response))

st.page_link("pages/login.py", label="Уже есть аккаунт? Войти")
