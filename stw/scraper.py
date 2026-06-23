from urllib.parse import urlparse

class Scraper:

    def __init__(self, engines, processors, sites):
        self.engines = engines
        self.processors = processors
        self.sites = sites
        self.cache = {}

    def get_site(self, url):
        domain = urlparse(url).netloc.lower().removeprefix("www.")
        return self.sites.get(domain)

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
        
        data = self.run_processors(data, site.processors)
        if data: self.cache[url] = data

        return data


    def run_processors(self, data, processors):
        for name in processors:
            processor = self.processors.get(name)
            if not processor: raise ValueError(f"Unknown processor: {name}")

            data = processor(data)
            if not data: return None

        return data


    def compare_engines(self, url):
        site = self.get_site(url)
        if not site: return {}

        results = {}
        for name, engine in self.engines.items():
            try:
                results[name] = engine.extract(url, site.rules)
            except Exception as error:
                results[name] = {"error": str(error)}

        return results

    def close(self):
        for engine in self.engines.values():
            if hasattr(engine, "close"):
                engine.close()
