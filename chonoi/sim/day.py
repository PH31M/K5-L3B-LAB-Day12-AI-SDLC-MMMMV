"""Chế độ `day` — KHUNG cho contract v1.1 (ticket 01).

Hiện chỉ chạy pha `gather` để `--mode day --ticks 0` có snapshot đúng schema.
Vòng ngày đầy đủ (gather → quan → shop → Ngày kế) là ticket 05; khi đó thay phần `step`
bằng máy trạng thái, giữ nguyên các trường snapshot dưới đây.
"""

from .gather import GatherSim

TICK = 60


class DaySim:
    mode = "day"

    def __init__(self, tuning, scenario, streams, ids):
        self.tuning = tuning
        d = scenario.get("day", {}) if isinstance(scenario, dict) else {}
        self.day = int(d.get("day", 1))
        self.plan = next((p for p in tuning["day_plan"] if p["day"] == self.day), tuning["day_plan"][0])
        self.upgrades = dict(d.get("upgrades") or {})
        self.active_upgrades = dict(self.upgrades)
        self.money = int(d.get("money", 0))
        self.earned = int(d.get("earned", 0))
        self.reputation = float(d.get("reputation", tuning["quan"]["reputation_initial"]))
        self.phase = "gather"
        self.done = False
        self.reason = None
        # Pha sáng dựng từ khối gather của scenario (nếu có)
        self.inner = GatherSim(tuning, scenario.get("gather", {}), streams, ids)

    # --- giao diện cho runner -------------------------------------------------
    @property
    def time_left_ticks(self):
        return self.inner.time_left_ticks

    def snapshot(self):
        snap = self.inner.snapshot()
        snap.update({
            "day": self.day,
            "day_plan": {"dishes": dict(self.plan["dishes"]), "ingredients": dict(self.plan["ingredients"])},
            "upgrades": dict(self.upgrades),
            "active_upgrades": dict(self.active_upgrades),
        })
        return snap

    def step(self, inp):
        events = self.inner.step(inp)
        if self.inner.done:
            self.done = True
            self.reason = self.inner.reason
        return events

    def inventory_items(self):
        return self.inner.inventory_items()
