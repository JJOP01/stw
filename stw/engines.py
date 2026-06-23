from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from elements import Element


class ExtractionEngine(ABC):

    @abstractmethod
    def extract(self, url, rules):
        pass

    @abstractmethod
    def find(self, selector):
        pass

    @staticmethod
    def extract_values(element, rule):
        """ Extract element from a single element according to rule """
        if rule.mode == "attr": return element.get(rule.attribute)
        if rule.mode == "text": return element.text.strip()
        raise ValueError(f"Unsupported extraction mode: {rule.mode}")

    def apply_rule(self, elements, rules):
        """ Convert elements into extracted data """
        data = {}
        for rule in rules:
            matched = elements(rule.selector)
            if not matched: continue
            if rule.multi:
                data[rule.key] = [self.extract_value(element, rule) for element in matched]
            else:
                data[rule.key] = self.extract_value(matched[0], rule)
                
        return data


class RequestEngine(ExtractionEngine):

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def extract(self, url, rules):
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, "html.parser")
        return self.apply_rules(rules)

    def find(self, selector):
        return [Element(element, "bs4") for element in self.soup.select(selector)]


class PlaywrightEngine(ExtractionEngine):

    BLOCKED_TYPES = {"image", "font", "stylesheet"}
    
    def __init__(self, context):
        self.context = context
        self.context.route("**/*", self.block)

    def block(self, route):
        if route.request.resource_type in self.BLOCKED_TYPES: route.abort()
        else: route.continue_()
        
    def extract(self, url, rules):
        self.page = self.context.new_page()
        try:
            self.page.set_default_timeout(3000) # timeouts subject to change
            self.page.set_default_navigation_timeout(10000)
            self.page.goto(url, wait_until="domcontentloaded", timeout=10000)
            return self.apply_rules(rules)
        
        finally:
            self.page.close()
        
    def find(self, selector):
        locator = self.page.locator(selector)
        return [Element(locator.nth(i), "playwright") for i in range(locator.count())]


class SeleniumEngine(ExtractionEngine):
    pass