import os
import time
import requests

from .common import FileDownloader, DownloadContext

CHUNK_SIZE = 8192


class HttpFD(FileDownloader):

        PROTOCOLS = ("http", "https")
        
        def download(self, filename, info):
                url = info["url"]

                ctx = DownloadContext(filename=filename, tmp_filename=filename+'.part')
                ctx.start_time = time.time()
                if os.path.exists(ctx.tmp_filename):
                        ctx.downloaded_bytes = os.path.getsize(ctx.tmp_filename)
                headers = {}
                if ctx.downloaded_bytes:
                        headers["Range"] = f"bytes={ctx.downloaded_bytes}-"
                        
                with requests.get(url, headers=headers, stream=True, timeout=30) as response:
                        response.raise_for_status()
                        content_length = int(response.headers.get("Content-Length", 0))
                        if ctx.downloaded_bytes and response.status_code == 206:
                                mode = "ab"
                                ctx.total_bytes = content_length + ctx.downloaded_bytes
                        else:
                                mode = "wb"
                                ctx.downloaded_bytes = 0
                                ctx.total_bytes = content_length

                        with open(ctx.tmp_filename, mode) as file:
                                for chunk in response.iter_content(CHUNK_SIZE):
                                        if not chunk:
                                                continue
                                        file.write(chunk)
                                        ctx.downloaded_bytes += len(chunk)
                                        now = time.time()
                                        ctx.speed = self.calc_speed(ctx.start_time, now, ctx.downloaded_bytes)
                                        remaining_bytes = ctx.total_bytes - ctx.downloaded_bytes
                                        ctx.eta = self.calc_eta(ctx.speed, remaining_bytes)
                                        ctx.percent = self.calc_percent(ctx.downloaded_bytes, ctx.total_bytes)
                                        self._hook_progress(ctx)
                        os.replace(ctx.tmp_filename, ctx.filename)
                        ctx.eta = 0
                        ctx.percent = 100.0
                        self._hook_progress(ctx)

