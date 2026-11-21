# 07: Mở rộng — Dòng nước lũ (`current`)

**What to build:** Cứ 30 giây nước lũ ập tới 8 giây, đẩy Út Sen theo một chiều. Báo trước 2 giây để người chơi kịp phản ứng.

**Blocked by:** 02

**Status:** implemented-awaiting-contract-integration

Luật current đã cài và kiểm qua component; lịch/lực đẩy đã kiểm thêm qua CLI với metadata hooks trong thư mục tạm.
Các dấu tích xác nhận luật; manifest và scenario flags cần owner contract ghép trước khi bật ở sản phẩm.
[Bằng chứng và bàn giao](../../proof/phase-3/nhat-minh.md).

- [ ] Manifest `gather.current {interval_ticks, duration_ticks, warning_ticks, min_depth, speed}`; `extensions` có `current`.
- [x] Lịch: `t = 1800·k` (k ≥ 1); báo trước ở `t−120` bằng `current_warning {starts_at_phase_tick}`; bắt đầu **trước** di chuyển ở `t`, kéo dài 480 tick.
- [x] Hướng chọn đều +x/−x theo seed khi bắt đầu; cộng 1.5 m/s vào người chơi nếu `d` đầu bước ≥ 10, rồi chặn mép; **không** tích lũy vào `player.vel`.
- [x] Kết thúc: `current_end {direction, reason:"elapsed"}` trước di chuyển ở `t+480`; nếu ca kết thúc trước → `current_end(phase_end)` trước `faint`/`gather_end`.
- [x] Snapshot `current: null` hoặc `{direction, ticks_left}`, đếm cả tick vừa chụp.
- [x] `random_current:false` tắt lịch; `current_direction:-1|1` khóa hướng; cá và quái **không** chịu lực dòng.
- [x] Không bật extension → hành vi y như lõi, cùng seed cho cùng byte.
