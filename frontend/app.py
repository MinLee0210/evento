import streamlit as st


def main():
    st.set_page_config(layout="wide", page_title="evento", page_icon="⚡️")
    st.navigation(
        [
            st.Page("views/main.py", title="Main", icon=":material/manage_search:"),
            st.Page("views/about.py", title="About us", icon=":material/history_edu:"),
        ]
    ).run()


if __name__ == "__main__":
    main()
