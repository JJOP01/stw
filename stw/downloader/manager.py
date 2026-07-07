import re

from . import get_suitable_downloader
from ..utils import determine_ext
from ..config import get_output_dir


class FileDownloadManager:
    
    def __init__(self):
        self.progress_hooks = []

    def add_progress_hook(self, hook):
        self.progress_hooks.append(hook)

    def prepare_filename(self, info):
        title = self._sanitise_filename(info.get("title", "video"))
        ext = info.get("ext", "mp4")
        return get_output_dir() / f"{title}.{ext}"

    def _sanitise_filename(self, name):
        name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name).strip(" .")
        return name or "video"

    def download(self, info):
        fd = get_suitable_downloader(info)()
        for hook in self.progress_hooks:
            fd.add_progress_hook(hook)

        filename = self.prepare_filename(info)
        return fd.download(filename, info)
