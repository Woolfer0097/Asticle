import streamlit as st
from streamlit_cookies_controller import CookieController

CONTROLLER_KEY = "asticle_cookies"


def get_cookie_controller(*, writable: bool = False) -> CookieController:
    controller = CookieController(key=CONTROLLER_KEY)
    if isinstance(controller.getAll(), dict):
        return controller

    st.session_state.pop(CONTROLLER_KEY, None)

    if not writable:
        return controller

    st.session_state[CONTROLLER_KEY] = {}
    return CookieController(key=CONTROLLER_KEY)


def get_cookie(name: str):
    controller = get_cookie_controller()
    cookies = controller.getAll()
    if not isinstance(cookies, dict):
        return None

    return cookies.get(name)


def set_cookie(name: str, value, **kwargs) -> None:
    get_cookie_controller(writable=True).set(name, value, **kwargs)


def remove_cookie(name: str) -> None:
    controller = get_cookie_controller(writable=True)
    if controller.get(name) is not None:
        controller.remove(name)
