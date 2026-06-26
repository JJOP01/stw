import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

STREAMTAPE_NOROBOT_REGEX = re.compile(r"document\.getElementById\('norobotlink'\)\.innerHTML = (.+?);")
STREAMTAPE_TOKEN_REGEX = re.compile(r"token=([^&']+)")

def clean_title(data, context):
    title = data.get("title")
    if title:
        data["title"] = re.sub(r'[<>:"/\\|?*]', "", title)
    return data

def resolve_streamtape(data, context):
    if "video" not in data or "streamtape" not in data["video"]: return data
    url = data["video"].replace("/e/", "/v/")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html = response.text

    norobot = STREAMTAPE_NOROBOT_REGEX.search(html)
    if not norobot: return None
    token = STREAMTAPE_TOKEN_REGEX.search(norobot.group(1))
    if not token: return None

    soup = BeautifulSoup(html, "html.parser")
    hidden = soup.select_one("div#ideoooolink[style='display:none;']")
    if not hidden: return None

    data["video"] = f"https:/{hidden.text}&token={token.group(1)}&download=1"
    return data

def rebase_url(data, context):
    v = data.get("video")
    base = context.options.get("video_base")
    if v and v.startswith("/"):
        data["video"] = urljoin(base, v)
    return data

PROCESSORS = {
    "clean_title": clean_title,
    "resolve_streamtape": resolve_streamtape,
    "rebase_url": rebase_url
}