# Ma trận truy vết Phase 3 (contract v1.2 — "Mùa Nước Nổi")

Cách kiểm chung: `PYTHONUTF8=1 python3 tools/run_checks.py` · riêng v1.2: `PYTHONPATH=tests:. python3 -m unittest tests.test_freshness_v12`.
Manifest ghi `"1.3"` (Phase 4 chỉ thêm lệnh) và chứa đủ luật v1.2 — `docs/clarify.md` Q14.

Kết quả lần chạy tích hợp (2026-11-21, Windows 11, Python 3.12.5): **211 test OK**, smoke/tất định/bằng chứng PASS —
`docs/proof/phase-3/do-tuoi/run-checks.txt`; smoke theo ticket — `docs/proof/phase-3/do-tuoi/smoke-p3.txt`.

## Lõi — kho cá thể và độ tươi

| AC | Cách kiểm | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P3-01 Manifest `freshness {100, 0.5, 0.25, 30}`, kiểm dải | `Manifest.test_manifest_has_v12_blocks_and_validates_ranges` | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-02 File kho `{"items":[{id,kind,fresh}]}`, rỗng `[]`, xuất theo id | `Handoff.test_two_process_handoff_keeps_id_kind_and_exact_freshness` | `docs/proof/phase-3/do-tuoi/smoke-p3.txt` | đạt |
| AC-P3-03 v1.2 trả mã 2 cho kho đếm, id trùng/rỗng, kind lạ, fresh ngoài [0,100]/NaN | `test_v12_rejects_counted_inventory_and_bad_individuals`, `test_inv_bad_schema_exit_2` | `docs/proof/phase-3/do-tuoi/smoke-p3.txt` | đạt |
| AC-P3-04 `--inventory-out` ghi một lần khi `gather_end`, file tạm + thay thế; ngất → `{"items":[]}`; chạm `--ticks` giữ nguyên đích | `test_faint_writes_empty_inventory_and_tick_limit_keeps_target`, `test_tick_limit_does_not_create_or_overwrite_inventory` | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-05 Đọc lại file giữ giá trị và nhánh ở ngưỡng 30 | `test_handoff_at_threshold_keeps_branch` (7201 units sau gather → ươn ở bước quán 2) | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-06 Hàng mới fresh 100, hao từ bước sau; id tăng tiếp sau id fixture | `test_new_items_start_at_100_and_ids_continue_after_fixture` | nt | đạt |
| AC-P3-07 Giỏ 0.5/s, kho quán 0.25/s (kể cả hàng đang giữ), kẹp 0, pause dừng hao | `test_stock_decays_including_reserved…`, `test_pause_freezes_decay`, `test_freshness_clamps_at_zero` | nt | đạt |
| AC-P3-08 `spoiled` đúng một lần khi ≥30 → <30, theo id, `location` hold/stock; fixture fresh 30 → tick 1 | `test_ticket_fixture_fresh_30_spoils_at_tick_1`, `test_spoiled_once_per_item_in_id_order_and_not_again` | `docs/proof/phase-3/do-tuoi/smoke-p3.txt` | đạt |
| AC-P3-09 Hàng ươn chiếm ô, không nấu, không giữ, không mời khách | `test_spoiled_items_still_fill_hold`, `test_spoiled_stock_is_not_offered_to_new_customers` | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-10 Giữ theo id: tươi nhất, hòa theo id; `reserved` là mảng id; không dùng chung | `test_cook_consumes_reserved_ids…` (giữ I4, I5, I2 bỏ I3), `test_bad_reserved_fixture_exit_2` | nt | đạt |
| AC-P3-11 Phần giữ vừa ươn → nhả toàn bộ, giữ lại một lần theo order_tick rồi id bàn; thiếu → `unfulfillable`, khách chờ | `test_reserved_item_spoils_then_rereserve_once_freshest`, `test_rereserve_by_order_tick_then_table_and_unfulfillable` | nt | đạt |
| AC-P3-12 Nấu tiêu đúng id; `base_price = floor(giá × TB fresh / 100)`; `items` sắp kind rồi id; boa trên giá chốt | `test_cook_consumes_reserved_ids_and_price_floors_on_average_freshness` (= 92), `test_nau_dung_don_va_chin_sau_cook_s` (= 59) | nt | đạt |
| AC-P3-13 `lost` trong `monster_hit`/`faint` là mảng cá thể LIFO | `test_hit_mat_mau_roi_nua_gio_va_bat_tu`, `test_faint_bo_gio_lifo_va_kho_rong`, `test_monster_loss_and_faint_export_individuals_in_lifo_order` | nt | đạt |
| AC-P3-14 day: bàn giao cùng tick không hao thêm, giữ id; Ngày kế cấp id mới; Shop không hao | `Day.test_day_handoff_same_tick_and_next_day_new_ids`, `test_phase_events_keep_old_phase…` | nt | đạt |
| AC-P3-15 Scenario mâu thuẫn (reserved trỏ id lạ/ươn/dùng chung/thiếu kho, hold sai schema) → mã 2 | `test_bad_reserved_fixture_exit_2`, `test_bad_hold_schema_exit_2` | nt | đạt |
| AC-P3-16 Cùng seed cùng byte | `check_determinism` + `day --days 2 --seed 7` hai lần, sha256 giống | `docs/proof/phase-3/do-tuoi/smoke-p3.txt` | đạt |
| AC-P3-17 HUD đọc được độ tươi / hàng ươn | Chromium thật: giỏ `44% / 94% · ⚠ 2 ƯƠN`, kho `% · ⚠ 2 ươn`, `Tươi 72% → 43k`, 0 lỗi console | `docs/proof/phase-3/do-tuoi/ui-check-p3.json` | đạt |

