import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Filesystem layout of the dataset and external service credentials."""

    db_dir: Path = BACKEND_DIR / "db"
    google_api_key: str | None = None
    gemini_model: str = "models/gemini-1.5-flash"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            db_dir=Path(os.getenv("EVENTO_DB_DIR", BACKEND_DIR / "db")),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    @property
    def keyframes_dir(self) -> Path:
        return self.db_dir / "s_optimized_keyframes"

    @property
    def features_dir(self) -> Path:
        return self.db_dir / "features"

    @property
    def media_dir(self) -> Path:
        return self.db_dir / "media-info"

    @property
    def keyframes_csv(self) -> Path:
        return self.db_dir / "keyframes.csv"

    @property
    def video_urls_json(self) -> Path:
        return self.db_dir / "vid_url.json"

    @property
    def url_fps_json(self) -> Path:
        return self.db_dir / "url_fps.json"

    @property
    def device(self) -> str:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
