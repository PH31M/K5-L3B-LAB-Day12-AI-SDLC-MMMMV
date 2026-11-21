"""Kho quán v1.2: cá thể, giữ chỗ theo id, giữ lại khi hàng ươn, giá theo độ tươi (TICKET-03 §1).

Chỉ dùng khi `sim.freshness` có giá trị (contract v1.2+). Kho v1.1 (object đếm) vẫn đi đường cũ trong
`quan_customers`/`quan_service` để test và fixture v1.1 chạy được (ADR-0001, adapter hai schema).

- `sim.stock`: mảng cá thể trong sim `{id, kind, fresh_units, decay_rem}` — gồm cả hàng đang được giữ.
- `customer["reserved"]`: mảng id cá thể (sắp theo kind rồi id).
"""

import math
from fractions import Fraction

from ..errors import BadInput
from ..ids import id_key, sort_by_id
from . import freshness


def is_v12(sim):
    return getattr(sim, "freshness", None) is not None


def held_ids(customers):
    out = set()
    for c in customers:
        out.update(c.get("reserved") or ())
    return out


def _usable(items, config, excluded):
    return [it for it in items if it["id"] not in excluded and not freshness.is_spoiled(it, config)]


def available_counts(sim):
    """Số cá thể khả dụng theo loại: chưa ươn và chưa bị đơn nào giữ."""
    out = {}
    for it in _usable(sim.stock, sim.freshness, held_ids(sim.customers)):
        out[it["kind"]] = out.get(it["kind"], 0) + 1
    return out


def pick(items, recipe, config, excluded):
    """Mỗi loại trong công thức lấy các cá thể khả dụng tươi nhất, hòa theo id. Thiếu -> None."""
    chosen = []
    usable = _usable(items, config, excluded)
    for kind in sorted(recipe):
        pool = freshness.freshest_first([it for it in usable if it["kind"] == kind])
        if len(pool) < recipe[kind]:
            return None
        chosen.extend(pool[:recipe[kind]])
    return order_ids(chosen)


def order_ids(items):
    """Thứ tự chuẩn của phần giữ / items đã tiêu: theo kind rồi id."""
    return [it["id"] for it in sorted(items, key=lambda it: (it["kind"], id_key(it["id"])))]


def reserve(sim, customer):
    """Giữ cá thể tươi nhất cho đơn; trả True nếu đủ."""
    others = held_ids(c for c in sim.customers if c is not customer)
    ids = pick(sim.stock, sim.menu[customer["dish_id"]]["recipe"], sim.freshness, others)
    customer["reserved"] = ids or []
    return ids is not None


def handle_spoiled(sim, spoiled_ids, events):
    """Đơn có phần giữ vừa ươn: nhả toàn bộ, thử giữ lại đúng một lần; theo order_tick rồi id bàn.

    Không đủ -> `unfulfillable`, khách vẫn chờ tới hạn kiên nhẫn."""
    if not spoiled_ids:
        return
    bad = set(spoiled_ids)
    affected = [c for c in sim.customers
                if c.get("order_status") == "reserved" and bad.intersection(c.get("reserved") or ())]
    affected.sort(key=lambda c: (c.get("order_tick", 0), id_key(c["table_id"])))
    for c in affected:
        c["reserved"] = []
        if not reserve(sim, c):
            c["order_status"] = "unfulfillable"


def consume(sim, customer):
    """Bắt đầu nấu: tiêu đúng các id đang giữ; trả (items xuất theo kind rồi id, base_price đã chốt)."""
    ids = list(customer.get("reserved") or [])
    by_id = {it["id"]: it for it in sim.stock}
    used = [by_id[i] for i in ids if i in by_id]
    used.sort(key=lambda it: (it["kind"], id_key(it["id"])))
    taken = {it["id"] for it in used}
    sim.stock = [it for it in sim.stock if it["id"] not in taken]
    price = sim.menu[customer["dish_id"]]["price"]
    total = sum(Fraction(it["fresh_units"]) for it in used)
    n = len(used)
    base_price = math.floor(Fraction(price) * total / (n * freshness.UNITS_PER_POINT * 100)) if n else price
    return freshness.export(used), base_price


def export_stock(items):
    return freshness.export(sort_by_id(items))


def assign_fixture(customers, stock, menu, config):
    """Kiểm/điền `reserved` của khách dựng sẵn (scenario). Sai hoặc mâu thuẫn -> BadInput (mã 2).

    `stock` là mảng cá thể trong sim. Đơn có `reserved` tường minh được kiểm trước; đơn `reserved`
    bỏ trống được cấp theo order_tick rồi id bàn, lấy tươi nhất rồi id nhỏ."""
    by_id = {it["id"]: it for it in stock}
    taken = set()
    pending = []
    for c in customers:
        status = c.get("order_status", "reserved")
        ids = c.get("reserved")
        if ids is None or ids == []:
            c["reserved"] = []
            if status == "reserved":
                pending.append(c)
            continue
        if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
            raise BadInput(f"customers.{c['id']}: reserved phải là mảng id cá thể (v1.2)")
        if status != "reserved":
            raise BadInput(f"customers.{c['id']}: chỉ đơn reserved mới giữ cá thể")
        kinds = {}
        for i in ids:
            it = by_id.get(i)
            if it is None:
                raise BadInput(f"customers.{c['id']}: reserved trỏ tới cá thể không có trong kho: {i}")
            if i in taken:
                raise BadInput(f"customers.{c['id']}: cá thể {i} đã được đơn khác giữ")
            if freshness.is_spoiled(it, config):
                raise BadInput(f"customers.{c['id']}: không được giữ cá thể ươn {i}")
            taken.add(i)
            kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
        if kinds != menu[c["dish_id"]]["recipe"]:
            raise BadInput(f"customers.{c['id']}: reserved khác công thức của món")
        c["reserved"] = order_ids([by_id[i] for i in ids])
    pending.sort(key=lambda c: (c.get("order_tick", 0), id_key(c["table_id"])))
    for c in pending:
        ids = pick(stock, menu[c["dish_id"]]["recipe"], config, taken)
        if ids is None:
            raise BadInput(f"customers.{c['id']}: kho không đủ cá thể chưa ươn để giữ chỗ")
        taken.update(ids)
        c["reserved"] = ids
    return customers
