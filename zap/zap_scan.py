import time
import os
import requests
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


def seed_url(path):
    """Lader ZAP's interne HTTP-klient besøge URL'en — replacer-reglen injicerer auth."""
    try:
        zap.core.access_url(url=f"{TARGET}{path}", followredirects=True)
        print(f"      GET    {path} -> seedet")
    except Exception as e:
        print(f"      GET    {path} -> fejl: {e}")


# 1) Login og hent JWT token
print("[1/6] Logger ind som testuser@test.dk...")
for attempt in range(1, 4):
    try:
        resp = requests.post(
            f"{TARGET}/auth/login",
            json={"email": "testuser@test.dk", "password": "Test1234!"},
            timeout=60
        )
        resp.raise_for_status()
        break
    except requests.exceptions.Timeout:
        print(f"      Timeout (forsøg {attempt}/3) — prøver igen...")
        if attempt == 3:
            raise
token = resp.json()["access_token"]
auth = {"Authorization": f"Bearer {token}"}
print(f"      JWT token hentet ({len(token)} tegn)")

# 2) Tilføj Authorization-header til ZAP's session
zap.replacer.add_rule(
    description="JWT Auth Header",
    enabled=True,
    matchtype="REQ_HEADER",
    matchregex=False,
    matchstring="Authorization",
    replacement=f"Bearer {token}",
    initiators="",
)
print("      Authorization-header tilføjet til ZAP session")

# 3) Seed alle kendte endpoints
print("\n[2/6] Seeder kendte endpoints...")
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Opret test-todo direkte (uden ZAP proxy) for at få et ID til /todos/{id}
todo_id = None
r = requests.post(
    f"{TARGET}/todos",
    json={"title": "ZAP test todo", "completed": False},
    headers=auth, timeout=30, verify=False
)
if r.status_code in (200, 201):
    todo_id = r.json().get("id")
    print(f"      POST /todos -> {r.status_code} (id={todo_id})")
else:
    print(f"      POST /todos -> {r.status_code}")

# Seed via ZAP's interne HTTP-klient — replacer-reglen injicerer Authorization-header
for path in ["/health", "/auth/me", "/todos"]:
    seed_url(path)
if todo_id:
    seed_url(f"/todos/{todo_id}")

# Ryd op
if todo_id:
    requests.delete(f"{TARGET}/todos/{todo_id}", headers=auth, timeout=30, verify=False)
    print(f"      DELETE /todos/{todo_id} -> ryddet op")

# 4) Forbind
print(f"\n[3/6] Forbinder til ZAP ({ZAP_URL})...")
print(f"      Version: {zap.core.version}")

# 5) Spider
print(f"\n[4/6] Spider mod {TARGET}...")
spider_id = zap.spider.scan(TARGET)
poll(spider_id, "spider")
urls = zap.spider.results(spider_id)
print(f"      Fundet {len(urls)} URL'er")

# 6) Aktiv scan
print("\n[5/6] Aktiv scan...")
scan_id = zap.ascan.scan(TARGET)
poll(scan_id, "aktiv scan")
print("      Afsluttet")

# Alerts
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

# HTML rapport
os.makedirs("zap", exist_ok=True)
with open(REPORT, "w", encoding="utf-8") as f:
    f.write(zap.core.htmlreport())
print(f"\n[6/6] HTML rapport gemt: {REPORT}")
