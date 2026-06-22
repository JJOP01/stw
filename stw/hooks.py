import re
import requets

from urllib.parse import urljoin
from bs4 import BeautifulSoup

STREAMTAPE_NOROBOT_REGEX = re.compile(r"document\.getElementById\('norobotlink'\)\.innerHTML = (.+?);")
STREAMTAPE_TOKEN_REGEX = re.compile(r"token=([^&']+)")



def clean_title(title):
