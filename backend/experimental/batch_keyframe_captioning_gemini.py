import asyncio
import google.generativeai as genai
from typing import List, Dict
from typing_extensions import TypedDict
import time
import os
import logging
import glob
import nest_asyncio

from dotenv import load_dotenv

# Áp dụng nest_asyncio để cho phép lồng vòng lặp sự kiện
nest_asyncio.apply()
load_dotenv()

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    handlers=[
        logging.FileHandler("gemini_api_calls.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Định nghĩa số lượng gọi API mỗi phút
API_CALLS_PER_MINUTE = 15
CONCURRENT_WORKERS = 10  # Điều chỉnh dựa trên khả năng của hệ thống

# Lấy khóa API từ biến môi trường để tăng cường bảo mật
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY is not set. Please set it as an environment variable.")
    exit(1)
genai.configure(api_key=GOOGLE_API_KEY)

# Định nghĩa schema JSON mong đợi sử dụng TypedDict
class ResponseSchema(TypedDict):
    img_des: str
    ocr_result: str
    ocr_context: str
    od: str
    colors: str

# Danh sách hình ảnh mẫu
list_img = sorted(glob.glob('./backend/db/s_optimized_keyframes/*.webp'))[50:100]

# Chuẩn bị prompt với đầu vào cố định
PROMPT = """
Please analyze the provided image and produce a JSON object with the following fields:

- 'img_des': Generate a concise and clear description of the image in one paragraph. Focus on the main objects, actions, and relevant context. Minor details are also mentioned. The description should accurately capture the scene, relationships between objects, and any key actions or emotions, if present. Ensure the language is precise, neutral, and no longer than two sentences. Note: Ignore news overlay on red banner.

- 'ocr_result': OCR for this image, separate each piece of information with " || "

- 'ocr_context': A concise summary that captures the OCR information

- 'od': List all common objects in this image using the most simple/common words

- 'colors': List colors included in the image: Red, Blue, Green, Yellow, Orange, Pink, Purple, Brown, Black, White, Gray
"""

# Danh sách để lưu kết quả
results: List[Dict] = [None] * len(list_img)

# Cấu hình retry
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 5  # giây

# Semaphore để giới hạn số lượng worker đồng thời
semaphore = asyncio.Semaphore(CONCURRENT_WORKERS)

async def process_image(index: int, image_path: str):
    """
    Xử lý một hình ảnh duy nhất: tải lên và gọi API với cơ chế retry và exponential backoff.
    """
    global results
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with semaphore:
                logger.info(f"[{index}] Bắt đầu xử lý '{image_path}' (Lần thử {attempt})")

                # Tải lên hình ảnh sử dụng File API
                uploaded_image = await asyncio.to_thread(genai.upload_file, path=image_path)
                logger.info(f"[{index}] Tải lên '{image_path}' thành URI: {uploaded_image.uri}")

                # Kiểm tra trạng thái tệp cho đến khi nó trở thành ACTIVE
                while True:
                    uploaded_file = await asyncio.to_thread(genai.get_file, uploaded_image.name)
                    if uploaded_file.state.name == "ACTIVE":
                        logger.info(f"[{index}] Tệp '{uploaded_image.uri}' đã sẵn sàng.")
                        break
                    elif uploaded_file.state.name == "FAILED":
                        raise ValueError(f"Tải lên tệp thất bại cho '{image_path}'.")
                    else:
                        await asyncio.sleep(1)  # Chờ trước khi kiểm tra lại

                # Chọn mô hình Gemini
                model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")

                # Gọi GenerateContent API
                response = await asyncio.to_thread(
                    model.generate_content,
                    [uploaded_file, PROMPT],
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=ResponseSchema
                    ),
                    request_options={"timeout": 600}
                )

                # Lưu kết quả vào danh sách ở vị trí đúng
                results[index] = response.text
                logger.info(f"[{index}] Gọi API thành công.")
                return  # Thoát sau khi xử lý thành công

        except Exception as e:
            logger.error(f"[{index}] Lỗi khi xử lý '{image_path}': {e}")
            if attempt < MAX_RETRIES:
                backoff = INITIAL_RETRY_DELAY * 2 ** (attempt - 1)
                logger.info(f"[{index}] Thử lại sau {backoff} giây...")
                await asyncio.sleep(backoff)
            else:
                logger.error(f"[{index}] Thất bại sau {MAX_RETRIES} lần thử.")
                results[index] = None  # Hoặc lưu thông báo lỗi nếu cần

async def main():
    start_time = time.time()
    logger.info("Bắt đầu xử lý các hình ảnh...")

    batch_size = API_CALLS_PER_MINUTE  # 15
    total_images = len(list_img)
    batches = [list_img[i:i + batch_size] for i in range(0, total_images, batch_size)]

    for batch_num, batch in enumerate(batches, 1):
        logger.info(f"Đang xử lý lô {batch_num}/{len(batches)}")
        tasks = [
            asyncio.create_task(process_image(idx, img_path))
            for idx, img_path in enumerate(batch, start=(batch_num - 1) * batch_size)
        ]
        await asyncio.gather(*tasks)
        if batch_num < len(batches):
            logger.info("Đã hoàn thành lô hiện tại. Đang chờ 60 giây trước khi xử lý lô tiếp theo...")
            await asyncio.sleep(60)  # Chờ 60 giây trước khi xử lý lô tiếp theo

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Hoàn thành xử lý {total_images} hình ảnh trong {elapsed_time:.2f} giây.")

    # Kiểm tra số lượng gọi API thành công
    successful_calls = sum(1 for r in results if r is not None)
    logger.info(f"Số lượng gọi API thành công: {successful_calls}/{total_images}")

    # Ví dụ: In 5 kết quả đầu tiên
    for idx, res in enumerate(results[:5], 1):
        logger.info(f"Kết quả {idx}: {res}")

# Chạy hàm main
if __name__ == "_main_":
    asyncio.run(main())