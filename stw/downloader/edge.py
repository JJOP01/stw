from pathlib import Path
import json
import subprocess
import time
import urllib.parse
import urllib.request
import websocket

EDGE = Path(r"\mnt\c\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") # change for yourself
EDGE_PORT = 9222
EDGE_DATA = Path("~//edge").expanduser()


class Edge:
    def __init__(self, port=EDGE_PORT, data_dir=EDGE_DATA):
        self.port, self.data_dir = port, data_dir

    @property
    def endpoint(self): return f"http://127.0.0.1:{self.port}"

    def start(self):
        if not EDGE.exists(): raise FileNotFoundError(f"Edge not found: {EDGE}")
        if self.running(): return
        self.data_dir.mkdir(parents=True, exist_ok=True)
        subprocess.Popen([str(EDGE), f"--remote-debugging-port={self.port}", f"--user-data-dir={self.data_dir}"])
        for _ in range(40):
            if self.running(): return
            time.sleep(.25)
        raise RuntimeError("Could not start Edge")

    def running(self):
        try:
            urllib.request.urlopen(f"{self.endpoint}/json/version", timeout=.5)
            return True
        except Exception: return False

    def pages(self):
        with urllib.request.urlopen(f"{self.endpoint}/json", timeout=2) as response:
            return json.load(response)

    def tab(self, url):
        domain = urllib.parse.urlparse(url).netloc
        page = next((p for p in self.pages() if p["type"] == "page" and urllib.parse.urlparse(p["url"]).netloc == domain), None)
        if page is None:
            with urllib.request.urlopen(f"{self.endpoint}/json/new?{urllib.parse.quote(url, safe=':/?=&')}") as response:
                page = json.load(response)
        return EdgeTab(page)


class EdgeTab:
    def __init__(self, page):
        self.ws, self.id = websocket.create_connection(page["webSocketDebuggerUrl"]), 0

    def call(self, method, params=None):
        self.id += 1
        self.ws.send(json.dumps({"id": self.id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == self.id: return message

    def navigate(self, url): return self.call("Page.navigate", {"url": url})

    def evaluate(self, expression):
        result = self.call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        return result["result"]["result"].get("value")

    def close(self): self.ws.close()
