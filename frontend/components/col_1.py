import streamlit as st 

# Video Details Expander
def setup_column_1():
    video_details_expander = st.expander("Video details")
    with video_details_expander:
        if st.session_state['expander_content']:
            vid_name, frame, video_url = st.session_state['expander_content']
            st.video(video_url)
            st.write(f"**Video ID:** {vid_name}, {frame}")
            st.write(f"**Video URL:** {video_url}")

            # Checkbox in video details
            image_id = f"{vid_name}_{frame}"
            checkbox_key = f"checkbox_{image_id}"
            if image_id not in st.session_state['checkbox_states']:
                st.session_state['checkbox_states'][image_id] = False

            selected = st.checkbox("Select", key=checkbox_key)
            st.session_state['checkbox_states'][image_id] = selected

            # Update selected_images
            if selected:
                # Find img_path from id2img_fps
                # img_path = None
                # for path in id2img_fps.values():
                #     if image_id in path:
                #         img_path = path
                #         break
                info_query = f"{vid_name}-frame.webp"
                st.session_state['selected_images'][image_id] = (vid_name, frame, info_query)
            else:
                st.session_state['selected_images'].pop(image_id, None)
        else:
            st.write("No video selected.")

    # Selected Images Expander
    selected_images_expander = st.expander("Selected image(s)")
    with selected_images_expander:
        selected_images = st.session_state['selected_images'].values()
        if selected_images:
            for vid_name, frame, img_path in selected_images:
                st.write(f"**{vid_name}, {frame}**")
        else:
            st.write("No images selected.")
