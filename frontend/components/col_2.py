import json

import streamlit as st

from api.base import setup_url
# from url import (BACKEND_URL_SEARCH_IMAGE, BACKEND_URL_SEARCH_OCR,
#                  BACKEND_URL_GET_IMAGE, BACKEND_URL_GET_VIDEO_METADATA)
from api.search import get_image, search_image_by_text


def setup_column_2():
    (
        BACKEND_URL,
        BACKEND_URL_GET_IMAGE,
        BACKEND_URL_GET_VIDEO_METADATA,
        BACKEND_URL_SEARCH_IMAGE,
        BACKEND_URL_SEARCH_OCR,
    ) = setup_url(st.session_state["url"])
    # ------------------------------ #
    #    Added Slider and Checkbox   #
    # ------------------------------ #

    tab1, tab2 = st.tabs(["Sentence-based search", "OCR-based search"])

    with tab1:
        with st.expander("Settings"):
            # Slider for K_neighbors
            K_neighbors = st.slider(
                "Number of Neighbors (K_neighbors)",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Adjust the number of nearest neighbors to retrieve.",
                key="text_search",
            )
            st.session_state["top_k"] = K_neighbors

            # Checkbox for high_performance
            embed_model_list = ["BLIP", "BLIP_DES", "BLIP_FCT", "CLIP"]
            high_performance = st.radio(
                "You can choose CLIP-based or BLIP-based",
                embed_model_list,
                index=embed_model_list.index("BLIP"),
            ).lower()
            print(high_performance)
            st.session_state["high_performance"] = high_performance

            smart_query = st.toggle("Extend query with LLM")
            st.session_state['smart_query'] = smart_query
        # Search bar
        text_query = st.text_input(
            "Enter a text query, a frame or an image url",
            placeholder='Eg: "Cảnh quay một chiếc thuyền cứu hộ đi trên băng..." || "L01_V001, 1" || "https://bitexco.c...scaled.jpg"',
            key="text_query_for_text_search",
        )

        search_clicked = st.button("Search", key="text_search_button")

        if search_clicked and text_query:
            with st.spinner("Performing search..."):
                data = {
                    "query": text_query,
                    "top_k": st.session_state["top_k"],
                    "high_performance": st.session_state["high_performance"],
                    "smart_query": st.session_state["smart_query"]
                }

                try:
                    response = search_image_by_text(
                        url=BACKEND_URL_SEARCH_IMAGE, data=data
                    )
                    # Store results in session_state
                    st.session_state["search_results"] = response

                    # Reset checkbox states for new search
                    st.session_state["checkbox_states"] = {}
                    # Reset selected_images for new search
                    st.session_state["selected_images"] = {}
                except Exception as e:
                    st.error(e)

    with tab2:
        with st.expander("Settings"):
            # Slider for K_neighbors
            K_neighbors = st.slider(
                "Number of Neighbors (K_neighbors)",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Adjust the number of nearest neighbors to retrieve.",
                key="ocr_search",
            )
            st.session_state["top_k"] = K_neighbors

            mode = st.slider(
                "Mode of algorithm",
                min_value=0,
                max_value=7,
                step=1,
                help="Adjust mode the change the fuzzy matching algorithm.",
                key="ocr_search_fuzzy_matching",
            )
            st.session_state["mode"] = mode
        # Search bar
        text_query = st.text_input(
            "Enter a keyword",
            placeholder='Eg: "Cảnh quay một chiếc thuyền cứu hộ đi trên băng..." || "L01_V001, 1" || "https://bitexco.c...scaled.jpg"',
            key="text_query_for_ocr_serch",
        )

        search_clicked = st.button("Search", key="ocr_search_button")

        if search_clicked and text_query:
            with st.spinner("Performing search..."):

                data = {
                    "query": text_query,
                    "top_k": st.session_state["top_k"],
                    "mode": st.session_state["mode"],
                }

                try:
                    response = search_image_by_text(
                        url=BACKEND_URL_SEARCH_OCR, data=data
                    )
                    # Store results in session_state
                    st.session_state["search_results"] = response

                    # Reset checkbox states for new search
                    st.session_state["checkbox_states"] = {}
                    # Reset selected_images for new search
                    st.session_state["selected_images"] = {}
                except Exception as e:
                    st.error(e)

    # Display images from session_state if available
    if st.session_state.get("search_results"):
        # Ensure image_id is unique by adding row and column indices
        num_cols = 4  # Adjust as needed
        response = st.session_state.get("search_results")

        image_paths = response["image_paths"]
        vid_urls = response["vid_urls"]
        frames = response["frames"]
        rows = [
            image_paths[i : i + num_cols] for i in range(0, len(image_paths), num_cols)
        ]

        for row_idx, row in enumerate(rows):
            cols = st.columns(len(row))
            print(row)
            for idx, img_path in enumerate(row):
                vid_id = img_path.split(".")[
                    0
                ]  # Sample of infos_query: L22_V027-30543.webp
                print(vid_id)
                vid_name, frame = vid_id.split("-")

                # Ensure image_id is unique by adding row and column indices
                image_id = f"{vid_name}_{frames[row_idx]}_{row_idx}_{idx}"
                checkbox_key = f"checkbox_{image_id}"

                # Initialize checkbox state if not present
                if image_id not in st.session_state["checkbox_states"]:
                    st.session_state["checkbox_states"][image_id] = False

                with cols[idx]:
                    # Each iframe component
                    try:
                        # print(infos_query[row_idx])
                        st.image(
                            get_image(url=BACKEND_URL_GET_IMAGE, image_idx=img_path),
                        )  # Set fixed width
                    except Exception as e:
                        st.error(f"Error loading image: {e}")

                    # Center the button and checkbox using HTML and CSS
                    st.markdown(
                        f"""
                        <div style="display:flex; flex-direction: column; align-items: center; border: white;
                        border-radius:77%">
                        """,
                        unsafe_allow_html=True,
                    )

                    # Define the callback function
                    def button_callback(
                        vid_name=vid_name,
                        frame=frame,
                        video_url=vid_urls[row_idx],
                        button_label=f"{vid_name}, {frame}",
                    ):
                        st.session_state["expander_content"] = (
                            vid_name,
                            frame,
                            video_url,
                        )
                        st.session_state["copy_to_clipboard"] = button_label

                    st.button(
                        f"{vid_name}, {frame}",
                        key=f"btn_{image_id}",
                        on_click=button_callback,
                    )

                    # Checkbox for selection
                    selected = st.checkbox("Select", key=checkbox_key)
                    st.session_state["checkbox_states"][image_id] = selected

                    # Update selected_images
                    if selected:
                        # st.session_state['selected_images'][image_id] = (vid_name, frame, img_path)
                        info_query = f"{vid_name}-{frame}.webp"
                        st.session_state["selected_images"][image_id] = (
                            vid_name,
                            frame,
                            info_query,
                        )
                    else:
                        st.session_state["selected_images"].pop(image_id, None)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True,
                    )
