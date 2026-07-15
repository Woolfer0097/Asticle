import streamlit as st
from auth.state import is_authenticated, is_admin


def header():
    header = st.container(
        height=120,
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
    )
    header.subheader("Asticle Articles", width=235)

    if header.button("Список статей"):
        st.switch_page("pages/articles.py")

    if header.button("Избранное"):
        if is_authenticated():
            st.switch_page("pages/favourites.py")
        else:
            st.switch_page("pages/noregistration.py")

    if header.button("Профиль"):
        if is_authenticated():
            st.switch_page("pages/profile.py")
        else:
            st.switch_page("pages/noregistration.py")

    if is_authenticated():
        if is_admin():
            if header.button("Админка"):
                st.switch_page("pages/admin/admin.py")
