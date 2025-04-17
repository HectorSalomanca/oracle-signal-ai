from fastapi import FastAPI, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import detector.anomaly as dz

app = FastAPI()
hits = Counter("oracle_anomalies_total", "Total detected anomalies")
last_z = Gauge("oracle_last_mean_z", "Mean Z in last detection")

@app.get("/check")
def check():
    res = dz.detect()
    if res:
        hits.inc()
        last_z.set(res["mean_z"])
    return res or {"status": "quiet"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
