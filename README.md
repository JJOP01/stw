# stw #

scraping the web is a tool I designed taking inspiration from the project yt-dlp -- creating a generalised extractor tool

# Requirements #

python >= 3.12.2

# Deployment #

```bash
cd stw
pip install -e .
playwright install chromium
```

This installs the required dependencies {Requests, Playwright, BeautifulSoup4} and chromium browser binaries

# Usage #

In bash enter `stw --help` to see all options