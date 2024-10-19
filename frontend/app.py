import streamlit as st

from setup_lifespan import setup_template


def main():

    setup_template()
    pg = st.navigation(
        [
            st.Page("views/main.py", title="Main", icon=":material/manage_search:"),
            st.Page("views/about.py", title="About us", icon=":material/history_edu:"),
        ]
    )
    pg.run()


if __name__ == "__main__":
    main()
