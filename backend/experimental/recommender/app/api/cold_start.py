import pandas as pd
import numpy as np

def recommend_cold_start(df:pd.DataFrame, video_idx:str, n_videos:int=10, m_clusters:int=4, m_videos:int=4) -> list[str]:
    "Used at the initial state of the ResSys: overcome the cold-start"
    row = df[df['Video name'].str.endswith(f"{video_idx}")]
    selected_label = row.label.values[0]
    recommend_list = []

    # Pick n-video from high-related cluster
    selected_cluster = df[df['label'] == selected_label]
    selected_video = rand_idx = np.random.randint(0, len(selected_cluster), n_videos)
    for vid in selected_video: 
        recommend_idx = vid.split('/')[-1]
        recommend_list.append(recommend_idx)

    # Picking from m remains clusters
    while True: 
        rand_clusters = np.random.choice(selected_label, m_clusters, replace=False)
        if not np.isin(selected_label, rand_clusters): 
            break

    # Update recommend_list with items from m_clusters
    for cluster in rand_clusters: 
        selected_cluster = df[df['label'] == cluster]
        n_docs = len(selected_cluster)
        rand_idx = np.random.randint(0, n_docs, m_videos)
        for vid in selected_cluster.iloc[rand_idx, 0]:   # Only select the first row as Video name
            recommend_idx = vid.split('/')[-1]
            recommend_list.append(recommend_idx)

    
    return recommend_list