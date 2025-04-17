import sqlite3, datetime as dt, statistics, pathlib, json
DB = pathlib.Path(__file__).resolve().parent.parent / "oracle.db"

def last_hour():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    t0 = (dt.datetime.utcnow() - dt.timedelta(hours=1)).isoformat(timespec='seconds')
    cur.execute("SELECT z FROM raw_dot WHERE ts >= ?", (t0,))
    zs = [row[0] for row in cur.fetchall()]
    conn.close(); return zs

def detect():
    zs = last_hour()
    if len(zs) < 6: return None
    mean = statistics.mean(zs)
    if mean >= 2.6:
        return {"time": dt.datetime.utcnow().isoformat(timespec='seconds'),
                "mean_z": round(mean, 3), "samples": len(zs)}
    return None

if __name__ == "__main__":
    res = detect()
    print(json.dumps(res) if res else "no-anomaly")
