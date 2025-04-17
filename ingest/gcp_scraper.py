import requests, re, sqlite3, datetime as dt, pathlib
DB = pathlib.Path(__file__).resolve().parent.parent / "oracle.db"
DOT_URL = "https://noosphere.princeton.edu/dot.html"
COLOR_RE = re.compile(r"dot-(green|blue|yellow|orange|red)")
ZS_RE    = re.compile(r"Z=([0-9.]+)")

def get_state():
    html = requests.get(DOT_URL, timeout=10).text
    color = COLOR_RE.search(html).group(1)
    zscore = float(ZS_RE.search(html).group(1))
    return color, zscore

def store(color, z):
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS raw_dot(
        ts TEXT PRIMARY KEY, color TEXT, z REAL)""")
    conn.execute("INSERT OR IGNORE INTO raw_dot VALUES(?,?,?)",
                 (dt.datetime.utcnow().isoformat(timespec='seconds'), color, z))
    conn.commit(); conn.close()

if __name__ == "__main__":
    c, z = get_state(); store(c, z); print("Saved", c, z)
