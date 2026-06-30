import os
import time
import requests

from .common import FileDownloader, DownloadContext

class HttpFD(FileDownloader):

        PROTOCOLS = ("http", "https")
	
	def download(self, info):
		url = info["url"]
                
                ctx = DownloadContext(filename=info["title"]+".mp4", tmp_filename=info["title"] + ".mp4.part")
		ctx.start_time = time.time()

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
                ctx.eta = 0
                self._hook_progress(ctx)
		os.replace(ctx.tmp_filename, ctx.filename)
