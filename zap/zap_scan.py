import time
import os
from zapv2 import ZAPv2

TARGET    = "https://pythonayd-todo-api.onrender.com"
ZAP_URL   = "http://localhost:8090"
REPORT    = "zap/zap_report.html"

zap = ZAPv2(proxies={"http": ZAP_URL, "https": ZAP_URL})


def poll(scan_id, scan_type):
    while True:
        if scan_type == "spider":
            pct = int(zap.spider.status(scan_id))
        else:
            pct = int(zap.ascan.status(scan_id))
        print(f"  {scan_type} fremgang: {pct}%")
        if pct >= 100:
            break
        time.sleep(5)


# 1) Forbind
print(f"[1/4] Forbinder til ZAP ({ZAP_URL})...")
print(f"      Version: {zap.core.version}")

# 2) Spider
print(f"\n[2/4] Spider mod {TARGET}...")
spider_id = zap.spider.scan(TARGET)
poll(spider_id, "spider")
urls = zap.spider.results(spider_id)
print(f"      Fundet {len(urls)} URL'er")

# 3) Aktiv scan
print("\n[3/4] Aktiv scan...")
scan_id = zap.ascan.scan(TARGET)
poll(scan_id, "aktiv scan")
print("      Afsluttet")

# 4) Alerts
alerts = zap.core.alerts(baseurl=TARGET)
risk_order = ["High", "Medium", "Low", "Informational"]
buckets = {r: [] for r in risk_order}
for a in alerts:
    buckets.setdefault(a.get("risk", "Informational"), []).append(a)

print(f"\n{'='*60}")
print(f"  Resultater: {len(alerts)} alert(s) mod {TARGET}")
print(f"{'='*60}")
for risk in risk_order:
    items = buckets[risk]
    if items:
        print(f"\n[{risk.upper()}] — {len(items)} fund")
        for a in items:
            print(f"  • {a.get('alert')}")
            print(f"    URL : {a.get('url')}")
            desc = a.get("description", "")
            if desc:
                print(f"    Beskr: {desc[:120]}...")

# 5) HTML rapport
os.makedirs("zap", exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write(zap.core.htmlreport())
print(f"\nHTML rapport gemt: {REPORT}")
