import streamlit as st


def setup_banner():
    custom_html = """
<div class="banner">
    <img src="https://aichallenge.hochiminhcity.gov.vn/documents/20142/2098060/AIC2024-Banner+website.png/9f28317e-8852-54b9-eb3d-7401c31f1a44?t=1719482873995" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""
    # Display the custom HTML
    st.components.v1.html(custom_html)
