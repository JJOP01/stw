import time

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DownloadContext:
	filename: str
	tmp_file_name: str
	downloaded: int = 0
	total: int = 0
	speed: float | None = None
	eta: int | None = None
	start_time: float = 0


class FileDownloader(ABC):

	def __init__(self):
		""" Create """
		self.progress_hooks = []

	def add_progress_hooks(self, hook):
		self.progress_hooks.append(hook)

	def _hook_progress(self, status):
		for hook in progress_hooks:
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

	@staticmethod
	def calc_eta()

	@abstractmethod
	def download(self, filename, info):
		pass


class HttpFD(FileDownloader):
	def download(self, filename, info):
		url = info