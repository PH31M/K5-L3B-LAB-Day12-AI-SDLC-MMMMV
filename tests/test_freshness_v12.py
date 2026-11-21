"""Phase 3 (TICKET-03, contract v1.2): kho cá thể, độ tươi, giữ chỗ theo id, giá theo tươi, bàn giao, dòng lũ.

Hộp đen qua `headless_cmd` + JSONL/file kho (ticket 06 QA). Số liệu ngưỡng tính bằng units (1 điểm = 240):
giỏ hao 2 units/tick, kho quán 1 unit/tick, ươn khi < 7200 units (fresh 30).
"""

import json
import unittest

from helpers import Workdir, events, frames, individuals, read_jsonl, run_headless, snapshots, write_json

G1 = 2 / 240   # hao một bước trong giỏ
Q1 = 1 / 240   # hao một bước trong kho quán


def item(ident, kind, fresh):
    return {"id": ident, "kind": kind, "fresh": fresh}


class Base(unittest.TestCase):
    def headless(self, w, mode, scenario=None, inputs=None, ticks=1, every=1, extra=(), name="o"):
        args = ["--mode", mode, "--seed", "1", "--ticks", str(ticks), "--snapshot-every", str(every),
                "--out", w.path(name + ".jsonl"), *extra]
        if scenario is not None:
            args += ["--scenario", write_json(w.path(name + "-sc.json"), scenario)]
        if inputs is not None:
            args += ["--inputs", write_json(w.path(name + "-in.json"), frames(*inputs))]
        code, err = run_headless(*args)
        self.assertEqual(code, 0, err)
        return read_jsonl(w.path(name + ".jsonl"))

    def exit_code(self, w, mode, scenario=None, extra=()):
        args = ["--mode", mode, "--seed", "1", "--ticks", "0", "--out", w.path("bad.jsonl"), *extra]
        if scenario is not None:
            args += ["--scenario", write_json(w.path("bad-sc.json"), scenario)]
        return run_headless(*args)[0]


class Gather(Base):
    def test_ticket_fixture_fresh_30_spoils_at_tick_1(self):
        """Fixture nguyên văn trong TICKET-03: một bước không input -> spoiled ở tick 1."""
        sc = {"gather": {"hold": [item("I1", "ca_linh", 30)], "random_fish": False, "monsters": []}}
        with Workdir() as w:
            rows = self.headless(w, "gather", sc)
        self.assertEqual(events(rows, "spoiled"),
                         [{"type": "event", "tick": 1, "phase": "gather", "name": "spoiled",
                           "data": {"item_id": "I1", "kind": "ca_linh", "location": "hold"}}])
        self.assertEqual(snapshots(rows)[-1]["hold_count"], 1)  # ươn vẫn chiếm ô

    def test_spoiled_once_per_item_in_id_order_and_not_again(self):
        sc = {"gather": {"hold": [item("I10", "ca_loc", 30), item("I2", "ca_linh", 30), item("I3", "ca_keo", 29)],
                         "random_fish": False, "monsters": []}}
        with Workdir() as w:
            rows = self.headless(w, "gather", sc, ticks=30)
        self.assertEqual([(e["tick"], e["data"]["item_id"]) for e in events(rows, "spoiled")],
                         [(1, "I2"), (1, "I10")])

    def test_new_items_start_at_100_and_ids_continue_after_fixture(self):
        sc = {"gather": {"player": {"pos": [50, 5]}, "hold": [item("I7", "bong_sung", 80)],
                         "fish": [{"id": "F1", "kind": "ca_linh", "pos": [50, 5]}],
                         "random_fish": False, "monsters": []}}
        with Workdir() as w:
            rows = self.headless(w, "gather", sc, [{"tick": 0, "catch": True}], ticks=2)
        snaps = snapshots(rows)
        self.assertEqual([(i["id"], i["fresh"]) for i in snaps[1]["hold"][1:]],
                         [("I8", 100), ("I9", 100), ("I10", 100)])  # hàng mới chưa hao trong bước nhận
        self.assertAlmostEqual(snaps[2]["hold"][1]["fresh"], 100 - G1, delta=0.01)
        self.assertAlmostEqual(snaps[1]["hold"][0]["fresh"], 80 - G1, delta=0.01)

    def test_bad_hold_schema_exit_2(self):
        bad_holds = (["ca_loc"], [item("I1", "ca_loc", 30.5), item("I1", "ca_loc", 40)],
                     [item("I1", "ca_la", 50)], [item("I1", "ca_loc", -1)], [item("", "ca_loc", 5)],
                     [{"id": "I1", "kind": "ca_loc"}])
        with Workdir() as w:
            for hold in bad_holds:
                with self.subTest(hold=hold):
                    self.assertEqual(self.exit_code(w, "gather", {"gather": {"hold": hold}}), 2)


