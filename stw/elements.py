class Element:

    def __init__(self, element, backend):
        self.element = element
        self.backend = backend

    def get(self, attribute):
        if self.backend == "bs4": return self.element.get(attribute)
        if self.backend == "playwright": return self.element.get_attribute(attribute)
        raise ValueError(f"Unknown element backend: {self.backend}")

    def text(self):
        if self.backend == "bs4": return self.element.text
        if self.backend == "playwright": return self.element.text_content()
        raise ValueError(f"Unknown element backend: {self.backend}")
