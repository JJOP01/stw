from ..utils import determine_protocol


def get_suitable_downloader(info):
    protocol = determine_protocol(info)
    try:
        return PROTOCOL_MAP[protocol]
    except KeyError:
        raise ValueError(f"Unknown protocol: {protocol}")

    
from .common import FileDownloader
from .manager import FileDownloadManager
from .http import HttpFD


PROTOCOL_MAP = {
    'http': HttpFD,
    'https': HttpFD
}


__all__ = [
    "FileDownloader",
    "FileManager",
    "get_suitable_downloader"
]
