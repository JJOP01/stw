from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import time

import requests

@dataclass
class DownloadContext:
	filename: str
	tmp_filename: str
	downloaded_bytes: int = 0
	total_bytes: int | None = None
	speed: float | None = None
	eta: int | None = None
	start_time: float = 0


class FileDownloader(ABC):
	def __init__(self):
		self.progress_hooks = []

	def add_progress_hook(self, hook):
		self.progress_hooks.append(hook)

	def _hook_progress(self, status):
		for hook in self.progress_hooks:
			hook(status)

	@staticmethod
	def calc_percent(byte_counter, data_len):
		if data_len is None:
			return None
		return float(byte_counter) / float(data_len) * 100

	@staticmethod
	def calc_speed(start, now, bytes):
		dif = now - start
		if bytes == 0 or dif < 0.001:
			return None
		return float(bytes) / dif

	@classmethod
	def calc_eta(cls, start_or_rate, now_or_remaining, total=None, current=None):
		if total is None:
			rate, remaining = start_or_rate, now_or_remaining
			if None in (rate, remaining):
				return None
			return int(float(remaining) / rate)
		start, now = start_or_rate, now_or_remaining
		if now is None: now = time.time()
		rate = cls.calc_speed(start, now, current)
		return rate and int((float(total) - float(current)) / rate)

	@staticmethod
	def format_bytes(size):
		if size is None: return "N/A"
		size = float(size)
		for unit in ["B", "KiB", "MiB", "GiB"]:
			if size < 1024:
				return f"{size:.2f}{unit}"
			size /= 1024
		return f"{size:.2f}TiB"

	@classmethod
	def format_speed(cls, speed):
		if speed is None: return "N/A"
		return f"{cls.format_bytes(speed)}/s"

	@staticmethod
	def format_time(seconds):
		if seconds is None: return "N/A"
		seconds = int(seconds)
		h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
		if h > 0:
			return f"{h:02d}:{m:02d}:{s:02d}"
		return f"{m:02d}:{s:02d}"

	@abstractmethod
	def download(self, filename, info):
		pass


class HttpFD(FileDownloader):

	PROTOCOLS = ("http", "https")
	
	def download(self, filename, info):
		ctx = DownloadContext(filename, filename + ".part")
		ctx.start_time = time.time()
		url = info["video"]
		if os.path.exists(ctx.tmp_filename):
			ctx.downloaded_bytes = os.path.getsize(ctx.tmp_filename)
		headers = {}
		if ctx.downloaded_bytes:
			headers["Range"] = f"bytes={ctx.downloaded_bytes}-"

		with requests.get(url, headers=headers, stream=True, timeout=30) as response:
			response.raise_for_status()
			ctx.total_bytes = int(response.headers.get("Content-Length", 0))
			if ctx.downloaded_bytes:
				ctx.total_bytes += ctx.downloaded_bytes

			mode = "ab" if ctx.downloaded_bytes else "wb"
			with open(ctx.tmp_filename, mode) as file:
				for chunk in response.iter_content(8192):
					if not chunk:
						continue

					file.write(chunk)
					ctx.downloaded_bytes += len(chunk)
					now = time.time()
					ctx.speed = self.calc_speed(ctx.start_time, now, ctx.downloaded_bytes)
					ctx.eta = self.calc_eta(ctx.speed, ctx.total_bytes - ctx.downloaded_bytes)
					self._hook_progress(ctx)
		os.replace(ctx.tmp_filename, ctx.filename)



DOWNLOADERS = {
	"http": HttpFD(),
	# "yt-dlp": YTDLPDownloader(),
}


if __name__ == "__main__":

	try:
		downloadable_url = ""
		downloader = HttpFD()
		downloader.add_progress_hook(console_progress)
		downloader.download("test.mp4", {"video": downloadable_url})

	finally:
		if os.path.exists("test.mp4"):
			os.remove("test.mp4")
		elif os.path.exists("test.mp4.part"):
			os.remove("test.mp4.part")