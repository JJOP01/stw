import re
import time

from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class MediaExtensions:
    video: tuple[str, ...]
    audio: tuple[str, ...]
    manifests: tuple[str, ...]
    subtitles: tuple[str, ...]

MEDIA_EXTENSIONS = MediaExtensions(
    video=("avi", "flv", "mkv", "mov", "mp4", "webm", "3gp", "m4v"),
    audio=("mp3", "aac", "flac", "m4a", "ogg", "opus", "wav"),
    manifests=("m3u8", "mpd", "f4m", "smil"),
    subtitles=("srt", "vtt", "ass"),)

KNOWN_EXTENSIONS = (*MEDIA_EXTENSIONS.video, *MEDIA_EXTENSIONS.audio,*MEDIA_EXTENSIONS.manifests,)

def determine_ext(url, default_ext="unknown_ext"):
    if url is None or "." not in url:
        return default_ext
    path = urlparse(url).path
    guess = path.rsplit(".", 1)[-1].lower().rstrip("/")
    if guess and guess.isalnum():
        return guess
    return default_ext
    
def determine_protocol(info):
    if info.get("protocol") is not None:
        return info.get("protocol")
    url = info["url"]
    return urlparse(url).scheme

def format_bytes(size):
    if size is None:
        return "N/A"
    size = float(size)
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TiB"

def format_speed(speed):
    if speed is None:
        return "N/A"
    return f"{format_bytes(speed)}/s"

def format_time(seconds):
    if seconds is None:
        return "N/A"
    seconds = int(seconds)
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def console_progress(ctx):
    print(
        f"\r[download] {ctx.percent:5.1f}% of "
        f"{format_bytes(ctx.total_bytes)} "
        f"at {format_speed(ctx.speed)} "
        f"ETA {format_time(ctx.eta)}",
        end=""
    )   
