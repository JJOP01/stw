from pathlib import Path
import json

ROOT = Path(__file__).parents[2]
DOWNLOADS = ROOT / "downloads"
LOCAL = Path(__file__).parent / "local.json"

def initialise():
    DOWNLOADS.mkdir(exist_ok=True)
    if not LOCAL.exists():
        LOCAL.write_text(json.dumps({"output_dir": str(DOWNLOADS)}, indent=4))
        
def get_output_dir():
    return Path(json.loads(LOCAL.read_text())["output_dir"])

def set_output_dir(path):
    path = Path(path).expanduser()
    if not path.is_dir():
        raise ValueError(f"'{path}' is not a valid directory")
    LOCAL.write_text(json.dumps({"output_dir": str(path)}, indent=4))

from .site_configs import SITE_CONFIGS 

__all__ = [
    "initialise",
    "get_output_dir",
    "set_output_dir",
    "SITE_CONFIGS",
]
