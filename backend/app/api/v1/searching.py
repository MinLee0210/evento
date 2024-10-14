"""Algorihtms that related to search."""
import os

def search_by_text(query: str, top_k: int, vector_store, vid_url:dict, url_fps:dict) -> dict:
    """
    Searches for images related to a given text query using a vector store.

    Args:
        query (str): The text query to search for.
        top_k (int): The number of top results to return.
        vector_store: The vector store object to use for searching.

    Returns:
        dict: A dictionary containing the search results:
            - scores (list): A list of similarity scores for each retrieved image.
            - idx_image (list): A list of indices corresponding to the retrieved images.
            - infos_query (list): A list of filenames (without path) associated with the query.
            - image_paths (list): A list of filenames (without path) associated with the retrieved images.
    """
    scores, idx_image, infos_query, image_paths = vector_store.text_search(query, top_k)
    vid_urls = []
    # embed_urls = []
    frames = []
    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]
    for img_id in image_paths: 
        vid_id = img_id.split('.')[0]
        vid_name, frame = vid_id.split('-')
        url = vid_url[vid_name] + '&t=' + str(int(int(frame)/url_fps[vid_url[vid_name]]))
        # embed_url = vid_url[vid_name].replace('watch?v=', 'embed/') # TODO: make this execuate from frontend
        vid_urls.append(url)
        # embed_urls.append(embed_url)
        frames.append(frame)

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths,
        'vid_urls': vid_urls, 
        # 'embed_urls': embed_urls, 
        'frames': frames
    }


def search_by_image(vid_name: str, top_k: int, vector_store): 
    """
    Searches for images related to a given text query using a vector store.

    """
    root_img = "./s_optimized_keyframes/"
    image_path = os.path.join(root_img, '-'.join(vid_name.split(', ')) + '.webp')
    scores, idx_image, infos_query, image_paths = vector_store.image_similarity_search(image_path, top_k, online=False)

    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths
    }

def search_by_image_online(img_path: str, top_k: int, vector_store, vid_url:dict, url_fps:dict): 
    """
    Searches for online images related to a given text query using a vector store.
    """
    scores, idx_image, infos_query, image_paths = vector_store.image_similarity_search(img_path, top_k, online=True)
    vid_urls = []
    # embed_urls = []
    frames = []
    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]
    for img_id in image_paths: 
        vid_id = img_id.split('.')[0]
        vid_name, frame = vid_id.split('-')
        url = vid_url[vid_name] + '&t=' + str(int(int(frame)/url_fps[vid_url[vid_name]]))
        # embed_url = vid_url[vid_name].replace('watch?v=', 'embed/') # TODO: make this execuate from frontend
        vid_urls.append(url)
        # embed_urls.append(embed_url)
        frames.append(frame)

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths,
        'vid_urls': vid_urls, 
        # 'embed_urls': embed_urls, 
        'frames': frames
    }


def search_by_ocr(keyword, top_k, ocr_tool, mode): 
    """
    Searching by keywords using OCR.
    """
    