import json


def search(client, path="/search/", **body):
    response = client.post(path, json={"top_k": 3, **body})
    assert response.status_code == 200, response.text
    return response.json()["hits"]


def test_health(client):
    assert client.get("/").json() == {"status": "ok"}


def test_text_search_ranks_and_builds_video_url(client):
    hits = search(client, query="keyframe 2")
    assert hits[0] == {
        "image": "L01_V002-00030.webp",
        "video": "L01_V002",
        "frame": 30,
        "url": "https://yt/watch?v=b&t=1",
        "score": 1.0,
    }
    assert len(hits) == 3


def test_smart_query_without_api_key_falls_back_to_plain(client):
    assert search(client, query="keyframe 1", smart_query="Explore")[0]["frame"] == 120


def test_frame_reference_searches_by_closest_keyframe_in_shot(client):
    assert search(client, query="L01_V001, 150")[0]["image"] == "L01_V001-00120.webp"
    assert search(client, query="L01_V001,5")[0]["image"] == "L01_V001-00010.webp"


def test_frame_reference_outside_any_shot_is_404(client):
    assert client.post("/search/", json={"query": "L01_V002, 500"}).status_code == 404


def test_json_encoded_string_body_is_accepted(client):
    body = json.dumps({"query": "keyframe 0", "top_k": 1})
    response = client.post("/search/", json=body)
    assert response.status_code == 200
    assert response.json()["hits"][0]["image"] == "L01_V001-00010.webp"


def test_invalid_request_is_rejected(client):
    assert client.post("/search/", json={"query": "x", "top_k": 0}).status_code == 422
    assert client.post("/search/", json={"query": ""}).status_code == 422
    assert client.post("/search/ocr", json={"query": "x", "mode": 8}).status_code == 422


def test_ocr_search(client):
    hits = search(client, "/search/ocr", query="football")
    assert hits[0]["image"] == "L01_V002-00030.webp"
    assert all(hit["image"] != "L01_V001-00120.webp" for hit in hits)  # no OCR text


def test_get_image_and_video(client):
    assert client.get("/search/image/L01_V001-00010.webp").headers["content-type"] == "image/webp"
    assert client.get("/search/image/..%2F..%2Fkeyframes.csv").status_code == 404
    assert client.get("/search/video/L01_V001").json() == {"title": "News"}
    assert client.get("/search/video/L09_V999").status_code == 404