## Mở rộng — dòng nước lũ (`current`)

| AC | Cách kiểm | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P3-C1 Manifest `extensions` có `current`, `gather.current {1800,480,120,10,1.5}` kiểm dải | `Manifest.test_manifest_has_v12_blocks_and_validates_ranges` | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-C2 Lịch t=1800k: `current_warning` ở t−120, `current_start {direction,duration_ticks}` ở t, `current_end(elapsed)` ở t+480 | `Current.test_schedule_events_and_snapshot_on_real_manifest` | nt | đạt |
| AC-P3-C3 Lực 1.5 m/s khi d đầu bước ≥ 10, không tích lũy vào `vel`, chặn mép; cá/quái không bị đẩy | `test_current_start_depth_and_velocity_not_accumulated`, `test_current_clamps_player_and_does_not_push_fish_or_monster`; trình duyệt: trôi −1.525 m/1 s ở d = 12.1 | `docs/proof/phase-3/do-tuoi/ui-check-p3.json` | đạt |
| AC-P3-C4 Ca kết thúc trước → `current_end(phase_end)` trước `faint`/`gather_end` | `test_current_dock_emits_phase_end_before_gather_end` | `docs/proof/phase-3/do-tuoi/run-checks.txt` | đạt |
| AC-P3-C5 Snapshot `current: null | {direction, ticks_left}` đếm cả tick vừa chụp (480 ở tick t) | `test_schedule_events_and_snapshot_on_real_manifest` | nt | đạt |
| AC-P3-C6 `random_current:false` tắt lịch; `current_direction` khóa hướng; giá trị sai → mã 2 | `test_random_current_false_and_bad_direction` | nt | đạt |
| AC-P3-C7 HUD: báo trước bằng chữ + 🌊 + âm thanh, băng khi đang chảy | ảnh `gather-current-warning.jpg`, `gather-current-active.jpg` | `docs/proof/phase-3/do-tuoi/gather-current-active.jpg` | đạt |

## Test phải sửa — lý do (luật v1.2 thay luật cũ)

| Test | Trước | Sau | Lý do |
|---|---|---|---|
| Fixture `hold` / `quan.stock` trong `test_gather_*`, `test_smoke_p1`, `test_monsters`, `test_fish_rules`, `test_net_day_rules`, `test_quan_rules`, `test_day_loop`, `test_python_starter_units` | mảng kind / object đếm | `individuals([...])` (mảng cá thể) | TICKET-03 §1: kho cá thể thay kho đếm; v1.2 trả mã 2 cho schema cũ |
| So `hold`, `lost`, file kho | so mảng kind / object đếm | so `kinds(...)`, `counts(...)`, id, fresh ±0.01 | Cùng luật (thứ tự nhặt, LIFO, số lượng) nhưng payload là cá thể |
| `test_nau_dung_don_va_chin_sau_cook_s` | `base_price == 60`, `items == ["ca_loc"]` | `59`, `items` là cá thể I1 | Giá theo tươi: I1 đã hao 1 unit ở tick 1 ⇒ `floor(60 × 99.9958/100) = 59` |
| `test_inv_bad_schema_exit_2` | chỉ sai schema đếm | thêm kho đếm (mã 2 ở v1.2), id trùng, kind lạ, fresh ngoài miền | Adapter v1.2 |
| `test_surface_refills_and_stays_at_maximum` | không có event trong 1800 tick | thêm `random_current:false` | Extension `current` bật trong manifest phát `current_warning` ở 1680; ca này chỉ xét oxy |
| `test_gather_extensions` (item_ids) | đọc `fish_caught/gather.data.item_ids` | đọc id qua snapshot `hold`; manifest `fresh=False` bỏ `freshness` | Giữ payload event v1.1 (ticket không thêm `item_ids`) — clarify Q15; manifest gốc đã là v1.2 |

## Chưa kiểm / ngoài phạm vi

- Mở rộng `reservations` (khách đặt trước) và Chợ Chú Sáu: **chưa làm** (nhóm 5 người cần ≥ 1 mục; đã chọn `current`).
  Scenario vẫn kiểm cú pháp `quan.reservations` có từ trước nhưng sim chưa dùng.
- Thứ tự "cập nhật cá và sinh thêm" ở cuối bước gather (ticket) khác P2 (cá bơi trước tương tác) — giữ P2, ghi clarify Q16.
- HUD chỉ kiểm trên Chromium headless một máy Windows.
