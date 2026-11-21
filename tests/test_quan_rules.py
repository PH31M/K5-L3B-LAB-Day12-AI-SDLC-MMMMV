"""Test hộp đen cho luật `quan` Phase 1 (ticket 07, phần chờ ticket 01).

Bốn test này dựng trạng thái giữa chừng bằng `quan.customers` / `quan.hand` — những khóa
chưa được `scenario.py` hỗ trợ ở v1.0. Vì vậy chúng đang `skip`; khi ticket 01 merge thì
BỎ `@unittest.skip` (không phải viết lại gì khác).

Nguồn: PRD-0 §E/§F + docs/plan/phase-1-conformance.md §6.
"""

import json
import unittest

from helpers import Workdir, events, frames, read_jsonl, run_headless, snapshots, write_json


def tuning():
    with open("game.contract.json", encoding="utf-8") as f:
        return json.load(f)["tuning"]


class Base(unittest.TestCase):
    def run_quan(self, w, scenario=None, inputs=None, ticks=30, every="1", name="q", inventory=None):
        args = ["--mode", "quan", "--seed", "1", "--ticks", str(ticks),
                "--snapshot-every", every, "--out", w.path(name + ".jsonl")]
        if scenario is not None:
            args += ["--scenario", write_json(w.path("sc.json"), scenario)]
        if inputs is not None:
            args += ["--inputs", write_json(w.path("in.json"), frames(*inputs))]
        if inventory is not None:
            args += ["--inventory", inventory]
        code, err = run_headless(*args)
        self.assertEqual(code, 0, err)
        return read_jsonl(w.path(name + ".jsonl"))

    def snaps(self, rows):
        return {r["tick"]: r for r in snapshots(rows)}


@unittest.skip("chờ ticket 01: scenario.py chưa nhận customers[]/hand đầy đủ")
class Customers(Base):
    def test_khach_den_tick_120_va_giu_cho(self):
        """Không scenario: khách đầu đến ở tick 120, ngồi bàn trống id nhỏ nhất, giữ đúng công thức."""
        with Workdir() as w:
            rows = self.run_quan(w, ticks=200, every="1")
            arrived = events(rows, "customer_arrived")
            self.assertEqual([e["tick"] for e in arrived], [120], [e["tick"] for e in events(rows)])
            data = arrived[0]["data"]
            self.assertEqual(data["table_id"], "T1")
            snap = self.snaps(rows)[121]
            guest = [c for c in snap["customers"] if c["id"] == data["order_id"]][0]
            self.assertEqual(guest["order_status"], "reserved")
            self.assertEqual(guest["reserved"], tuning()["menu"][data["dish_id"]]["recipe"])
            self.assertEqual(snap["stock"], {})  # giữ chỗ không làm đổi tồn vật lý

    def test_het_kien_nhan_thi_roi_va_mat_uy_tin(self):
        """Khách chờ với kiên nhẫn 60 tick: rời ở tick 60, uy tín 3.0 → 2.5."""
        sc = {"quan": {"customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                      "patience_ticks_left": 60, "order_status": "reserved",
                                      "reserved": {"ca_loc": 1}}]}}
        with Workdir() as w:
            rows = self.run_quan(w, sc, ticks=70)
            left = events(rows, "customer_left")
            self.assertEqual(len(left), 1, [(e["name"], e["tick"]) for e in events(rows)])
            self.assertEqual((left[0]["tick"], left[0]["data"]["reason"]), (60, "patience"))
            self.assertAlmostEqual(left[0]["data"]["reputation"], 2.5, places=2)
            self.assertEqual(self.snaps(rows)[70]["customers"], [])


@unittest.skip("chờ ticket 01: scenario.py chưa nhận stoves[].state/ready_ticks + hand")
class Service(Base):
    def test_nau_dung_don_va_chin_sau_cook_s(self):
        """Đứng cạnh bếp, có đơn reserved: interact → cook_started (tiêu đúng nguyên liệu), 6 s sau dish_ready."""
        sc = {"quan": {"player": {"pos": [2, 8]},
                       "stock": {"ca_loc": 2},
                       "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                      "order_status": "reserved", "reserved": {"ca_loc": 1}}]}}
        with Workdir() as w:
            rows = self.run_quan(w, sc, [{"tick": 0, "interact": True}], ticks=400, every="30")
            started = events(rows, "cook_started")
            self.assertEqual(len(started), 1, [(e["name"], e["data"]) for e in events(rows)])
            data = started[0]["data"]
            self.assertEqual(data["dish_id"], "ca_loc_nuong_trui")
            self.assertEqual(data["items"], ["ca_loc"])
            self.assertEqual(data["base_price"], 60)
            self.assertEqual([e["tick"] for e in events(rows, "dish_ready")], [360])
            snap = self.snaps(rows)[400]
            self.assertEqual(snap["stock"], {"ca_loc": 1})  # đã tiêu 1 khi bắt đầu nấu
            self.assertEqual(snap["stoves"][0]["state"], "ready")

    def test_phuc_vu_dung_don_thi_tra_tien_va_boa(self):
        """Cầm đúng món, đứng cạnh bàn: served → sau 10 s paid = giá + boa 20%."""
        hand = {"order_id": "C1", "dish_id": "ca_loc_nuong_trui", "base_price": 60}
        sc = {"quan": {"player": {"pos": [9, 2]}, "hand": hand,
                       "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                      "order_status": "assigned", "reserved": {},
                                      "patience_ticks_left": 3600}]}}
        with Workdir() as w:
            rows = self.run_quan(w, sc, [{"tick": 0, "interact": True}], ticks=700, every="100")
            served = events(rows, "served")
            self.assertEqual(len(served), 1, [(e["name"], e["data"]) for e in events(rows)])
            self.assertEqual(served[0]["data"]["tip"], 12)  # floor(60 × 0.2)
            paid = events(rows, "paid")
            self.assertEqual(len(paid), 1)
            self.assertEqual(paid[0]["data"]["amount"], 72)
            self.assertEqual(paid[0]["data"]["reason"], "finished_eating")
            self.assertAlmostEqual(self.snaps(rows)[700]["reputation"], 3.2, places=2)


if __name__ == "__main__":
    unittest.main()
