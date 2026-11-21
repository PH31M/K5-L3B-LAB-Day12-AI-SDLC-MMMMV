"""Soak test 10 Ngày headless bằng bot tất định (PRD Phase 4 §2, Ticket 02).

    python3 tools/soak.py --seed 7 --days 10 --out docs/proof/phase-4/soak.json

Chạy 10 Ngày liên tiếp trong một tiến trình:
- Qua đủ gather -> quan -> shop mỗi Ngày.
- Tiền, earned, uy tín, cấp nâng cấp tiếp tục xuyên suốt các Ngày.
- D1-D5 lặp lại ở D6-D10.
- Kết quả ghi ra file JSON gồm: days, days_completed, crashes, results, duration_s.

Mã thoát: 0 OK · 2 tham số sai · 1 lỗi chạy / crash.
"""

import argparse
import json
import math
import os
import sys
import time

# Đảm bảo root repo nằm trong sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from chonoi.contract import load_contract
from chonoi.errors import BadInput
from chonoi.inputs import InputState
from chonoi.runner import Session
from chonoi.scenario import load_scenario


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write(f"lỗi: {message}\n")
        sys.exit(2)


def _int(name):
    def conv(s):
        try:
            return int(s)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{name} phải là số nguyên")
    return conv


def bot_gather_input(gather_sim, plan, tick_in_phase):
    px, pd = gather_sim.pos
    dock_pos = gather_sim.t["dock_pos"]
    dock_radius = gather_sim.t["dock_radius"]

    # Thu hoạch đủ hàng hoặc sắp hết oxy / quá thời gian ca thì về bến
    if len(gather_sim.hold) >= 6 or gather_sim.oxygen_ticks <= 400 or tick_in_phase >= 1500:
        if pd > 1.0 and gather_sim.oxygen_ticks <= 400:
            return InputState(move=(0.0, -1.0), held=set(), edges=set())
        dx = dock_pos[0] - px
        dd = dock_pos[1] - pd
        dist = math.hypot(dx, dd)
        if dist <= dock_radius * 0.7:
            return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})
        if dist > 0:
            return InputState(move=(dx / dist, dd / dist), held=set(), edges=set())
        return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})

    needed_kinds = set(plan.get("ingredients", {}).keys())

    # Bắt cá nếu oxy dồi dào
    if gather_sim.oxygen_ticks > 800:
        target_fish = [f for f in gather_sim.fish if f.get("kind") in needed_kinds or len(gather_sim.hold) == 0]
        if target_fish:
            best_fish = min(target_fish, key=lambda f: math.hypot(f["pos"][0] - px, f["pos"][1] - pd))
            fx, fd = best_fish["pos"]
            dx, dd = fx - px, fd - pd
            dist = math.hypot(dx, dd)
            if dist <= gather_sim.t["catch_radius"] and not gather_sim._at_surface() and gather_sim.catch_cd_ticks == 0:
                return InputState(move=(0.0, 0.0), held=set(), edges={"catch"})
            if dist > 0:
                return InputState(move=(dx / dist, dd / dist), held=set(), edges=set())

    # Hái nút thực vật tại mặt nước
    ready_nodes = [n for n in gather_sim.nodes if n["regrow_ticks"] == 0]
    if ready_nodes:
        best_node = min(ready_nodes, key=lambda n: math.hypot(n["pos"][0] - px, n["pos"][1] - pd))
        nx, nd = best_node["pos"]
        dx, dd = nx - px, nd - pd
        dist = math.hypot(dx, dd)
        if dist <= gather_sim.t["interact_radius"] and gather_sim._at_surface():
            return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})
        if dist > 0:
            return InputState(move=(dx / dist, dd / dist), held=set(), edges=set())

    return InputState(move=(1.0, 0.0), held=set(), edges=set())


