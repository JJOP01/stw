import os
import argparse
from urllib.parse import urlparse

from .scraper import Scraper
from .downloader import FileDownloadManager
from .utils import console_progress

def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("-t", "--test", action="store_true", help="test if each scraping engine works ons")
    parser.add_argument("--media-url", action="store_true", help="download urls as direct links to media files")
    parser.add_argument("-dry", action="store_true", help="perform dry run of program on urls")    
    return parser.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    scraper = Scraper()
    manager = FileDownloadManager()
    manager.add_progress_hook(console_progress)
    try:
        for url in args.urls:
            if args.test:
                results = scraper.compare_engines(url)
                for name, result in results.items():
                    print(f"\n[{name}]")
                    print(f"    link: {result.get('url')}")
                    print(f"   title: {result.get('title')}")
                continue

            if args.media_url:
                filename = os.path.splitext(os.path.basename(urlparse(url).path))[0]
                manager.download(filename, url)
                continue

            data = scraper.extract(url)
            if data and not args.dry:
                manager.download(data)
            elif data:
                print(f"[link] {data}")
                print("[info] Skipping download")

    except KeyboardInterrupt:
        print("\n[info] KeyboardInterrupted")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
