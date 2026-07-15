import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type,
        )
    }

    response = requests.post(
        f"{BACKEND_URL}/images/upload",
        files=files,
        timeout=15,
    )

    if response.ok:
        image_data = response.json()
        image_url = image_data["image_url"]

        st.success("Image uploaded")
        st.image(image_url, use_container_width=True)
        st.write(image_data["photo_path"])
    else:
        st.error(response.json().get("detail", "Upload failed"))
