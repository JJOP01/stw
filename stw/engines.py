from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from .elements import Element


class ExtractionEngine(ABC):

    @abstractmethod
    def extract(self, url, rules):
        pass

    @abstractmethod
    def find(self, source, selector):
        pass

    def apply_rules(self, source, rules):
        """ Convert elements into extracted data """
        data = {}
        for rule in rules:
            matched = self.find(source, rule.selector)
            if not matched: 
                continue
            if rule.multi:
                data[rule.key] = [element.value(rule) for element in matched]
            else:
                data[rule.key] = matched[0].value(rule)
                
        return data


class RequestEngine(ExtractionEngine):

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def extract(self, url, rules):
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return self.apply_rules(soup, rules)

    def find(self, soup, selector):
        return [Element(element, "bs4") for element in soup.select(selector)]


class PlaywrightEngine(ExtractionEngine):
    
    def __init__(self, context):
        self.context = context
        
    def extract(self, url, rules):
        page = self.context.new_page()
        try:
            page.set_default_timeout(3000) # timeouts subject to change
            page.set_default_navigation_timeout(10000)
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            return self.apply_rules(page, rules)
        
        finally:
            page.close()
        
    def find(self, page, selector):
        locator = page.locator(selector)
        return [Element(locator.nth(i), "playwright") for i in range(locator.count())]


class SeleniumEngine(ExtractionEngine):
    pass #assert False, "Not Implemented"