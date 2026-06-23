import json
import re
import requests

class InfoExtractor:

	VALID_URL = None

	@classmethod
	def suitable(cls, url):
		return cls.VALID_URL and re.match(cls.VALID_URL, url)

	def extract(self, url):
		return self._real_extract(url)

	def _real_extract(self, url):
		raise NotImplemented

	def _download_webpage(self, url):
		response = request.get(url, headers={"User-Agent":"Mozilla/5.0"})
		response.raise_for_status()
		return response.text

	