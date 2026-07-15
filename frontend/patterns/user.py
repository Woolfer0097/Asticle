import streamlit as st


def render_user_card(user: dict):
    with st.container(border=True):
        st.subheader(user.get("nickname"))
        st.write(f'Почта: {user.get("email")}')
        st.write(f'Роль: {user.get("role")}')
