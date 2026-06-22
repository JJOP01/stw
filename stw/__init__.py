import os
import argparse
from urllib.parse import urlparse

# TODO: make scraper
from scraper import Scraper

def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    
    parser.add_argument("urls", nargs="+")
    parser.add_argument("-t", "--test", action="store_true", help="test if each scraping engine works ons")
    parser.add_argument("--direct", action="store_true", help="download urls as direct links to media files")
    parser.add_argument("-dry", action="store_true", help="perform dry run of program on urls")
    
    return parser.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)

    # TODO: add working web-scraper
    scraper = Scraper()

    for url in args.urls:
        
        if args.test:
            results = scraper.compare_engines(url)

            for name, result in results.items():
                print(f"\n[{name}]")
                print(f"    link: {result.get('video')}")
                print(f"   title: {result.get('title')}")
                
            continue
        
        if args.direct:
            

if __name__ == "__main__":
    main()
