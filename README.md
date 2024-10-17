<p align="center">
  <img src="./docs/AIC2024-Banner website.png" width="1080">
</p>

<h1 align="center"> ⚡️ evento </h1>


<p align="center">
  <em>Joining forces with innovators and AI enthusiasts, this project is a dynamic collaboration aimed at crafting a cutting-edge event-retrieval system, proudly participating in the Ho Chi Minh AI Challenge 2024.</em>
</p>



  ![Static Badge](https://img.shields.io/badge/python->=3.10-blue)
  ![Static Badge](https://img.shields.io/badge/fastapi-0.115.2-blue)
  ![Static Badge](https://img.shields.io/badge/streamlit-1.38.0-blue)
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>

- [📍 Overview](#-overview)
- [🎯 Features](#-feature)
- [🤖 Tech Stack](#-technologies-used)
- [🚀 Usage](#-usage)
- [📋 API](#-api)
- [🎬 Demo](#-demo)
- [👣 Workflow](#-workflow)
- [📐 App Structure](#-app-structure)
- [🧑‍💻 Contributors](#-contributors)
</details>

## 📍 Overview
Welcome to `⚡️ evento`, an ambitious collaborative project aimed at revolutionizing event retrieval through the innovative use of visual data. Our team, **AIO_TOP10**, is honored to participate in the prestigious Ho Chi Minh AI Challenge 2024, where we strive to showcase our expertise in artificial intelligence. We are committed to developing a cutting-edge, robust, and efficient event-retrieval system, leveraging the immense potential of AI to enhance information retrieval processes.


More details about the challenge refers to this [link.](https://aichallenge.hochiminhcity.gov.vn/)


## 🎯 Features

- [ x ] Multimodal search.
- [ x ] Synthetic data with a Multimodal Model. 
- [ ] Share similarity search.
- [ ] Recommendation.
 
_Note:_ We are happy to share our [trip](https://trello.com/invite/b/66c4acf531cdf8fd5c8f167e/ATTI60ab09c08943d3ba5220d47918aab2229CBAC9CF/aiotop10-evento) while developing this app. 


## 🤖 Tech Stack

### Server building

- Back-end: FastAPI. 
- Front-end: Streamlit.
- Deploy: Docker, Vercel.

### Core technology

- Keyframe-extraction: TransNetV2 + K-Means clustering.
- LLM: Gemini. 
- Embedding: CLIP, BLIP.


## 🚀 Usage

1. **Clone the repository**
```
git clone https://github.com/MinLee0210/evento.git
cd /evento
```

2. **Setup Environment**

**Download dataset from Kaggle**

We store our dataset on Kaggle. Please, download it from [here](https://www.kaggle.com/datasets/pyetsvu/aic2024-extracted-data) and compress it in `db` directory, `/backend/db`.
Additionally, we have 2 other appoaches to download. You can read the detail from [here](backend/db/README.md).

_Note:_ Currently, we do not offer an automated solution for transferring our local dataset to a database. However, we highly recommend considering MySQL for efficient data reading, MongoDB for seamless data writing, and Redis for caching high-similarity queries, a feature we refer to as 'share search'. For more insights into our share search mechanism, please refer to our comprehensive documentation (docs).

**Set API's key in backend directory**

We use Gemini's API for extracting keywords and refining queries. As a result, setting Gemini's API key is essential to run the app. We also provide a `env.template` as an example in the `backend`.


3. **Run the application**

**Run the backend**

```
# /evento

cd /backend
bash start_be.sh 
```
In case you can not run `bash`: 

1. Install requirements with `pip install -r requirements.txt`
2. Move to the `/app` and run `uvicorn main:app --host=0.0.0.0 --port=8000 --reload`.


Run the frontend

```
# /evento

cd /frontend
bash start_fe.sh 
```

In case you can not run `bash`: 

1. Install requirements with `pip install -r requirements.txt`
2. Run `streamilit run app.py`.

## 📋 API

|Method| Type | Description | 
| - | - | - |
|`/`| `GET` |  Get a random quote. Just for checking basic connection between frontend and backend. | 
| `/search` | `POST` | Search by text. |
| `/search/ocr` | `POST` | Search by fuzzy matching between extracted keywords and OCR-based extraced data.  |
| `/search/image/{image_idx}` | `GET` | Get image by `image_idx`. |
| `/search/video/{vid_idx}` | `GET` | Get video metadata by `vid_idx`. |

_Note:_ Detail about how to get response after running the app successfully is in [notebook](./docs/notebooks/dev_search_text_api.ipynb)


## 🎬 Demo

- **Galleries**


- **Videos**


## 👣 Workflow




## 📐 App Structure
```
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   └── v1
│   │   │       └── query_refine
│   │   ├── components
│   │   │   ├── embedding
│   │   │   ├── fuzzymatching
│   │   │   ├── kfe
│   │   │   ├── llms
│   │   │   └── translation
│   │   ├── core
│   │   ├── routes
│   │   ├── schema
│   │   ├── services
│   │   └── utils
│   ├── db
│   │   ├── features
│   │   ├── media-info
│   │   ├── objects
│   │   └── s_optimized_keyframes
│   ├── experimental
│   │   └── recommender
│   └── test
│       ├── api                               # Testing logic of defined business's API.
│       └── unit                              # Testing each components.
├── docs
│   ├── notebooks
│   └── test_query
├── frontend
│   ├── api
│   ├── assets
│   ├── components
│   └── views
└── scripts
```


## 🧑‍💻 Contributors

Thanks to the following amazing individuals who have contributed to this project:
* [Lê Đức Minh](https://github.com/MinLee0210)
* [Phạm Ngọc Huyền](https://www.facebook.com/ngochuyenpham.99)
* [Vũ Hoàng Phát](https://github.com/paultonsdee)
* [Trần Nguyễn Vân Anh](https://www.facebook.com/vananh.trannguyen.54584)
* [Phạm Nguyễn Quốc Huy](https://github.com/kidneyflowerSE)