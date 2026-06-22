from abc import ABC, abstractmethod


class FileDownloader(ABC):

	@abstractmethod
	def supports(self, data):
		pass

	@abstractmethod
	def download(self, data):
		pass


