"""Smoke Phase 3 theo TICKET-03 qua headless_cmd; ghi bản ghi vào smoke-p3.txt cạnh script.

Chạy từ gốc repo: python docs/proof/phase-3/do-tuoi/smoke_p3.py
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CMD = [sys.executable, "-m", "chonoi.headless"]
log = []


def run(*args):
    p = subprocess.run([*CMD, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    shown = " ".join(a if os.sep not in a and "/" not in a else os.path.basename(a) for a in args)
    log.append(f"$ python3 -m chonoi.headless {shown}\n  exit={p.returncode} {p.stderr.strip()}")
    return p.returncode


def rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return path


with tempfile.TemporaryDirectory() as d:
    j = lambda n: os.path.join(d, n)  # noqa: E731
    ok = True

    # 1) Ngưỡng 30: một bước gather không input -> spoiled ở tick 1
    log.append("## 1. Fixture ngưỡng 30 (nguyên văn ticket)")
    sc = write(j("s30.json"), {"gather": {"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 30}],
                                          "random_fish": False, "monsters": []}})
    ok &= run("--mode", "gather", "--seed", "1", "--ticks", "1", "--scenario", sc, "--out", j("o30.jsonl")) == 0
    ev = [r for r in rows(j("o30.jsonl")) if r["type"] == "event"]
    log.append("  " + json.dumps(ev, ensure_ascii=False))
    want = [{"type": "event", "tick": 1, "phase": "gather", "name": "spoiled",
             "data": {"item_id": "I1", "kind": "ca_linh", "location": "hold"}}]
    ok &= ev == want
    log.append(f"  khớp dòng mẫu của ticket: {ev == want}")

    # 2) Smoke bàn giao file: fresh 100, interact frame 0, rồi quan --ticks 0
    log.append("\n## 2. Smoke bàn giao hai tiến trình")
    sc = write(j("s100.json"), {"gather": {"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 100}],
                                           "random_fish": False, "monsters": []}})
    inp = write(j("in.json"), {"frames": [{"tick": 0, "interact": True}]})
    ok &= run("--mode", "gather", "--seed", "1", "--ticks", "10", "--scenario", sc, "--inputs", inp,
              "--out", j("g.jsonl"), "--inventory-out", j("kho.json")) == 0
    with open(j("kho.json"), encoding="utf-8") as f:
        saved_text = f.read()
    saved = json.loads(saved_text)
    log.append("  file kho: " + saved_text.strip())
    ok &= run("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", j("kho.json"), "--out", j("q.jsonl")) == 0
    stock = [r for r in rows(j("q.jsonl")) if r["type"] == "snapshot"][0]["stock"]
    log.append("  snapshot quán tick 0 stock: " + json.dumps(stock, ensure_ascii=False))
    same = ([(i["id"], i["kind"]) for i in stock] == [(i["id"], i["kind"]) for i in saved["items"]]
            and all(abs(a["fresh"] - b["fresh"]) <= 0.01 for a, b in zip(stock, saved["items"]))
            and saved["items"][0]["fresh"] == 100 - 2 / 240)
    ok &= same
    log.append(f"  id/kind giống, fresh = 100 − 2/240 (sau một lần hao ở bước gather), sai số ≤ 0.01: {same}")

    # 3) v1.2 từ chối kho đếm và sai schema
    log.append("\n## 3. Mã 2 cho kho đếm / sai schema")
    for name, bad in (("dem", {"items": {"ca_linh": 2}}), ("trung-id", {"items": [{"id": "I1", "kind": "ca_loc", "fresh": 5}] * 2}),
                      ("kind-la", {"items": [{"id": "I1", "kind": "ca_map", "fresh": 5}]}),
                      ("fresh-ngoai-mien", {"items": [{"id": "I1", "kind": "ca_loc", "fresh": 120}]})):
        code = run("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", write(j(name + ".json"), bad),
                   "--out", j("bad.jsonl"))
        ok &= code == 2

    # 4) day: bàn giao trong bộ nhớ + tất định cùng seed
    log.append("\n## 4. day --days 2 --seed 7 --ticks 30000: chạy hai lần, so byte")
    digests = []
    for i in (1, 2):
        ok &= run("--mode", "day", "--days", "2", "--seed", "7", "--ticks", "30000", "--out", j(f"d{i}.jsonl")) == 0
        with open(j(f"d{i}.jsonl"), "rb") as f:
            digests.append(hashlib.sha256(f.read()).hexdigest()[:16])
    names = {}
    for r in rows(j("d1.jsonl")):
        if r["type"] == "event":
            names[r["name"]] = names.get(r["name"], 0) + 1
    log.append(f"  sha256 {digests[0]} / {digests[1]} — giống: {digests[0] == digests[1]}")
    log.append("  event: " + json.dumps({k: names[k] for k in sorted(names) if k.startswith(("current", "gather_end", "quan_end", "spoiled", "shop"))}, ensure_ascii=False))
    ok &= digests[0] == digests[1]

    log.append(f"\nKẾT LUẬN: {'PASS' if ok else 'FAIL'}")

with open(os.path.join(HERE, "smoke-p3.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(log) + "\n")
print("\n".join(log))
sys.exit(0 if ok else 1)
