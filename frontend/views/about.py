import pathlib

import streamlit as st


def read_markdown_file(markdown_file):
    return pathlib.Path(markdown_file).read_text()


# ----- Sidebar -----
st.sidebar.write("App created by **AIO_TOP10**")

# ----- Main content -----
st.markdown(
    """
    <h1 style='text-align: center;'>About us</h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Our team of five passionate individuals has come together to revolutionize the event retrieval landscape. We are a diverse group, each bringing unique skills and expertise to the table. With a shared vision of creating an efficient and user-friendly system, we strive to make event management and retrieval a seamless experience.

    ### We are

    * [Vũ Hoàng Phát](https://github.com/paultonsdee)
    * [Lê Đức Minh](https://github.com/MinLee0210)
    * [Phạm Ngọc Huyền](https://www.facebook.com/ngochuyenpham.99)
    * [Trần Nguyễn Vân Anh](https://www.facebook.com/vananh.trannguyen.54584)
    * [Phạm Nguyễn Quốc Huy](https://github.com/kidneyflowerSE)
"""
)