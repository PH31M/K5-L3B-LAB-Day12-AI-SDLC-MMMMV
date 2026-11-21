"""Kiểm HUD v1.2 trên Chromium thật (Playwright): độ tươi giỏ/kho, hàng ươn, giá theo tươi, dòng lũ.

Chạy: python docs/proof/phase-3/do-tuoi/ui_check_p3.py  (từ gốc repo; cần `pip install playwright`).
Ghi ảnh + ui-check-p3.json cạnh script. Không đổi luật: chỉ khởi `chonoi.live`, bấm phím, đọc /state.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def item(i, kind, fresh):
    return {"id": i, "kind": kind, "fresh": fresh}


def start(mode, scenario):
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(scenario, f)
    p = subprocess.Popen([sys.executable, "-m", "chonoi.live", "--mode", mode, "--port", "0", "--scenario", path],
                         cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    url = None
    while not url:
        line = p.stdout.readline()
        if not line:
            raise RuntimeError("live không khởi động")
        m = re.search(r"(http://127\.0\.0\.1:\d+/)", line)
        url = m and m.group(1)
    return p, url


def main():
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        def page(url):
            pg = browser.new_page(viewport={"width": 1280, "height": 720})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
            pg.goto(url)
            pg.wait_for_timeout(900)
            return pg, errs

        def state(pg):
            return pg.evaluate("fetch('/state').then(r => r.json())")

        def wait_until(pg, pred, seconds):
            for _ in range(int(seconds * 10)):
                if pred(state(pg)):
                    return
                pg.wait_for_timeout(100)
            raise TimeoutError("hết thời gian chờ trạng thái")

        # 1) Gather: giỏ có độ tươi khác nhau + một con sắp ươn (30.02 -> ươn sau 3 bước)
        hold = [item("I1", "ca_loc", 95), item("I2", "ca_linh", 45), item("I3", "ca_linh", 30.02),
                item("I4", "bong_sung", 12)]
        p, url = start("gather", {"gather": {"hold": hold, "random_fish": False, "monsters": []}})
        try:
            pg, errs = page(url)
            pg.wait_for_timeout(600)
            st = state(pg)
            pg.screenshot(path=os.path.join(HERE, "gather-hold-fresh.jpg"), type="jpeg", quality=80)
            results["gather_hold"] = {"hold": st["hold"], "errors": list(errs)}
            # 2) dòng lũ: chờ báo trước (phase_tick 1680) rồi lặn xuống >= 10 m trước khi dòng bắt đầu ở 1800
            wait_until(pg, lambda s: s["phase_tick"] >= 1690, 60)
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(HERE, "gather-current-warning.jpg"), type="jpeg", quality=80)
            warn_tick = state(pg)["phase_tick"]
            pg.keyboard.down("s")
            pg.wait_for_timeout(1700)
            pg.keyboard.up("s")
            wait_until(pg, lambda s: s.get("current"), 20)
            before = state(pg)
            pg.wait_for_timeout(1000)
            after = state(pg)
            pg.screenshot(path=os.path.join(HERE, "gather-current-active.jpg"), type="jpeg", quality=80)
            results["current"] = {"warning_seen_at_phase_tick": warn_tick, "current": after["current"],
                                  "depth": after["player"]["pos"][1],
                                  "x_drift_1s_no_input": round(after["player"]["pos"][0] - before["player"]["pos"][0], 3),
                                  "errors": list(errs)}
            pg.close()
        finally:
            p.terminate()

        # 3) Quán: kho có độ tươi, đơn đang giữ một con sắp ươn -> giữ lại; nấu -> giá chốt theo tươi
        stock = [item("I1", "ca_loc", 30.01), item("I2", "ca_loc", 72), item("I3", "bong_sung", 88),
                 item("I4", "bong_sung", 41), item("I5", "ca_linh", 18)]
        sc = {"quan": {"random_customers": False, "player": {"pos": [3, 8]}, "stock": stock,
                       "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                      "reserved": ["I1"], "patience_ticks_left": 3600}]}}
        p, url = start("quan", sc)
        try:
            pg, errs = page(url)
            st = state(pg)
            pg.screenshot(path=os.path.join(HERE, "quan-stock-fresh.jpg"), type="jpeg", quality=80)
            guest = st["customers"][0]
            pg.keyboard.press("e")
            pg.wait_for_timeout(700)
            st2 = state(pg)
            pg.screenshot(path=os.path.join(HERE, "quan-cook-price.jpg"), type="jpeg", quality=80)
            cook = [e for e in st2.get("events", []) if e.get("name") == "cook_started"]
            spoiled = [e for e in st2.get("events", []) if e.get("name") == "spoiled"]
            results["quan"] = {"reserved_after_spoil": guest["reserved"], "order_status": guest["order_status"],
                               "spoiled_events": [e["data"] for e in spoiled],
                               "cook_started": cook[0]["data"] if cook else None,
                               "stock_after": st2["stock"], "errors": list(errs)}
            pg.keyboard.press("c")
            pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(HERE, "quan-stock-hc.jpg"), type="jpeg", quality=80)
            results["quan"]["errors_after_hc"] = list(errs)
            pg.close()
        finally:
            p.terminate()
        browser.close()
    with open(os.path.join(HERE, "ui-check-p3.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps(results, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