def bot_quan_input(quan_sim):
    px, pz = quan_sim.pos

    # 1. Đang cầm món -> bưng ra đúng bàn của khách
    if quan_sim.hand is not None:
        target_cid = quan_sim.hand["order_id"]
        customer = next((c for c in quan_sim.customers if c["id"] == target_cid), None)
        if customer:
            table = next((tb for tb in quan_sim.tables if tb["id"] == customer["table_id"]), None)
            if table:
                tx, tz = table["pos"]
                dist = math.hypot(tx - px, tz - pz)
                if dist <= 1.2:
                    return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})
                return InputState(move=((tx - px) / dist, (tz - pz) / dist), held=set(), edges=set())

    # 2. Tay trống:
    # A. Bếp có món chín -> lại lấy món
    ready_stove = next((s for s in quan_sim.stoves if s["state"] == "ready"), None)
    if ready_stove:
        sx, sz = ready_stove["pos"]
        dist = math.hypot(sx - px, sz - pz)
        if dist <= 1.2:
            return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})
        return InputState(move=((sx - px) / dist, (sz - pz) / dist), held=set(), edges=set())

    # B. Bếp rảnh và có khách đang đợi đã giữ chỗ -> bật bếp nấu
    idle_stove = next((s for s in quan_sim.stoves if s["state"] == "idle"), None)
    waiting_customer = next((c for c in quan_sim.customers if c["state"] == "waiting" and c["order_status"] == "reserved"), None)
    if idle_stove and waiting_customer:
        sx, sz = idle_stove["pos"]
        dist = math.hypot(sx - px, sz - pz)
        if dist <= 1.2:
            return InputState(move=(0.0, 0.0), held=set(), edges={"interact"})
        return InputState(move=((sx - px) / dist, (sz - pz) / dist), held=set(), edges=set())

    # Mặc định: di chuyển về trung tâm sảnh để đón khách / trực bếp
    cx, cz = 3.5, 5.0
    dist = math.hypot(cx - px, cz - pz)
    if dist > 0.5:
        return InputState(move=((cx - px) / dist, (cz - pz) / dist), held=set(), edges=set())
    return InputState(move=(0.0, 0.0), held=set(), edges=set())


def bot_shop_input(shop_sim):
    # Mua nâng cấp có thể chi trả
    for upgrade_name in ("oxygen", "hp", "net"):
        levels = shop_sim.catalog.get(upgrade_name, [])
        curr_lvl = shop_sim.upgrades.get(upgrade_name, 0)
        if curr_lvl < len(levels):
            price = levels[curr_lvl]["price"]
            if shop_sim.money >= price:
                return InputState(move=(0.0, 0.0), held=set(), edges={"shop_done"}, buy=upgrade_name)
    return InputState(move=(0.0, 0.0), held=set(), edges={"shop_done"})


def write_soak_output(out_path, days, days_completed, crashes, results, duration_s):
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    payload = {
        "days": days,
        "days_completed": days_completed,
        "crashes": crashes,
        "results": results,
        "duration_s": round(duration_s, 3),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return payload


def main(argv=None) -> int:
    p = _Parser(prog="soak.py", description="Soak test 10 Ngày headless bằng bot tất định.")
    p.add_argument("--seed", type=_int("seed"), default=7)
    p.add_argument("--days", type=_int("days"), default=10)
    p.add_argument("--out", default="soak.json")
    p.add_argument("--scenario")
    a = p.parse_args(argv)

    if a.days <= 0:
        sys.stderr.write("lỗi: --days phải > 0\n")
        return 2

    try:
        contract = load_contract()
        tuning = contract["tuning"]
        scenario = load_scenario(a.scenario, "day", tuning) if a.scenario else {}
    except BadInput as e:
        sys.stderr.write(f"lỗi đầu vào: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"lỗi khởi tạo: {e}\n")
        return 1

    try:
        session = Session("day", tuning, scenario, seed=a.seed, days=a.days)
    except Exception as e:
        sys.stderr.write(f"lỗi dựng sim: {e}\n")
        return 1

    t0 = time.perf_counter()
    results = []
    crashes = 0
    ticks = 0

    while not session.done:
        ticks += 1
        phase = session.sim.phase
        day = session.sim.day
        try:
            if phase == "gather":
                inp = bot_gather_input(session.sim.inner, session.sim.plan, session.phase_tick)
            elif phase == "quan":
                inp = bot_quan_input(session.sim.inner)
            else:
                inp = bot_shop_input(session.sim.inner)

            if phase == "shop":
                events = session.step(inp)
                if any(e["name"] == "shop_end" for e in events):
                    mult = tuning["score"]["reputation_multiplier"]
                    score = session.sim.earned + mult * math.floor(session.sim.reputation)
                    results.append({
                        "day": day,
                        "earned": session.sim.earned,
                        "reputation": round(float(session.sim.reputation), 2),
                        "score": score,
                    })
                continue

            session.step(inp)
        except Exception as e:
            crashes += 1
            sys.stderr.write(f"crash tại tick {ticks} (ngày {day}, pha {phase}): {e}\n")
            # Ghi ngay kết quả dở dang để không mất file output
            wall_s = time.perf_counter() - t0
            write_soak_output(a.out, a.days, session.sim.days_completed, crashes, results, wall_s)
            return 1

    wall_s = time.perf_counter() - t0
    payload = write_soak_output(a.out, a.days, session.sim.days_completed, crashes, results, wall_s)
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if session.sim.days_completed == a.days and crashes == 0:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