class Handoff(Base):
    def test_two_process_handoff_keeps_id_kind_and_exact_freshness(self):
        """Smoke bàn giao trong TICKET-03: cập bến frame 0, quán --ticks 0 đọc đúng id/kind/fresh."""
        sc = {"gather": {"hold": [item("I1", "ca_linh", 100), item("I2", "ca_loc", 31.5)],
                         "random_fish": False, "monsters": []}}
        with Workdir() as w:
            inv = w.path("kho.json")
            self.headless(w, "gather", sc, [{"tick": 0, "interact": True}], ticks=5,
                          extra=("--inventory-out", inv), name="g")
            with open(inv, encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(saved, {"items": [item("I1", "ca_linh", 100 - G1), item("I2", "ca_loc", 31.5 - G1)]})
            rows = self.headless(w, "quan", ticks=0, extra=("--inventory", inv), name="q")
        stock = snapshots(rows)[0]["stock"]
        self.assertEqual([(i["id"], i["kind"]) for i in stock], [("I1", "ca_linh"), ("I2", "ca_loc")])
        for got, want in zip(stock, saved["items"]):
            self.assertAlmostEqual(got["fresh"], want["fresh"], delta=0.01)

    def test_handoff_at_threshold_keeps_branch(self):
        """fresh đọc lại từ file đủ chính xác: 7201 units sau gather vẫn chưa ươn, ươn ở bước quán thứ 2."""
        sc = {"gather": {"hold": [item("I1", "ca_loc", 7203 / 240)], "random_fish": False, "monsters": []}}
        with Workdir() as w:
            inv = w.path("kho.json")
            self.headless(w, "gather", sc, [{"tick": 0, "interact": True}], extra=("--inventory-out", inv), name="g")
            rows = self.headless(w, "quan", ticks=3, extra=("--inventory", inv), name="q")
        self.assertEqual([(e["tick"], e["data"]) for e in events(rows, "spoiled")],
                         [(2, {"item_id": "I1", "kind": "ca_loc", "location": "stock"})])

    def test_faint_writes_empty_inventory_and_tick_limit_keeps_target(self):
        sc = {"gather": {"player": {"pos": [20, 10], "oxygen_ticks": 0, "zero_oxy_ticks": 59, "hp": 1},
                         "hold": individuals(["ca_loc"]), "random_fish": False, "monsters": []}}
        with Workdir() as w:
            inv = w.path("kho.json")
            self.headless(w, "gather", sc, extra=("--inventory-out", inv))
            with open(inv, encoding="utf-8") as f:
                self.assertEqual(json.load(f), {"items": []})
            other = w.path("keep.json")
            with open(other, "w", encoding="utf-8") as f:
                f.write("giữ nguyên")
            self.headless(w, "gather", {"gather": {"hold": individuals(["ca_loc"])}}, ticks=2,
                          extra=("--inventory-out", other), name="t")
            with open(other, encoding="utf-8") as f:
                self.assertEqual(f.read(), "giữ nguyên")

    def test_v12_rejects_counted_inventory_and_bad_individuals(self):
        ok = item("I1", "ca_loc", 50)
        with Workdir() as w:
            for bad in ({"items": {"ca_loc": 1}}, {"items": {}}, {"items": [ok, ok]},
                        {"items": [dict(ok, fresh=float("nan"))]}, {"items": [dict(ok, fresh=100.5)]}):
                with self.subTest(bad=bad):
                    p = w.path("inv.json")
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump(bad, f)
                    self.assertEqual(self.exit_code(w, "quan", extra=("--inventory", p)), 2)


class Quan(Base):
    def test_stock_decays_including_reserved_and_spoiled_event_location_stock(self):
        sc = {"quan": {"stock": [item("I1", "ca_loc", 30), item("I2", "bong_sung", 50)],
                       "random_customers": False}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, ticks=2)
        self.assertEqual([(e["tick"], e["data"]) for e in events(rows, "spoiled")],
                         [(1, {"item_id": "I1", "kind": "ca_loc", "location": "stock"})])
        self.assertAlmostEqual(snapshots(rows)[-1]["stock"][1]["fresh"], 50 - 2 * Q1, delta=0.01)

    def test_reserved_item_spoils_then_rereserve_once_freshest(self):
        sc = {"quan": {"random_customers": False,
                       "stock": [item("I1", "ca_loc", 30), item("I2", "ca_loc", 50), item("I3", "ca_loc", 40)],
                       "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                      "reserved": ["I1"]}]}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, ticks=1)
        guest = snapshots(rows)[-1]["customers"][0]
        self.assertEqual((guest["order_status"], guest["reserved"]), ("reserved", ["I2"]))
        self.assertEqual(snapshots(rows)[0]["customers"][0]["reserved"], ["I1"])

    def test_rereserve_by_order_tick_then_table_and_unfulfillable(self):
        sc = {"quan": {"random_customers": False,
                       "stock": [item("I1", "ca_loc", 30), item("I2", "ca_loc", 30), item("I3", "ca_loc", 60)],
                       "customers": [
                           {"id": "C1", "table_id": "T2", "dish_id": "ca_loc_nuong_trui", "order_tick": 5,
                            "reserved": ["I1"]},
                           {"id": "C2", "table_id": "T1", "dish_id": "ca_loc_nuong_trui", "order_tick": 5,
                            "reserved": ["I2"]}]}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, ticks=3)
        by_id = {c["id"]: c for c in snapshots(rows)[-1]["customers"]}
        self.assertEqual((by_id["C2"]["order_status"], by_id["C2"]["reserved"]), ("reserved", ["I3"]))
        self.assertEqual((by_id["C1"]["order_status"], by_id["C1"]["reserved"]), ("unfulfillable", []))
        self.assertEqual(by_id["C1"]["state"], "waiting")  # khách vẫn chờ tới hạn

    def test_cook_consumes_reserved_ids_and_price_floors_on_average_freshness(self):
        # Mặc định: giữ 3 cá linh tươi nhất (I4 95, I5 90, I2 70) + I9; I3 (60) còn lại trong kho.
        sc = {"quan": {"player": {"pos": [2, 8]}, "random_customers": False,
                       "stock": [item("I5", "ca_linh", 90), item("I2", "ca_linh", 70),
                                 item("I9", "bong_dien_dien", 55), item("I3", "ca_linh", 60),
                                 item("I4", "ca_linh", 95)],
                       "customers": [{"id": "C1", "table_id": "T1", "dish_id": "lau_ca_linh_dien_dien",
                                      "patience_ticks_left": 3600}]}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, [{"tick": 0, "interact": True}], ticks=1)
        self.assertEqual(snapshots(rows)[0]["customers"][0]["reserved"], ["I9", "I2", "I4", "I5"])
        data = events(rows, "cook_started")[0]["data"]
        self.assertEqual([(i["kind"], i["id"]) for i in data["items"]],
                         [("bong_dien_dien", "I9"), ("ca_linh", "I2"), ("ca_linh", "I4"), ("ca_linh", "I5")])
        # floor(120 × (95+90+70+55 − 4/240)/4 / 100) = floor(92.995) = 92
        self.assertEqual(data["base_price"], 92)
        self.assertEqual([i["id"] for i in snapshots(rows)[-1]["stock"]], ["I3"])

    def test_spoiled_stock_is_not_offered_to_new_customers(self):
        sc = {"quan": {"stock": [item("I1", "ca_loc", 29), item("I2", "bong_sung", 10), item("I3", "bong_sung", 20)]}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, ticks=121)
        self.assertEqual(events(rows, "customer_arrived"), [])
        self.assertEqual([e["tick"] for e in events(rows, "no_dish")], [120])

    def test_pause_freezes_decay(self):
        sc = {"quan": {"stock": [item("I1", "ca_loc", 50)], "random_customers": False}}
        with Workdir() as w:
            rows = self.headless(w, "quan", sc, [{"tick": 0, "pause": True}, {"tick": 1, "pause": False},
                                                 {"tick": 5, "pause": True}], ticks=6)
        fresh = [s["stock"][0]["fresh"] for s in snapshots(rows)]
        self.assertEqual(fresh[:6], [50] * 6)
        self.assertAlmostEqual(fresh[6], 50 - Q1, delta=0.01)

    def test_bad_reserved_fixture_exit_2(self):
        stock = [item("I1", "ca_loc", 50), item("I2", "ca_loc", 20)]
        guest = {"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui"}
        with Workdir() as w:
            for reserved in ({"ca_loc": 1}, ["I9"], ["I2"], ["I1", "I1"]):
                with self.subTest(reserved=reserved):
                    sc = {"quan": {"stock": stock, "customers": [dict(guest, reserved=reserved)]}}
                    self.assertEqual(self.exit_code(w, "quan", sc), 2)
            shared = {"quan": {"stock": stock, "customers": [dict(guest, reserved=["I1"]),
                                                             dict(guest, id="C2", table_id="T2", reserved=["I1"])]}}
            self.assertEqual(self.exit_code(w, "quan", shared), 2)
            short = {"quan": {"stock": stock, "customers": [guest, dict(guest, id="C2", table_id="T2")]}}
            self.assertEqual(self.exit_code(w, "quan", short), 2)  # chỉ 1 cá lóc chưa ươn cho 2 đơn


class Day(Base):
    def test_day_handoff_same_tick_and_next_day_new_ids(self):
        sc = {"gather": {"hold": [item("I1", "ca_loc", 100)], "time_left_ticks": 1,
                         "random_fish": False, "monsters": []},
              "quan": {"time_left_ticks": 1, "random_customers": False}}
        with Workdir() as w:
            rows = self.headless(w, "day", sc, [{"tick": 2, "shop_done": True}], ticks=6,
                                 extra=("--days", "2"))
        snaps = {s["tick"]: s for s in snapshots(rows)}
        self.assertEqual(snaps[1]["phase"], "quan")
        self.assertEqual(snaps[1]["stock"], [item("I1", "ca_loc", round(100 - G1, 3))])  # không hao thêm
        self.assertEqual(snaps[3]["phase"], "gather")
        self.assertEqual(snaps[3]["hold"], [item("I2", "ca_loc", 100)])  # Ngày 2: id mới, fresh ban đầu
        end = events(rows, "gather_end")[1]["data"]["inventory"]["items"]
        self.assertEqual([i["id"] for i in end], ["I2"])


class Current(Base):
    def test_schedule_events_and_snapshot_on_real_manifest(self):
        sc = {"gather": {"player": {"pos": [50, 0]}, "random_fish": False, "monsters": [],
                         "current_direction": 1}}
        with Workdir() as w:
            rows = self.headless(w, "gather", sc, ticks=2281, every=600)
        got = [(e["tick"], e["name"], e["data"]) for e in events(rows) if e["name"].startswith("current_")]
        self.assertEqual(got, [(1680, "current_warning", {"starts_at_phase_tick": 1800}),
                               (1800, "current_start", {"direction": 1, "duration_ticks": 480}),
                               (2280, "current_end", {"direction": 1, "reason": "elapsed"})])
        snaps = {s["tick"]: s for s in snapshots(rows)}
        self.assertEqual(snaps[1800]["current"], {"direction": 1, "ticks_left": 480})
        self.assertIsNone(snaps[1200]["current"])

    def test_random_current_false_and_bad_direction(self):
        with Workdir() as w:
            rows = self.headless(w, "gather", {"gather": {"random_current": False, "random_fish": False,
                                                          "monsters": []}}, ticks=1801, every=1801)
            self.assertFalse([e for e in events(rows) if e["name"].startswith("current_")])
            self.assertEqual(self.exit_code(w, "gather", {"gather": {"current_direction": 0}}), 2)
            self.assertEqual(self.exit_code(w, "gather", {"gather": {"random_current": "no"}}), 2)


class Manifest(unittest.TestCase):
    def test_manifest_has_v12_blocks_and_validates_ranges(self):
        import copy
        from helpers import ROOT
        from chonoi.contract import load_contract
        from chonoi.errors import BadInput
        with open(f"{ROOT}/game.contract.json", encoding="utf-8") as f:
            base = json.load(f)
        self.assertEqual(base["freshness"], {"initial": 100, "gather_decay_per_s": 0.5,
                                             "quan_decay_per_s": 0.25, "spoiled_below": 30})
        self.assertIn("current", base["extensions"])
        self.assertEqual(base["tuning"]["gather"]["current"], {"interval_ticks": 1800, "duration_ticks": 480,
                                                               "warning_ticks": 120, "min_depth": 10, "speed": 1.5})
        self.assertEqual(load_contract()["tuning"]["freshness"], base["freshness"])
        bads = [lambda c: c.pop("freshness"), lambda c: c["freshness"].update(spoiled_below=101),
                lambda c: c["freshness"].update(extra=1), lambda c: c["tuning"]["gather"].pop("current"),
                lambda c: c["tuning"]["gather"]["current"].update(duration_ticks=1800)]
        with Workdir() as w:
            for i, mutate in enumerate(bads):
                with self.subTest(case=i):
                    c = copy.deepcopy(base)
                    mutate(c)
                    path = write_json(w.path(f"c{i}.json"), c)
                    with self.assertRaises(BadInput):
                        load_contract(path)


if __name__ == "__main__":
    unittest.main()
