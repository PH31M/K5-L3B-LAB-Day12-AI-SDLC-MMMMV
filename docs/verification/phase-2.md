# Ma trận truy vết Phase 2 (contract v1.1)

Cách kiểm chung: `python3 tools/run_checks.py` · test riêng: `PYTHONPATH=tests:. python3 -m unittest discover -s tests`.

## Ticket 01 — prefactor v1.1 (xong)

| AC | Cách kiểm | Bằng chứng | Kết quả |
|---|---|---|---|
| Manifest 1.1: 8 đàn, 6 món, 3 loài, 6 nút, monsters, day_plan 5 Ngày, shop, extensions | `test_contract_v11.Manifest` | `docs/proof/phase-1/checks-latest.md` | đạt |
| `--mode day --ticks 0` chạy; snapshot có `day, day_plan, upgrades, active_upgrades` | `test_day_ticks_zero_has_day_fields` | nt | đạt |
| `--days` chỉ với `day`, trong [1,5] | `test_days_bounds_and_mode` | nt | đạt |
| `day` cấm `quan.stock` / `quan.reputation` | `test_day_scenario_rejects_stock_and_reputation` | nt | đạt |
| Scenario nhận `monsters[]`, `ca_ho`, `fish[].age_ticks`, `player.invuln_ticks/attack_cd_ticks` | `test_monsters_fixture`, `test_fish_age_ticks`, `test_player_invuln_and_attack_cooldown_accepted` | nt | đạt |
| Không hồi quy P1 | 103 test OK | nt | đạt |

## Test P1 phải sửa — lý do (bắt buộc ghi theo PRD)

| Test | Trước | Sau | Lý do |
|---|---|---|---|
| `test_gather_snapshot_has_gather_fields` | `len(fish) == 6` | `== 8` | Contract v1.1 chuẩn hoá **8 đàn** đầu ca (PRD Phase 2 §1.1) |
| `test_con_03_old_and_future_modes_rejected` | `day` phải bị từ chối | chỉ còn `river` | v1.1 hỗ trợ `--mode day`; danh sách mode cũ vẫn bị từ chối |
| `KINDS_P1` (inventory) | 4 nguyên liệu | 6 (`+ca_keo`, `+keo_neo`) | 2 nguyên liệu mới của thực đơn 6 món |

## Còn lại của Phase 2

Cá bơi/sinh (02), Cá Sấu (03), quán 2 bếp/4 bàn/6 món (04), `day` + Shop + pause (05), HUD (06), mở rộng `net` (07).
