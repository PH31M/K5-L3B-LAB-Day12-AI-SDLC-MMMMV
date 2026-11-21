"""Độ tươi cá thể (contract v1.2, ADR-0001). Không đọc/ghi file kho.

Đơn vị chính xác: 1 điểm tươi = 240 units. Hàng trong sim mang `fresh_units` (int, hoặc Fraction khi
fixture cho số lẻ không biểu diễn được bằng units nguyên) và `decay_rem` (phần lẻ hao chưa trừ).
Hao 0.5/s ở 60 Hz = 2 units/tick (giỏ), 0.25/s = 1 unit/tick (kho quán); ngưỡng ươn 30 = 7200 units.
So ngưỡng trên giá trị chính xác, chỉ đổi sang điểm khi xuất snapshot/event/file.
"""

from fractions import Fraction

from ..ids import id_key, sort_by_id

UNITS_PER_POINT = 240


def _norm(v):
    if isinstance(v, Fraction) and v.denominator == 1:
        return int(v)
    return v


def units(points):
    """Điểm (số JSON) -> units chính xác. Số thực đọc lại từ JSON được khôi phục về phân số gần nhất."""
    frac = Fraction(str(points)).limit_denominator(10 ** 6)
    return _norm(frac * UNITS_PER_POINT)


def points(fresh_units):
    v = Fraction(fresh_units) / UNITS_PER_POINT
    return int(v) if v.denominator == 1 else float(v)


def make(ident, kind, fresh_units):
    return {"id": ident, "kind": kind, "fresh_units": fresh_units, "decay_rem": Fraction(0)}


def from_fixture(items):
    """Mảng {id, kind, fresh} (đã kiểm) -> cá thể trong sim, giữ nguyên thứ tự."""
    return [make(it["id"], it["kind"], units(it["fresh"])) for it in items]


def copy_items(items):
    """Bàn giao trong bộ nhớ: giữ id/kind/fresh chính xác, bỏ phần lẻ hao của nơi chứa cũ."""
    return [make(it["id"], it["kind"], it["fresh_units"]) for it in items]


def export_item(item):
    return {"id": item["id"], "kind": item["kind"], "fresh": points(item["fresh_units"])}


def export(items):
    """Giữ thứ tự truyền vào (LIFO cho `lost`, thứ tự nhặt cho `hold`)."""
    return [export_item(it) for it in items]


def threshold(config):
    return units(config["spoiled_below"])


def is_spoiled(item, config):
    return item["fresh_units"] < threshold(config)


def per_tick(config, key, tick_hz):
    return Fraction(str(config[key])) * UNITS_PER_POINT / Fraction(str(tick_hz))


def initialize(items, ids):
    """Hàng có sẵn trong scenario giữ nguyên id; allocator nối tiếp sau id lớn nhất."""
    hold = from_fixture(items)
    for item in hold:
        ids.reserve(item["id"])
    return hold


def renew_ids(items, ids):
    """Ngày kế trong `day`: cấp id mới theo thứ tự mảng, giữ kind/fresh ban đầu."""
    return [make(ids.new("I"), it["kind"], units(it["fresh"])) for it in items]


def receive(sim, kind, amount):
    """Thêm hàng mới vào giỏ. Payload event `gather`/`fish_caught` giữ nguyên như v1.1 (ticket không đổi);
    id cá thể mới đọc được qua snapshot `hold`."""
    if sim.freshness is None:
        sim.hold.extend([kind] * amount)
        return {}
    sim.hold.extend(make(sim.ids.new("I"), kind, units(sim.freshness["initial"])) for _ in range(amount))
    return {}


def decay(items, config, key, tick_hz, location, events):
    """Hao một bước cho hàng có sẵn; phát `spoiled` theo id cho cá thể vừa đi từ >= ngưỡng xuống < ngưỡng.

    Trả danh sách id vừa ươn (để Quán xử lý giữ chỗ)."""
    step = per_tick(config, key, tick_hz)
    limit = threshold(config)
    spoiled = []
    for item in sort_by_id(items):
        before = item["fresh_units"]
        total = item["decay_rem"] + step
        whole = int(total)
        item["decay_rem"] = total - whole
        item["fresh_units"] = _norm(max(0, before - whole))
        if before >= limit > item["fresh_units"]:
            spoiled.append(item["id"])
            events.append(("spoiled", {"item_id": item["id"], "kind": item["kind"], "location": location}))
    return spoiled


def advance(hold, config, tick_hz, events):
    """Giỏ (gather): hao theo gather_decay_per_s."""
    return decay(hold, config, "gather_decay_per_s", tick_hz, "hold", events)


def freshest_first(items):
    """Tươi nhất trước, hòa theo id."""
    return sorted(items, key=lambda it: (-Fraction(it["fresh_units"]), id_key(it["id"])))
