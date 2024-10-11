"""Algorihtms that related to search."""
import os

def search_by_text(query: str, top_k: int, vector_store) -> dict:
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

    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths
    }


def search_by_image(vid_name: str, top_k: int, vector_store): 
    """
    Searches for images related to a given text query using a vector store.

    Args:
        vid_name (str): Index of video in the database.
        top_k (int): The number of top results to return.
        vector_store: The vector store object to use for searching.

    Returns:
        dict: A dictionary containing the search results:
            - scores (list): A list of similarity scores for each retrieved image.
            - idx_image (list): A list of indices corresponding to the retrieved images.
            - infos_query (list): A list of filenames (without path) associated with the query.
            - image_paths (list): A list of filenames (without path) associated with the retrieved images.

    Example: 
        ```
        vid_name = 'L07_V014, 17489'
        K_neighbors = 100
        high_performance = 1


        root_img = '/kaggle/input/aic2024-extracted-data/s_optimized_keyframes/'
        image_path = os.path.join(root_img, '-'.join(vid_name.split(', ')) + '.webp')
        scores, idx_image, infos_query, image_paths = faiss_search[high_performance].image_similarity_search(image_path, k=K_neighbors)
        faiss_search[high_performance].show_images(image_paths)
        print(scores)
        ```
    """
    root_img = "./s_optimized_keyframes/"
    image_path = os.path.join(root_img, '-'.join(vid_name.split(', ')) + '.webp')
    scores, idx_image, infos_query, image_paths = vector_store.image_similarity_search(image_path, top_k)

    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths
    }

def search_by_image_online(img_path: str, top_k: int, vector_store): 
    """
    Searches for images related to a given text query using a vector store.

    Args:
        vid_name (str): Index of video in the database.
        top_k (int): The number of top results to return.
        vector_store: The vector store object to use for searching.

    Returns:
        dict: A dictionary containing the search results:
            - scores (list): A list of similarity scores for each retrieved image.
            - idx_image (list): A list of indices corresponding to the retrieved images.
            - infos_query (list): A list of filenames (without path) associated with the query.
            - image_paths (list): A list of filenames (without path) associated with the retrieved images.

    Example: 
        ```
        vid_name = 'L07_V014, 17489'
        K_neighbors = 100
        high_performance = 1


        root_img = '/kaggle/input/aic2024-extracted-data/s_optimized_keyframes/'
        image_path = os.path.join(root_img, '-'.join(vid_name.split(', ')) + '.webp')
        scores, idx_image, infos_query, image_paths = faiss_search[high_performance].image_similarity_search(image_path, k=K_neighbors)
        faiss_search[high_performance].show_images(image_paths)
        print(scores)
        ```
    """
    scores, idx_image, infos_query, image_paths = vector_store.image_similarity_search(img_path, top_k, online=True)

    infos_query = [info.split('/')[-1] for info in infos_query]
    image_paths = [image_path.split('/')[-1] for image_path in image_paths]

    return {
        'scores': scores.tolist(),
        'idx_image': idx_image.tolist(),
        'infos_query': infos_query, 
        'image_paths': image_paths
    }
