"""Bếp, bưng, phục vụ, tiền — lát 4 (PRD §F, mục Quán). KHUNG: để trống cho Đức Minh.

`quan.py` gọi bốn hàm dưới đây theo đúng thứ tự PRD; hiện là no-op nên luật quán chưa chạy.
Điền vào đây, không sửa `quan.py`.
"""

TICK = 60


def tick(sim, events):
    """Giảm timer nấu; bếp xong -> ready + dish_ready; tăng ready_ticks cho món đã ready đầu bước."""
    return


def interact_once(sim, events):
    """Chọn MỘT đối tượng theo (khoảng cách, bếp trước bàn, id); không tương tác được thì bỏ lượt.

    - bếp idle: lấy đơn reserved cũ nhất (order_tick, rồi id bàn), tiêu đúng phần giữ, chốt base_price,
      bắt đầu nấu -> cook_started {stove_id, order_id, dish_id, items, base_price}
    - bếp ready + tay trống: chuyển món vào tay -> dish_picked
    - bàn có khách đúng order_id: khách ăn, timer ăn đầy -> served {..., patience_ticks_left, base_price, tip}
    """
    return


def collect_finished(sim, events):
    """Khách ăn xong: thu tiền -> paid {..., amount, reason:"finished_eating"}, rời bàn, +uy tín nếu boa > 0."""
    return


def close_shift(sim, events):
    """Hết ca: khách đang ăn trả ngay (reason:"closing"); dọn món trên bếp/tay của đơn còn lại."""
    return
