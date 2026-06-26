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
    downloader: str = "SET DOWNLOADER" 
    options: dict = field(default_factory=dict)

    def __post_init__(self): # processors outside the scope of configs

        valid_engines, valid_downloaders = {"request", "playwright"}, {"http", "yt-dlp"}
        if self.engine not in valid_engines:
            raise ValueError(f"Unknown engine: {self.engine}")
        if self.downloader not in valid_downloaders:
            raise ValueError(f"Unknown downloader: {self.downloader}")
        if not self.rules:
            raise ValueError("Site requires at least one extraction rule")
    
SITE_CONFIGS = {
    "default.site": Site(engine="playwright",
                         rules=(Rule(selector="video", attribute="src", mode="attr", key="video"),
                                Rule(selector="title", mode="text", key="title")),
                         processors=("resolve_streamtape",),
                         downloader="http"),
    
    "beta.xfreehd.com": Site(engine="playwright",
                         rules=[Rule(selector="source[title='SD']", attribute="src", mode="attr", key="video"),
                                Rule(selector="title", mode="text", key="title")],
                         downloader="http"),
}
