from typing import Any

import requests
import streamlit as st

from config import REQUEST_TIMEOUT, get_backend_url


def endpoint(path: str) -> str:
    return f"{get_backend_url()}{path}"


def media_url(path: str | None) -> str | None:
    if not path:
        return None
    if path.startswith(("http://", "https://")):
        return path
    return endpoint(path if path.startswith("/") else f"/{path}")


def api_request(
    method: str,
    path: str,
    *,
    token: str | None = None,
    **kwargs: Any,
) -> requests.Response:
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return requests.request(
        method,
        endpoint(path),
        headers=headers,
        timeout=REQUEST_TIMEOUT,
        **kwargs,
    )


def error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
    except ValueError:
        return f"Backend вернул HTTP {response.status_code}"

    if isinstance(detail, list):
        return "; ".join(item.get("msg", str(item)) for item in detail)

    return str(detail or f"Backend вернул HTTP {response.status_code}")


def read_json(response: requests.Response, fallback: Any) -> Any:
    try:
        return response.json()
    except ValueError:
        return fallback


def _session_token() -> str | None:
    return st.session_state.get("token")


def _legacy_article_content(extra: dict[str, Any]) -> str:
    fields = [
        ("Фото", extra.get("photo_path")),
        ("Здоровье", extra.get("health")),
        ("Урон", extra.get("damage")),
        ("Бронирование", extra.get("armor")),
        ("История", extra.get("history")),
        ("Рекомендация", extra.get("recommendation")),
        ("Тип", extra.get("category")),
        ("Нация", extra.get("nation")),
        ("Уровень", extra.get("level")),
    ]
    return "\n".join(f"{label}: {value}" for label, value in fields if value)


def register(alias: str, email: str, password: str) -> requests.Response:
    return api_request(
        "POST",
        "/auth/register",
        json={"alias": alias, "email": email, "password": password},
    )


def login(email: str, password: str) -> requests.Response:
    return api_request(
        "POST",
        "/auth/login",
        json={"email": email, "password": password},
    )


def get_profile(token: str) -> requests.Response:
    return api_request("GET", "/users/me", token=token)


def get_users(token: str) -> requests.Response:
    return api_request("GET", "/users/", token=token)


def get_articles() -> requests.Response:
    return api_request("GET", "/articles/")


def get_article(article_id: int) -> requests.Response:
    return api_request("GET", f"/articles/{article_id}")


def create_article(title: str, content: str | None = None, **extra: Any) -> requests.Response:
    if content is None:
        content = _legacy_article_content(extra)

    return api_request(
        "POST",
        "/articles/",
        token=_session_token(),
        json={"title": title, "content": content},
    )


def update_article(
    article_id: int,
    title: str,
    content: str | None = None,
    **extra: Any,
) -> requests.Response:
    if content is None:
        content = _legacy_article_content(extra)

    return api_request(
        "PATCH",
        f"/articles/{article_id}",
        token=_session_token(),
        json={"title": title, "content": content},
    )


def delete_article(article_id: int) -> requests.Response:
    return api_request("DELETE", f"/articles/{article_id}", token=_session_token())


def upload_article_cover(article_id: int, uploaded_file: Any) -> requests.Response:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream",
        )
    }
    return api_request(
        "POST",
        f"/articles/{article_id}/photo",
        token=_session_token(),
        files=files,
    )


def get_favourites(token: str | None = None) -> requests.Response:
    token = token or _session_token()
    return api_request("GET", "/favourites/", token=token)


def add_favourite(token: str | int, article_id: int | None = None) -> requests.Response:
    if article_id is None:
        article_id = int(token)
        token = _session_token() or ""

    return api_request("POST", f"/favourites/{article_id}", token=token)


def remove_favourite(token: str | int, article_id: int | None = None) -> requests.Response:
    if article_id is None:
        article_id = int(token)
        token = _session_token() or ""

    return api_request("DELETE", f"/favourites/{article_id}", token=token)


def get_error_message(response: requests.Response) -> str:
    return error_message(response)


def get_my_user() -> requests.Response:
    return api_request("GET", "/users/me", token=_session_token())


def get_all_users() -> requests.Response:
    return api_request("GET", "/users/", token=_session_token())


def get_favourite_by_article_id(article_id: int) -> requests.Response:
    response = requests.Response()
    favourites_response = get_favourites()

    if not favourites_response.ok:
        response.status_code = favourites_response.status_code
        return response

    favourite_ids = {
        item.get("article_id")
        for item in read_json(favourites_response, [])
    }
    response.status_code = 200 if article_id in favourite_ids else 404
    return response
