import streamlit as st

from patterns.header import header

header()
st.title("Добро пожаловать в админку!")

st.subheader("Статьи")
if st.button("Добавить статью"):
    st.switch_page("pages/admin/create_article.py")

if st.button("Редактировать статью"):
    st.switch_page("pages/admin/edit_articles.py")

st.subheader("Пользователи")
if st.button("Посмотреть всех пользователей"):
    st.switch_page("pages/admin/users.py")
