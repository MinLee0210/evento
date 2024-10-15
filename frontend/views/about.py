import pathlib
import streamlit as st


def read_markdown_file(markdown_file):
    return pathlib.Path(markdown_file).read_text()


# ----- Sidebar -----
st.sidebar.write("App created by AIO_TOP10")

# ----- Main content -----
st.markdown("""
    <h1 style='text-align: center;'>About us</h1>
    """, unsafe_allow_html=True)

markdown_file = './assets/about_us.md'
intro_markdown = read_markdown_file(markdown_file)
st.markdown(intro_markdown, unsafe_allow_html=True)




