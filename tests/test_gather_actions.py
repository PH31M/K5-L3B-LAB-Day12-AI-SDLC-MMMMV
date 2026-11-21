"""Unit tests cho Lát 2: Gather Actions (Hái nút, bắt cá, cập bến).

Tác giả: Trần Đình Nhật Minh (@trandinhnhatminh1452)
Ticket: docs/tickets/phase-1/03-gather-actions.md
"""

import unittest

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.sim.gather import GatherSim


def _make_sim(scenario_override=None):
    tuning = load_contract()["tuning"]
    sc = {
        "player": {"pos": [20.0, 0.0], "vel": [0.0, 0.0]},
        "hold": [],
        "nodes": [],
        "fish": [],
        "time_left_ticks": 1000,
    }
    if scenario_override:
        sc.update(scenario_override)
    streams = Streams(1)
    ids = IdAllocator()
    return GatherSim(tuning, sc, streams, ids)


def _input(interact=False, catch=False, move=(0.0, 0.0)):
    held = {"interact": interact, "catch": catch}
    edges = set()
    if interact:
        edges.add("interact")
    if catch:
        edges.add("catch")
    return InputState(list(move), held, edges)


class GatherActionsTest(unittest.TestCase):
    def test_dock_priority_over_gather(self):
        """Interact ở bến kích hoạt cập bến trước mọi xử lý hái, kể cả khi có nút trong tầm."""
        sim = _make_sim({
            "player": {"pos": [2.0, 0.0]},  # Ngay tại dock_pos [2, 0]
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [2.0, 0.0], "regrow_ticks": 0}],
        })
        events = sim.step(_input(interact=True))
        self.assertTrue(sim.done)
        self.assertEqual(sim.reason, "docked")
        end_events = [e for e in events if e[0] == "gather_end"]
        self.assertEqual(len(end_events), 1)
        self.assertEqual(end_events[0][1]["reason"], "docked")
        # Không được phát event gather
        self.assertFalse(any(e[0] == "gather" for e in events))
        # Nút vẫn giữ nguyên
        self.assertEqual(sim.nodes[0]["regrow_ticks"], 0)

    def test_gather_node_success_at_surface(self):
        """Hái nút ready thành công ở mặt nước: thêm vào giỏ, regrow 1200 tick, phát gather."""
        sim = _make_sim({
            "player": {"pos": [20.0, 0.2]},  # Mặt nước (d <= 0.5)
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [21.0, 0.0], "regrow_ticks": 0}],
        })
        events = sim.step(_input(interact=True))
        gather_events = [e for e in events if e[0] == "gather"]
        self.assertEqual(len(gather_events), 1)
        self.assertEqual(gather_events[0][1], {
            "node_id": "N1",
            "kind": "bong_dien_dien",
            "amount": 1,
        })
        self.assertEqual(sim.hold, ["bong_dien_dien"])
        self.assertEqual(sim.nodes[0]["regrow_ticks"], 1200)

    def test_gather_node_ignored_underwater(self):
        """Interact gần nút khi đang lặn (d > surface_depth) không được hái."""
        sim = _make_sim({
            "player": {"pos": [20.0, 1.0]},  # Lặn sâu d = 1.0 > 0.5
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [20.0, 1.0], "regrow_ticks": 0}],
        })
        events = sim.step(_input(interact=True))
        self.assertFalse(any(e[0] == "gather" for e in events))
        self.assertEqual(sim.hold, [])
        self.assertEqual(sim.nodes[0]["regrow_ticks"], 0)

    def test_gather_tie_break_by_id_key(self):
        """Hòa khoảng cách: chọn id nhỏ hơn theo id_key (N2 trước N10)."""
        sim = _make_sim({
            "player": {"pos": [20.0, 0.0]},
            "nodes": [
                {"id": "N10", "kind": "bong_sung", "pos": [21.0, 0.0], "regrow_ticks": 0},
                {"id": "N2", "kind": "bong_dien_dien", "pos": [19.0, 0.0], "regrow_ticks": 0},
            ],
        })
        # Cả N10 và N2 đều cách 1.0m, N2 có id_key nhỏ hơn N10
        events = sim.step(_input(interact=True))
        gather_events = [e for e in events if e[0] == "gather"]
        self.assertEqual(len(gather_events), 1)
        self.assertEqual(gather_events[0][1]["node_id"], "N2")

    def test_gather_hold_full(self):
        """Giỏ đầy: phát hold_full {action: 'gather', node_id, required, free: 0}, nút giữ nguyên."""
        sim = _make_sim({
            "player": {"pos": [20.0, 0.0]},
            "hold": ["ca_loc"] * 12,  # Đầy sức chứa 12
            "nodes": [{"id": "N1", "kind": "bong_sung", "pos": [20.5, 0.0], "regrow_ticks": 0}],
        })
        events = sim.step(_input(interact=True))
        hold_full_events = [e for e in events if e[0] == "hold_full"]
        self.assertEqual(len(hold_full_events), 1)
        self.assertEqual(hold_full_events[0][1], {
            "action": "gather",
            "node_id": "N1",
            "required": 1,
            "free": 0,
        })
        self.assertEqual(sim.nodes[0]["regrow_ticks"], 0)  # Giữ nguyên không đặt regrow
        self.assertEqual(len(sim.hold), 12)

    def test_node_regrown_event_and_regather(self):
        """Nút về 0 phát node_regrown và hái lại được ngay bước đó."""
        sim = _make_sim({
            "player": {"pos": [20.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_sung", "pos": [20.5, 0.0], "regrow_ticks": 1}],
        })
        # Ở tick này regrow_ticks giảm từ 1 về 0 -> phát node_regrown và interact hái luôn
        events = sim.step(_input(interact=True))
        event_names = [e[0] for e in events]
        self.assertIn("node_regrown", event_names)
        self.assertIn("gather", event_names)
        self.assertEqual(sim.hold, ["bong_sung"])

    def test_catch_fish_success(self):
        """Bắt cá thành công dưới nước: xóa đàn, yield đúng loài, hồi chiêu 30 tick."""
        sim = _make_sim({
            "player": {"pos": [20.0, 5.0]},  # Dưới nước
            "fish": [{"id": "F1", "kind": "ca_linh", "pos": [21.0, 5.0], "heading_deg": 0}],
        })
        events = sim.step(_input(catch=True))
        caught_events = [e for e in events if e[0] == "fish_caught"]
        self.assertEqual(len(caught_events), 1)
        self.assertEqual(caught_events[0][1], {
            "fish_id": "F1",
            "kind": "ca_linh",
            "yield": 3,
        })
        self.assertEqual(sim.hold, ["ca_linh", "ca_linh", "ca_linh"])
        self.assertEqual(len(sim.fish), 0)  # Đàn cá đã bị xóa
        self.assertEqual(sim.catch_cd_ticks, 30)  # 0.5s * 60

    def test_catch_fish_ignored_at_surface(self):
        """Ở mặt nước (d <= surface_depth) không thể bắt cá."""
        sim = _make_sim({
            "player": {"pos": [20.0, 0.2]},  # Mặt nước
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [20.0, 0.2], "heading_deg": 0}],
        })
        events = sim.step(_input(catch=True))
        self.assertFalse(any(e[0] == "fish_caught" for e in events))
        self.assertEqual(sim.hold, [])
        self.assertEqual(len(sim.fish), 1)
        self.assertEqual(sim.catch_cd_ticks, 0)

    def test_catch_fish_on_cooldown_ignored(self):
        """Đang hồi chiêu (catch_cd_ticks > 0) không thể bắt cá."""
        sim = _make_sim({
            "player": {"pos": [20.0, 5.0], "catch_cd_ticks": 10},
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [20.0, 5.0], "heading_deg": 0}],
        })
        # Bước này catch_cd_ticks giảm 10 -> 9 ở đầu bước
        events = sim.step(_input(catch=True))
        self.assertFalse(any(e[0] == "fish_caught" for e in events))
        self.assertEqual(len(sim.fish), 1)
        self.assertEqual(sim.catch_cd_ticks, 9)

    def test_catch_fish_hold_full(self):
        """Giỏ không đủ chỗ chứa toàn bộ yield: phát hold_full, giữ đàn cá, không hồi chiêu."""
        sim = _make_sim({
            "player": {"pos": [20.0, 5.0]},
            "hold": ["ca_loc"] * 10,  # Sức chứa 12, còn trống 2 slot
            "fish": [{"id": "F1", "kind": "ca_linh", "pos": [20.5, 5.0], "heading_deg": 0}],  # yield = 3
        })
        events = sim.step(_input(catch=True))
        hold_full_events = [e for e in events if e[0] == "hold_full"]
        self.assertEqual(len(hold_full_events), 1)
        self.assertEqual(hold_full_events[0][1], {
            "action": "catch",
            "fish_id": "F1",
            "required": 3,
            "free": 2,
        })
        self.assertEqual(len(sim.fish), 1)  # Giữ đàn
        self.assertEqual(sim.catch_cd_ticks, 0)  # Không đặt hồi chiêu

    def test_catch_fish_tie_break_by_id_key(self):
        """Hòa khoảng cách đàn cá: chọn id nhỏ hơn theo id_key."""
        sim = _make_sim({
            "player": {"pos": [20.0, 5.0]},
            "fish": [
                {"id": "F2", "kind": "ca_loc", "pos": [21.0, 5.0], "heading_deg": 0},
                {"id": "F1", "kind": "ca_loc", "pos": [19.0, 5.0], "heading_deg": 0},
            ],
        })
        events = sim.step(_input(catch=True))
        caught = [e for e in events if e[0] == "fish_caught"]
        self.assertEqual(len(caught), 1)
        self.assertEqual(caught[0][1]["fish_id"], "F1")


if __name__ == "__main__":
    unittest.main()
