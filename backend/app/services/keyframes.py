import ast
import json
import re
from pathlib import Path

import pandas as pd

from core.config import Settings
from schema.search import Hit


class KeyframeNotFound(LookupError):
    pass


class KeyframeCatalog:
    """Keyframe ids, their files, their videos and per-video metadata.

    A keyframe id is its position in the sorted keyframe file list, which is
    also the row order of the FAISS indexes and `keyframes.csv`.
    """

    EXT = ".webp"
    FRAME_REF = re.compile(r"^(L\d{2}_V\d{3}),\s*(\d{1,5})$")

    def __init__(
        self,
        images_dir: Path,
        media_dir: Path,
        image_names: list[str],
        frames: pd.DataFrame,
        video_urls: dict[str, str],
        url_fps: dict[str, float],
    ):
        self.images_dir = images_dir
        self.media_dir = media_dir
        self.image_names = image_names
        self.frames = frames
        self.video_urls = video_urls
        self.url_fps = url_fps

    @classmethod
    def from_settings(cls, settings: Settings) -> "KeyframeCatalog":
        frames = pd.read_csv(settings.keyframes_csv, sep="|")
        frames["shot"] = frames["shot"].map(ast.literal_eval)
        return cls(
            images_dir=settings.keyframes_dir,
            media_dir=settings.media_dir,
            image_names=sorted(
                p.name for p in settings.keyframes_dir.glob(f"*{cls.EXT}")
            ),
            frames=frames,
            video_urls=json.loads(settings.video_urls_json.read_text()),
            url_fps=json.loads(settings.url_fps_json.read_text()),
        )

    @property
    def ocr_texts(self) -> list[str | None]:
        return [text if isinstance(text, str) else None for text in self.frames["ocr"]]

    def hit(self, keyframe_id: int, score: float) -> Hit:
        image = self.image_names[keyframe_id]
        video, frame = Path(image).stem.split("-")
        url = self.video_urls[video]
        second = int(int(frame) / self.url_fps[url])
        return Hit(image=image, video=video, frame=int(frame), url=f"{url}&t={second}", score=score)

    def image_path(self, image: str) -> Path:
        path = self.images_dir / Path(image).name  # basename only: no path traversal
        if not path.is_file():
            raise KeyframeNotFound(image)
        return path

    def video_metadata(self, video: str) -> dict:
        path = self.media_dir / f"{Path(video).name}.json"
        if not path.is_file():
            raise KeyframeNotFound(video)
        return json.loads(path.read_text())

    def parse_frame_ref(self, query: str) -> tuple[str, int] | None:
        """Parse `"L01_V001, 1234"` into `("L01_V001", 1234)`."""
        match = self.FRAME_REF.match(query.strip())
        return (match[1], int(match[2])) if match else None

    def closest_keyframe(self, video: str, frame: int) -> Path:
        """Keyframe nearest to `frame` within the shot that contains it."""
        rows = self.frames[self.frames["vid_name"] == video]
        rows = rows[rows["shot"].map(lambda shot: shot[0] <= frame <= shot[1])]
        if rows.empty:
            raise KeyframeNotFound(f"{video}, {frame}")
        nearest = rows.loc[(rows["frame"] - frame).abs().idxmin(), "frame"]
        return self.image_path(f"{video}-{int(nearest):05d}{self.EXT}")
