"""Lát 2: Hái nút nguyên liệu, bắt đàn cá, cập bến.

Tác giả: Trần Đình Nhật Minh (@trandinhnhatminh1452)
Hợp đồng: docs/contracts/README.md & docs/plan/phase-1-conformance.md §3.F, §4
Ticket: docs/tickets/phase-1/03-gather-actions.md
"""

import math

from ..ids import id_key

TICK = 60.0


def try_dock(sim, events: list) -> bool:
    """Nếu đang trong bán kính bến, kết thúc gather lý do 'docked'.

    Được xét TRƯỚC mọi xử lý hái, không cần ở mặt nước.
    Trả về True nếu đã cập bến thành công.
    """
    if sim._in_dock():
        sim._finish("docked", events)
        return True
    return False


def handle_gather_node(sim, events: list) -> bool:
    """Hái nút nguyên liệu ở mặt nước.

    - Chỉ hái khi ở mặt nước (d <= surface_depth).
    - Chọn nút `ready` (regrow_ticks == 0) gần nhất trong interact_radius.
    - Hòa khoảng cách: chọn id nhỏ hơn theo `id_key` (ví dụ N2 trước N10).
    - Đủ chỗ: thêm `node_yield` vào giỏ (hold), đặt regrow_ticks = regrow_s * 60,
      phát event `gather` {node_id, kind, amount}.
    - Thiếu chỗ: phát event `hold_full` {action: "gather", node_id, required, free},
      nút giữ nguyên (không đặt regrow_ticks).
    Trả về True nếu đã xử lý hái nút (thành công hoặc hold_full).
    """
    if not sim._at_surface():
        return False

    interact_radius = sim.t["interact_radius"]
    candidates = []
    for n in sim.nodes:
        if n.get("regrow_ticks", 0) == 0:
            d = math.dist(sim.pos, n["pos"])
            if d <= interact_radius:
                candidates.append((d, n))

    if not candidates:
        return False

    # Khoảng cách gần nhất, hòa thì id nhỏ hơn theo id_key
    _, target = min(candidates, key=lambda c: (round(c[0], 6), id_key(c[1]["id"])))

    capacity = sim.t["hold_capacity"]
    free = max(0, capacity - len(sim.hold))
    node_yield = sim.t.get("node_yield", 1)

    if free >= node_yield:
        for _ in range(node_yield):
            sim.hold.append(target["kind"])
        target["regrow_ticks"] = int(round(sim.t.get("regrow_s", 20) * TICK))
        events.append(("gather", {
            "node_id": target["id"],
            "kind": target["kind"],
            "amount": node_yield,
        }))
        return True
    else:
        events.append(("hold_full", {
            "action": "gather",
            "node_id": target["id"],
            "required": node_yield,
            "free": free,
        }))
        return True


def handle_catch_fish(sim, events: list) -> bool:
    """Bắt đàn cá khi lặn dưới nước.

    - Chỉ thực hiện khi hết hồi chiêu (catch_cd_ticks == 0) và đang ở dưới nước (d > surface_depth).
    - Chọn đàn gần nhất trong catch_radius, hòa khoảng cách thì chọn id nhỏ hơn theo id_key.
    - Đủ chỗ: thêm toàn bộ `fish_yield`, XÓA đàn cá khỏi sim.fish,
      phát `fish_caught` {fish_id, kind, yield}, đặt hồi chiêu catch_cooldown_s * 60.
    - Thiếu chỗ: phát `hold_full` {action: "catch", fish_id, required, free},
      giữ nguyên đàn cá, không thử đàn khác, KHÔNG đặt hồi chiêu.
    - Không có đàn trong tầm: không event, không hồi chiêu.
    Trả về True nếu đã thử bắt đàn cá.
    """
    if sim.catch_cd_ticks > 0 or sim._at_surface():
        return False

    catch_radius = sim.t["catch_radius"]
    candidates = []
    for f in sim.fish:
        d = math.dist(sim.pos, f["pos"])
        if d <= catch_radius:
            candidates.append((d, f))

    if not candidates:
        return False

    # Khoảng cách gần nhất, hòa thì id nhỏ hơn theo id_key
    _, target = min(candidates, key=lambda c: (round(c[0], 6), id_key(c[1]["id"])))

    fish_yield_cfg = sim.t.get("fish_yield", {})
    if isinstance(fish_yield_cfg, dict):
        yield_amount = fish_yield_cfg.get(target["kind"], 1)
    else:
        yield_amount = int(fish_yield_cfg)

    capacity = sim.t["hold_capacity"]
    free = max(0, capacity - len(sim.hold))

    if free >= yield_amount:
        for _ in range(yield_amount):
            sim.hold.append(target["kind"])
        sim.fish.remove(target)
        events.append(("fish_caught", {
            "fish_id": target["id"],
            "kind": target["kind"],
            "yield": yield_amount,
        }))
        sim.catch_cd_ticks = int(round(sim.t.get("catch_cooldown_s", 0.5) * TICK))
        return True
    else:
        events.append(("hold_full", {
            "action": "catch",
            "fish_id": target["id"],
            "required": yield_amount,
            "free": free,
        }))
        return True


def handle_interact(sim, inp, events: list) -> bool:
    """Điều phối tương tác: bến trước, sau đó hái nút ở mặt nước."""
    if not inp.pressed("interact"):
        return False
    if try_dock(sim, events):
        return True
    return handle_gather_node(sim, events)


def handle_catch(sim, inp, events: list) -> bool:
    """Điều phối phím catch."""
    if not inp.pressed("catch"):
        return False
    return handle_catch_fish(sim, events)
