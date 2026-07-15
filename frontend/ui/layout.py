import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <div class="brand">
            <h1>Asticle</h1>
            <p>Редакционный каталог статей с обложками, избранным и быстрым управлением материалами через FastAPI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
