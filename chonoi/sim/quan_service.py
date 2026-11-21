"""Bếp, bưng, phục vụ, tiền — lát 4 (PRD §F, mục Quán).

⚠️ Đây là KHUNG GIỮ CHỖ tên hàm, không phải bản cài đặt. Bản thật (447 dòng + 9 test)
đang ở nhánh `feat/duc-minh` của Đức Minh; khi nhánh đó merge, file này bị thay thế và
`quan.py` không phải sửa gì vì đã gọi đúng bốn tên dưới đây.

Bốn hàm trả về danh sách event `[(name, data), ...]` theo đúng thứ tự PRD §F, không append vào
biến ngoài (khác kiểu `events` của `gather_actions`).
"""


def advance_stoves_and_eating(sim):
    """Bước 1–2: giảm cook_ticks_left; xong thì ready + dish_ready; tăng ready_ticks cho món đã ready
    ở ĐẦU bước; giảm eat_ticks_left của khách đang ăn."""
    return []


def handle_interact(sim, inp=None):
    """Bước 4: chọn MỘT đối tượng theo (khoảng cách, bếp trước bàn, id); không tương tác được thì bỏ lượt.

    - bếp idle: lấy đơn reserved cũ nhất (order_tick, rồi id bàn), tiêu đúng phần giữ, chốt base_price
      → `cook_started {stove_id, order_id, dish_id, items, base_price}`
    - bếp ready + tay trống: chuyển món vào tay → `dish_picked`
    - bàn có khách đúng order_id: khách ăn, timer đầy → `served {..., patience_ticks_left, base_price, tip}`
    """
    return []


def handle_finished_eating(sim):
    """Bước 5: khách ăn xong → `paid {..., amount, reason:"finished_eating"}`, rời bàn, +uy tín nếu boa > 0."""
    return []


def handle_closing(sim):
    """Bước 7: hết ca — khách đang ăn trả ngay (`reason:"closing"`); dọn món trên bếp/tay của đơn còn lại."""
    return []
