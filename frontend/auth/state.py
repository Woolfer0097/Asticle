from typing import Any

import requests
import streamlit as st

from api.client import error_message, get_profile
from patterns.cookie import get_cookie, remove_cookie, set_cookie


AUTH_COOKIE = "asticle_access_token"
LEGACY_AUTH_COOKIE = "access_token"
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 30


def init_state() -> None:
    cookie_token = get_cookie(AUTH_COOKIE)
    defaults = {
        "token": cookie_token,
        "profile": None,
        "selected_article_id": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    if not st.session_state.get("token") and cookie_token:
        st.session_state["token"] = cookie_token


def get_token() -> str | None:
    token = st.session_state.get("token")
    if token:
        return token

    cookie_token = get_cookie(AUTH_COOKIE)
    if cookie_token:
        st.session_state["token"] = cookie_token
        return cookie_token

    return None


def save_token(token: str) -> None:
    st.session_state["token"] = token
    set_cookie(AUTH_COOKIE, token, max_age=AUTH_COOKIE_MAX_AGE)


def save_auth(access_token: str, profile: dict[str, Any] | None = None) -> None:
    save_token(access_token)
    if profile is not None:
        st.session_state["profile"] = profile


def clear_auth() -> None:
    st.session_state["token"] = None
    st.session_state["profile"] = None
    remove_cookie(AUTH_COOKIE)
    remove_cookie(LEGACY_AUTH_COOKIE)


def is_authenticated() -> bool:
    return bool(get_token())


def current_profile() -> dict[str, Any] | None:
    return st.session_state.get("profile")


def is_admin() -> bool:
    profile = current_profile() or {}
    return profile.get("role") == "admin"


def can_manage_article(article: dict[str, Any]) -> bool:
    profile = current_profile()
    if not profile:
        return False

    if profile.get("role") == "admin":
        return True

    return article.get("owner_id") == profile.get("id")


def load_profile(show_errors: bool = False) -> dict[str, Any] | None:
    token = get_token()
    if not token:
        return None

    try:
        response = get_profile(token)
    except requests.RequestException:
        if show_errors:
            st.error("Не удалось получить профиль. Проверьте backend.")
        return None

    if response.status_code == 401:
        clear_auth()
        return None

    if response.ok:
        profile = response.json()
        st.session_state["profile"] = profile
        return profile

    if show_errors:
        st.error(error_message(response))
    return None
