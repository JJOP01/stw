from .common import FileDownloader
from .http import HttpFD

PROTOCOL_MAP = {
    'http': HttpFD
}

def get_suitable_downloader(info):
    protocol = info["protocol"]
    try:
        return PROTOCOL_MAP[protocol]
    except KeyError:
        raise ValueError(f"Unknown protocol: {protocol}")

__all__ = [
    "FileDownloader",
    "get_suitable_downloader"
]
