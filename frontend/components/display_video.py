import streamlit as st


from api.search import get_video_metadata

@st.dialog("Video Detail")
def render_video_iframe(url, vid_idx, vid_url): 
    response = get_video_metadata(url, vid_idx)

    # Get variables
    title = response.get('title')
    author = response.get('title')
    description = response.get('description')
    full_vid_url = response.get('watch_url')

    # Setup layout
    st.video(vid_url)
    st.write(f"**Title:** {title}")
    st.write(f"**Author:** {author}")
    st.write(f"**Description:** {description}")
    st.write(f"**Relevant Frame Video URL:** {vid_url}")
    st.write(f"**Full Video URL:** {full_vid_url}")