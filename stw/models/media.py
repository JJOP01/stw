from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class MediaInfo:
    url: str
    title: str = "video"
    ext: str | None = None
    downloader: str = "http"
    headers: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
