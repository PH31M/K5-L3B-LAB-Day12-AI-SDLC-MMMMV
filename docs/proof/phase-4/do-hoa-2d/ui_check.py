"""Kiểm UI thật bằng Chromium (Playwright): chạy chonoi.live, thao tác bàn phím, chụp ảnh, gom lỗi console.

python ui_check.py <repo> <out_dir> [case ...]
"""
import json, os, re, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

ROOT, OUT = sys.argv[1], sys.argv[2]
CASES = sys.argv[3:]
os.makedirs(OUT, exist_ok=True)
RESULTS = {}


def server(args, scenario=None):
    cmd = [sys.executable, "-m", "chonoi.live", "--port", "0", *args]
    if scenario is not None:
        fd, path = tempfile.mkstemp(suffix=".json"); os.close(fd)
        with open(path, "w", encoding="utf-8") as f: json.dump(scenario, f)
        cmd += ["--scenario", path]
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    while True:
        line = p.stdout.readline()
        if not line: raise RuntimeError("server không lên: " + " ".join(cmd))
        m = re.search(r"(http://127\.0\.0\.1:\d+/)", line)
        if m: return p, m.group(1)


class Run:
    def __init__(self, pw, name, args, scenario=None, query=""):
        self.name = name
        self.proc, self.url = server(args, scenario)
        self.b = pw.chromium.launch()
        self.page = self.b.new_page(viewport={"width": 1280, "height": 720})
        self.errors = []
        self.page.on("pageerror", lambda e: self.errors.append("pageerror: " + str(e)))
        self.page.on("console", lambda m: self.errors.append(f"console.{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        self.page.goto(self.url + query)
        self.page.wait_for_timeout(1200)

    def state(self):
        return self.page.evaluate("fetch('/state').then(r=>r.json())")

    def key(self, k, ms=120):
        self.page.keyboard.down(k); self.page.wait_for_timeout(ms); self.page.keyboard.up(k)

    def wait(self, ms): self.page.wait_for_timeout(ms)

    def shot(self, fname):
        path = os.path.join(OUT, fname); self.page.screenshot(path=path); return fname

    def until(self, pred, timeout=15):
        t0 = time.time()
        while time.time() - t0 < timeout:
            s = self.state()
            if pred(s): return s
            self.wait(100)
        raise AssertionError(f"{self.name}: hết giờ chờ trạng thái")

    def close(self):
        fps = self.page.evaluate("window.__chonoi ? window.__chonoi.fps : null")
        self.b.close(); self.proc.terminate()
        return fps


def case_gather(pw):
    r = Run(pw, "gather", ["--mode", "gather", "--seed", "1"])
    out = {"shots": [r.shot("gather-surface.png")]}
    s0 = r.state()
    r.page.keyboard.down("d"); r.wait(1200); r.page.keyboard.up("d")
    r.page.keyboard.down("s"); r.wait(1800); r.page.keyboard.up("s")
    s1 = r.state()
    out["moved"] = {"from": s0["player"]["pos"], "to": s1["player"]["pos"]}
    out["shots"].append(r.shot("gather-dive.png"))
    out["scene"] = r.page.evaluate("window.__chonoi.scene")
    out["fps"] = r.close(); out["errors"] = r.errors
    return out


def case_warn(pw):
    sc = {"gather": {"player": {"pos": [57, 22], "oxygen_ticks": 300}}}
    r = Run(pw, "warn", ["--mode", "gather", "--seed", "1"], sc)
    r.wait(300)
    out = {"shots": [r.shot("gather-warnings.png")]}
    st = r.state(); out["monsters"] = st.get("monsters"); out["oxy"] = st["player"]["oxygen_ticks"]
    r.key("c"); r.wait(300); out["shots"].append(r.shot("gather-warnings-hc.png"))
    out["fps"] = r.close(); out["errors"] = r.errors
    return out


def case_fx0(pw):
    sc = {"gather": {"player": {"pos": [57, 22], "oxygen_ticks": 300}}}
    r = Run(pw, "fx0", ["--mode", "gather", "--seed", "1"], sc, query="?fx=0")
    r.wait(300)
    out = {"shots": [r.shot("gather-fx0.png")], "fps": r.close(), "errors": r.errors}
    return out


QUAN_SC = {"quan": {
    "player": {"pos": [5, 6.8]},
    "stock": {"ca_loc": 2, "bong_sung": 4, "ca_linh": 3, "bong_dien_dien": 2},
    "random_customers": False,
    "stoves": [{"id": "B1", "state": "cooking", "dish": "ca_loc_nuong_trui", "cook_ticks_left": 300, "order_id": "C2"},
               {"id": "B2", "state": "ready", "dish": "lau_ca_linh_dien_dien", "order_id": "C3"}],
    "customers": [
        {"id": "C1", "table_id": "T1", "dish_id": "goi_bong_sung", "patience_ticks_left": 700, "order_tick": 1},
        {"id": "C2", "table_id": "T2", "dish_id": "ca_loc_nuong_trui", "order_status": "assigned", "patience_ticks_left": 2600},
        {"id": "C3", "table_id": "T3", "dish_id": "lau_ca_linh_dien_dien", "order_status": "assigned", "patience_ticks_left": 3000},
        {"id": "C4", "table_id": "T4", "dish_id": "canh_chua_ca_loc", "state": "eating", "order_status": "served",
         "eat_ticks_left": 500, "base_price": 90, "tip": 18}]}}


def case_quan(pw):
    r = Run(pw, "quan", ["--mode", "quan", "--seed", "1"], QUAN_SC)
    out = {"shots": [r.shot("quan-fixture.png")]}
    r.key("e"); r.wait(400)
    s = r.state(); out["hand_after_E_at_B2"] = s.get("hand")
    # đi lên (W) → z phải tăng; rồi tới bàn T3 (9,6) dọn món
    z0 = s["player"]["pos"][1]
    r.page.keyboard.down("w"); r.wait(250); r.page.keyboard.up("w")
    z1 = r.state()["player"]["pos"][1]
    out["W_increases_z"] = z1 > z0
    r.page.keyboard.down("d"); r.wait(900); r.page.keyboard.up("d")
    r.page.keyboard.down("s"); r.wait(320); r.page.keyboard.up("s")
    s = r.state(); out["pos_near_T3"] = s["player"]["pos"]
    out["shots"].append(r.shot("quan-carry.png"))
    r.key("e"); r.wait(500)
    s = r.state(); out["served_events"] = [e["name"] for e in s["events"] if e["name"] in ("served", "dish_picked")]
    r.key("p"); r.wait(400); out["paused"] = r.state()["state"]; out["shots"].append(r.shot("quan-pause.png"))
    r.key("p"); r.wait(300); out["resumed"] = r.state()["state"]
    r.key("c"); r.wait(300); out["shots"].append(r.shot("quan-hc.png")); r.key("c")
    out["fps"] = r.close(); out["errors"] = r.errors
    return out


def case_day(pw):
    sc = {"day": {"money": 450, "earned": 450}, "quan": {"time_left_ticks": 600}}
    r = Run(pw, "day", ["--mode", "day", "--days", "1", "--seed", "3"], sc)
    out = {"shots": [r.shot("day-1-gather-intro.png")]}
    r.key("e"); r.wait(700)
    s = r.state(); out["after_E"] = {"mode": s["mode"], "phase": s["phase"], "bounds": s["meta"].get("bounds")}
    out["client_scene"] = r.page.evaluate("window.__chonoi.scene")
    out["shots"].append(r.shot("day-2-quan.png"))
    z0 = s["player"]["pos"][1]
    r.page.keyboard.down("w"); r.wait(300); r.page.keyboard.up("w")
    out["W_increases_z_in_day_quan"] = r.state()["player"]["pos"][1] > z0
    r.wait(2500); out["shots"].append(r.shot("day-3-quan-customer.png"))
    s = r.until(lambda s: s["phase"] == "shop", 20)
    r.wait(400); out["shots"].append(r.shot("day-4-shop.png"))
    out["shop_meta_max_ticks"] = s["meta"].get("max_ticks")
    r.key("1"); r.wait(500)
    s = r.state(); out["after_buy"] = {"money": s["money"], "upgrades": s.get("upgrades"), "active": s.get("active_upgrades")}
    out["shots"].append(r.shot("day-5-shop-bought.png"))
    r.key("3"); r.wait(400)
    r.key("2"); r.wait(400)
    out["shop_events"] = [(e["name"], e["data"]) for e in r.state()["events"] if e["name"] in ("buy_failed", "bought")]
    out["shots"].append(r.shot("day-6-shop-fail.png"))
    r.key("Enter"); s = r.until(lambda s: s["finished"], 5)
    r.wait(400); out["end"] = {"reason": s["reason"], "money": s["money"], "upgrades": s.get("upgrades")}
    out["shots"].append(r.shot("day-7-summary.png"))
    out["fps"] = r.close(); out["errors"] = r.errors
    return out


def case_quan_plain(pw):
    r = Run(pw, "quan-plain", ["--mode", "quan", "--seed", "1"])
    r.wait(3000)
    out = {"shots": [r.shot("quan-plain.png")], "fps": r.close(), "errors": r.errors}
    return out


ALL = {"gather": case_gather, "warn": case_warn, "fx0": case_fx0, "quan": case_quan, "day": case_day, "quanplain": case_quan_plain}
with sync_playwright() as pw:
    for name in (CASES or ALL):
        try:
            RESULTS[name] = ALL[name](pw)
        except Exception as e:  # noqa
            RESULTS[name] = {"exception": repr(e)}
print(json.dumps(RESULTS, ensure_ascii=False, indent=1))
