from streamlit_cookies_controller import CookieController

CONTROLLER_KEY = "asticle_cookies"


def get_cookie_controller() -> CookieController:
    return CookieController(key=CONTROLLER_KEY)


def get_cookie(name: str):
    return get_cookie_controller().get(name)


def set_cookie(name: str, value, **kwargs) -> None:
    get_cookie_controller().set(name, value, **kwargs)


def remove_cookie(name: str) -> None:
    controller = get_cookie_controller()
    if controller.get(name) is not None:
        controller.remove(name)
