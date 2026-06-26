from dataclasses import dataclass, field

@dataclass(frozen=True)
class Rule:
    selector: str
    mode: str
    key: str
    attribute: str | None = None
    multi: bool = False

    def __post_init__(self):
        
        valid_modes = {"attr", "text"}
        if self.mode not in valid_modes:
            raise ValueError(f"Unknown extraction mode: {self.mode}")
        if self.mode == "attr" and not self.attribute:
            raise ValueError(f"attr extraction requires attribute")
        if self.mode == "text" and self.attribute is not None:
            raise ValueError("text extraction cannot have attribute")

@dataclass(frozen=True)
class Site:
    rules: tuple[Rule, ...]
    engine: str = "playwright"
    processors: tuple[str, ...] = ()
    options: dict = field(default_factory=dict)

    def __post_init__(self): # processors outside the scope of configs

        valid_engines = {"request", "playwright"}
        if self.engine not in valid_engines:
            raise ValueError(f"Unknown engine: {self.engine}")
        if not self.rules:
            raise ValueError("Site requires at least one extraction rule")
    
SITE_CONFIG = {
    "website1.com": Site(engine="playwright",
                         rules=(Rule(selector="video", mode="attr", attribute="src", key="video"),
                                Rule(selector="title", mode="text", key="title")),
                         processors=("resolve_streamtape",),
                         options={"direct_download": True}),
    
    "website2.com": Site(engine="playwright",
                         rules=(Rule(selector="video", mode="attr", attribute="src", key="video"),
                                Rule(selector="title", mode="text", key="title")),
                         processors=("resolve_streamtape",),
                         options={"direct_download": True}),
}
