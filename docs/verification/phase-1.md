# Ma trận truy vết Phase 1

Cách kiểm chung: `python3 tools/run_checks.py` (unit + hộp đen, smoke hai tiến trình, tất định).
Bằng chứng thô: `docs/proof/phase-1/`. Trạng thái ghi **trung thực tại thời điểm chạy** — cập nhật lại trước khi tag.

| AC | Yêu cầu (PRD §F) | Cách kiểm | Bằng chứng | Kết quả |
|---|---|---|---|---|
| AC-01 | Ở mặt nước oxy không giảm, hồi 6/tick, kẹp trần | `test_oxy_mat_nuoc_khong_giam` | `docs/proof/phase-1/checks-latest.md` | chưa đạt — chưa có luật |
| AC-02 | Dưới nước −1/tick, chạm 0 phát `oxygen_empty` | `test_oxy_duoi_nuoc_ve_0_dung_tick_1800` | nt | chưa đạt |
| AC-03 | Ngạt lần đầu ở `t+59`, `choke` kèm `hp` sau trừ | `test_choke_lan_dau_o_t_plus_59` | nt | chưa đạt |
| AC-04 | `faint` bỏ giỏ LIFO, `lost` là mảng kind, kho rỗng | `test_faint_bo_gio_lifo_va_kho_rong` | nt | chưa đạt |
| AC-05 | Nổi lên đúng bước đáng lẽ ngạt thì không ngạt | `test_noi_len_dung_tick_dang_le_ngat_thi_khong_ngat` | nt | chưa đạt |
| AC-06 | Hái nút gần nhất, hòa theo `id_key`; `hold_full` giữ nút | `test_hai_nut_hoa_khoang_cach_thi_theo_id_key`, `test_gio_day_thi_hold_full_khong_dat_regrow` | nt | chưa đạt |
| AC-07 | `regrow_ticks = 1200`, `node_regrown` đúng tick | `test_moc_lai_sau_1200_tick` | nt | chưa đạt |
| AC-08 | Bắt cá xóa đàn, `yield` đúng, hồi chiêu 30 tick | `test_bat_ca_xoa_dan_va_hoi_chieu_30_tick` | nt | chưa đạt |
| AC-09 | Không có đàn trong tầm: không event, không hồi chiêu | `test_khong_co_dan_trong_tam_thi_khong_hoi_chieu` | nt | đạt (guard) |
| AC-10 | Cập bến thắng hái, không cần ở mặt nước | `test_cap_ben_thang_hai_khi_dang_lan` | nt | đạt (đã có sẵn) |
| AC-11 | Hết giờ ở mọi độ sâu: giữ giỏ, ghi kho đúng một lần | `test_het_gio_duoi_sau_van_giu_gio` | nt | đạt (đã có sẵn) |
| AC-12 | Khách đến theo `first_customer_tick`/`customer_interval_s`, giữ đúng công thức, `no_dish`, hết kiên nhẫn → mất uy tín | 4 test quán (viết sau khi ticket 01 xong) | — | chưa có |
| AC-13 | Nấu trừ kho, `ready_ticks`, bưng 1 món, phục vụ đúng đơn, boa theo ngưỡng | 4 test quán | — | chưa có |
| AC-14 | Đóng ca: khách đang ăn trả tiền, khách chờ rời `closing` không trừ uy tín, `quan_end` một lần | test quán | — | chưa có |
| AC-15 | Smoke hai tiến trình: `gather` → file kho → `quan` thấy đúng `stock` | `tools/run_checks.py` cổng 2 | nt | chưa đạt |
| AC-16 | Cùng seed → JSONL giống từng byte | `tools/run_checks.py` cổng 3 | nt | chưa đạt |

## Đánh giá ngắn

- **Đạt:** các cổng hợp đồng đã có sẵn từ starter (cập bến, hết giờ, chặn biên, xuất kho, tất định khung).
- **Chưa đạt:** toàn bộ luật gather (oxy/ngạt/ngất/hái/bắt) và luật quán — đúng như ticket 02–05.
- **Điều cần chỉnh cho phase sau:** khi 01 xong, viết ngay 4 test quán (AC-12..14) để QA không chờ; trước khi tag phải chạy lại `tools/run_checks.py` và cập nhật cột Kết quả.
