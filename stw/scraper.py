from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

from .engines import RequestEngine, PlaywrightEngine
from .processors import PROCESSORS
from .site_configs import SITE_CONFIGS
from .downloader import DOWNLOADERS

BLOCKED_RESOURCE_TYPES = {"image", "font", "stylesheet"}

class Scraper:

    def __init__(self):
        self.cache = {}
        self.processors = PROCESSORS
        self.sites = SITE_CONFIGS
        self.downloaders = DOWNLOADERS

        self.setup_browser()
        self.engines = {"request": RequestEngine(), "playwright": PlaywrightEngine(self.context)}

    def setup_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.context.route("**/*", self.block)

    def block(self, route):
        if route.request.resource_type in BLOCKED_RESOURCE_TYPES:
            route.abort()
        else:
            route.continue_()

    def extract(self, url):
        if url in self.cache: return self.cache[url]

        site = self.get_site(url)
        if not site:
            print(f"[error] Unsupported site: {url}")
            return None

        engine = self.engines.get(site.engine)
        if not engine: raise ValueError(f"Missing engine: {site.engine}")

        data = engine.extract(url, site.rules)
        if not data: return None

        data = self.run_processors(data, site.processors, site)
        if data:  self.cache[url] = data

        return data

    def get_site(self, url):
        domain = urlparse(url).netloc.lower().removeprefix("www.")
        return self.sites.get(domain)

    def run_processors(self, data, processors, site):
        for name in processors:
            processor = self.processors.get(name)
            if not processor: 
                raise ValueError(f"Unknown processor: {name}")
            data = processor(data, site)
            if not data: 
                return None
        return data

    def compare_engines(self, url):
        site = self.get_site(url)
        if not site:
            return {}
        results = {}
        for name, engine in self.engines.items():
            try:
                results[name] = engine.extract(url, site.rules)
            except Exception as error:
                results[name] = {"error": str(error)}
        return results

    def download(self, data, site):
        downloader = self.downloaders.get(site.downloader)

    def close(self):
        for engine in self.engines.values():
            if hasattr(engine, "close"):
                engine.close()

        self.context.close()
        self.browser.close()
        self.playwright.stop()

