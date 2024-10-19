"""Algorihtms that related to search."""

import json
import os

from components.llms.prompts import EXTRACT_KEYWORDS


def search_by_text(
    query: str, top_k: int, vector_store, vid_url: dict, url_fps: dict
) -> dict:
    """
    Searches for images related to a given text query using a vector store.
    """
    scores, idx_image, infos_query, image_paths = vector_store.text_search(query, top_k)
    vid_urls = []
    # embed_urls = []
    frames = []
    infos_query = [info.split("/")[-1] for info in infos_query]
    image_paths = [image_path.split("/")[-1] for image_path in image_paths]
    for img_id in image_paths:
        vid_id = img_id.split(".")[0]
        vid_name, frame = vid_id.split("-")
        url = (
            vid_url[vid_name]
            + "&t="
            + str(int(int(frame) / url_fps[vid_url[vid_name]]))
        )
        # embed_url = vid_url[vid_name].replace('watch?v=', 'embed/') # TODO: make this execuate from frontend
        vid_urls.append(url)
        # embed_urls.append(embed_url)
        frames.append(frame)

    return {
        "scores": scores.tolist(),
        "idx_image": idx_image.tolist(),
        "infos_query": infos_query,
        "image_paths": image_paths,
        "vid_urls": vid_urls,
        # 'embed_urls': embed_urls,
        "frames": frames,
    }


def search_by_image(img_path: str, top_k: int, vector_store, vid_url, url_fps, online:bool=False):
    """
    Searches for online images related to a given text query using a vector store.
    """
    scores, idx_image, infos_query, image_paths = vector_store.image_similarity_search(
        img_path, top_k, online=online
    )
    vid_urls = []
    # embed_urls = []
    frames = []
    infos_query = [info.split("/")[-1] for info in infos_query]
    image_paths = [image_path.split("/")[-1] for image_path in image_paths]
    for img_id in image_paths:
        vid_id = img_id.split(".")[0]
        vid_name, frame = vid_id.split("-")
        url = (
            vid_url[vid_name]
            + "&t="
            + str(int(int(frame) / url_fps[vid_url[vid_name]]))
        )
        # embed_url = vid_url[vid_name].replace('watch?v=', 'embed/') # TODO: make this execuate from frontend
        vid_urls.append(url)
        # embed_urls.append(embed_url)
        frames.append(frame)

    return {
        "scores": scores.tolist(),
        "idx_image": idx_image.tolist(),
        "infos_query": infos_query,
        "image_paths": image_paths,
        "vid_urls": vid_urls,
        # 'embed_urls': embed_urls,
        "frames": frames,
    }


def search_by_ocr(
    query: str, top_k, matching_tool, mode, vid_url: dict, url_fps: dict, llm=None
):
    """
    Searching by keywords using OCR.
    """

    if llm: 
        # Pick up keywords from the original query
        extract_kw_query = EXTRACT_KEYWORDS + "\n" + query
        retries = 3
        # try:
        print(query)
        keywords = llm.run(extract_kw_query)
        # print(keywords)
        # print(type(keywords))
        if isinstance(keywords, str):
            while retries >= 0:
                # Normally, it executes 2 times and break.
                keywords = json.loads(keywords)
                # print(type(keywords))
                if type(keywords) == dict or type(keywords) == list:
                    break
                retries -= 1
        keywords = [d["keyword"] for d in keywords]
    else: 
        # At this moment, keywords is only a word
        keywords = [query]

    matching_paths = []
    for kw in keywords:
        result = matching_tool.run(kw, top_k=top_k, mode=mode)
        img_paths = matching_tool.get_image_paths(result)
        matching_paths += img_paths

    # Filtering out same result
    matching_paths = list(set(matching_paths))
    vid_urls = []
    # embed_urls = []
    frames = []
    # image_paths = [image_path.split('/')[-1] for image_path in matching_paths]
    for img_id in matching_paths:
        vid_id = img_id.split(".")[0]
        vid_name, frame = vid_id.split("-")
        url = (
            vid_url[vid_name]
            + "&t="
            + str(int(int(frame) / url_fps[vid_url[vid_name]]))
        )
        # embed_url = vid_url[vid_name].replace('watch?v=', 'embed/') # TODO: make this execuate from frontend
        vid_urls.append(url)
        # embed_urls.append(embed_url)
        frames.append(frame)
    return {
        "image_paths": matching_paths,
        "vid_urls": vid_urls,
        # 'embed_urls': embed_urls,
        "frames": frames,
    }


def get_video_metadata(vid_idx, media_dir):
    if ".json" not in vid_idx:
        vid_idx = ".".join([vid_idx, "json"])  # File is in .json format
    vid_metadata = json.loads(open(os.path.join(media_dir, vid_idx), "r").read())
    return vid_metadata
