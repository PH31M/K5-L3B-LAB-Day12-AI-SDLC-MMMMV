# Phase 3 — kho cá thể, độ tươi, dòng lũ: bằng chứng tích hợp

Ngày chạy: 2026-11-21 · Windows 11, Python 3.12.5, Chromium headless (Playwright) 1280×720.
Ma trận AC: [`docs/verification/phase-3.md`](../../../verification/phase-3.md).

| File | Nội dung | Cách tạo lại |
|---|---|---|
| [run-checks.txt](run-checks.txt) | Cổng kiểm: unittest (211 test), smoke gather → kho → quán trên schema v1.2, tất định, bằng chứng | `PYTHONUTF8=1 python3 tools/run_checks.py` |
| [smoke-p3.txt](smoke-p3.txt) | Fixture ngưỡng 30 nguyên văn ticket, smoke bàn giao hai tiến trình, 4 ca mã 2, `day --days 2` hai lần cùng byte | `python3 docs/proof/phase-3/do-tuoi/smoke_p3.py` |
| [ui-check-p3.json](ui-check-p3.json) + ảnh | HUD trên trình duyệt thật: độ tươi giỏ/kho, hàng ươn, giá chốt, dòng lũ (lực đo được), lỗi console | `python3 docs/proof/phase-3/do-tuoi/ui_check_p3.py` |

## Kết quả chính

- `gather` một bước với `hold:[{"id":"I1","kind":"ca_linh","fresh":30}]` phát đúng dòng mẫu của ticket:
  `{"type":"event","tick":1,"phase":"gather","name":"spoiled","data":{"item_id":"I1","kind":"ca_linh","location":"hold"}}`.
- Bàn giao file: `{"items":[{"id":"I1","kind":"ca_linh","fresh":99.99166666666666}]}` → snapshot quán tick 0 cùng id/kind,
  fresh 99.992 (JSONL làm tròn 3 chữ số, trong dung sai ±0.01).
- Kho đếm `{"items":{"ca_linh":2}}`, id trùng, kind lạ, fresh 120 → mã 2.
- Trình duyệt, quán: I1 (30.01) ươn → `spoiled {location:"stock"}`, đơn C1 giữ lại sang I2; nấu → `base_price` 43
  (`floor(60 × 71.708/100)`), chữ nổi "Tươi 72% → 43k". 0 lỗi console, kể cả khi bật tương phản cao.
- Trình duyệt, dòng lũ: thấy băng báo trước ở phase_tick 1721 (lịch 1680–1799); khi đang chảy, đứng yên ở d = 12.1 m
  bị đẩy −1.525 m trong ~1 s (luật 1.5 m/s), snapshot `current {direction:-1, ticks_left:364}`.

| Ảnh | Thấy gì |
|---|---|
| [gather-hold-fresh.jpg](gather-hold-fresh.jpg) | Giỏ `4/12 · cá linh ×1 44% · cá lóc ×1 94% · ⚠ 2 ƯƠN (chiếm ô)` |
| [gather-current-warning.jpg](gather-current-warning.jpg) | Băng `🌊 SẮP CÓ NƯỚC XIẾT sau … s` |
| [gather-current-active.jpg](gather-current-active.jpg) | Băng `🌊 NƯỚC XIẾT ← đẩy sang trái · còn 7 s`, toast hàng ươn |
| [quan-stock-fresh.jpg](quan-stock-fresh.jpg) | Kho khả dụng có % tươi và `⚠ n ươn` |
| [quan-cook-price.jpg](quan-cook-price.jpg) | `Tươi 72% → 43k` tại bếp B1 |
| [quan-stock-hc.jpg](quan-stock-hc.jpg) | Như trên ở tương phản cao |

## Chưa kiểm

- Mở rộng `reservations` và Chợ Chú Sáu chưa làm.
- HUD chỉ chạy trên Chromium headless của một máy; chưa thử Firefox/Safari.
