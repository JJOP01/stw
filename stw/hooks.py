from .downloader import FileDownloader

def console_progress(ctx):
	percent = FileDownloader.calc_percent(ctx.downloaded_bytes, ctx.total_bytes)
	speed = (ctx.speed / 1024 / 1024 if ctx.speed else 0)
	print(
		f"\r[download] {percent:5.1f}% of "
		f"{FileDownloader.format_bytes(ctx.total_bytes)} "
		f"at {FileDownloader.format_speed(ctx.speed)} "
		f"ETA {FileDownloader.format_time(ctx.eta)}",
		end=""
	)