class Element:

    def __init__(self, element, backend):
        self.element = element
        self.backend = backend

    def get(self, attribute):
        if self.backend == "bs4":
            return self.element.get(attribute)
        if self.backend == "playwright":
            return self.element.get_attribute(attribute)
        raise ValueError(f"Unknown element backend: {self.backend}")

    @property
    def text(self):
        if self.backend == "bs4":
            return self.element.text
        if self.backend == "playwright":
            return self.element.text_content()
        raise ValueError(f"Unknown element backend: {self.backend}")

    def value(self, rule):  
        if rule.mode == "attr":
            return self.get(rule.attribute)
        if rule.mode == "text":
            return self.text.strip()
        raise ValueError(f"Unsupported extraction mode: {rule.mode}")