import requests
import streamlit as st

from api.client import error_message, login, register
from auth.state import clear_auth, current_profile, is_authenticated, load_profile, save_token
from ui.layout import render_header


def render_auth() -> None:
    render_header()

    if is_authenticated():
        profile = current_profile() or load_profile()
        if profile:
            st.subheader("Профиль")
            st.write(f"**Алиас:** {profile.get('alias')}")
            st.write(f"**Почта:** {profile.get('email')}")
            st.write(f"**Роль:** {profile.get('role')}")
            st.write(f"**Активен:** {'да' if profile.get('is_active') else 'нет'}")
        if st.button("Выйти из аккаунта", type="primary"):
            clear_auth()
            st.rerun()
        return

    st.markdown(
        '<div class="note">Авторизация нужна только для избранного и просмотра профиля. Каталог доступен без входа.</div>',
        unsafe_allow_html=True,
    )
    login_tab, register_tab = st.tabs(["Вход", "Регистрация"])

    with login_tab:
        render_login_form()

    with register_tab:
        render_register_form()


def render_login_form() -> None:
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Пароль", type="password", key="login_password")
        submitted = st.form_submit_button("Войти", type="primary")

    if not submitted:
        return

    if not email.strip() or not password:
        st.error("Введите email и пароль.")
        return

    try:
        response = login(email.strip(), password)
    except requests.RequestException:
        st.error("Backend недоступен.")
        return

    if not response.ok:
        st.error(error_message(response))
        return

    token = response.json().get("access_token")
    if not token:
        st.error("Backend не вернул access_token.")
        return

    save_token(token)
    load_profile(show_errors=True)
    st.success("Вход выполнен.")
    st.rerun()


def render_register_form() -> None:
    with st.form("register_form"):
        alias = st.text_input("Псевдоним", key="register_alias")
        email = st.text_input("Email", key="register_email")
        password = st.text_input(
            "Пароль",
            type="password",
            key="register_password",
            help="Минимум 6 символов.",
        )
        submitted = st.form_submit_button("Зарегистрироваться", type="primary")

    if not submitted:
        return

    alias = alias.strip()
    email = email.strip()

    if not alias or not email or not password:
        st.error("Заполните все поля.")
        return

    try:
        response = register(alias, email, password)
    except requests.RequestException:
        st.error("Backend недоступен.")
        return

    if response.ok:
        st.success("Аккаунт создан. Теперь войдите.")
    else:
        st.error(error_message(response))
