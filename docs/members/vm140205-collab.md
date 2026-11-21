# vm140205-collab — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm (kèm commit):**
  - Ticket 04 P1 — khách, giữ chỗ, kiên nhẫn, `no_dish`: `quan_customers.py` + 4 test (`413fdfd`).
  - Prefactor v1.1 — manifest chuẩn, `scenario` nhận `day`/`monsters`, `--days`, envelope `day` (`c84eac9`).
  - Ticket 03 P2 — Cá Sấu: patrol/chase/hit/recoil/ngất, 10 test (`798680a`).
  - Hook net vào `day` — `shop.upgrades.net`, `active_upgrades`, hết skip (6 test) (`83e71a5`).
  - Công cụ: `tools/run_checks.py` (cổng 1 lệnh), `tools/team_progress.py`, `tools/bench.py` (Playwright/obscura, đúng công thức `p1_low_fps`).
  - QA: ma trận Phase 1, khôi phục proof HUD bị xoá (`d233ab4`), viết spec Phase 2–4.
- **Tôi đã review:** PR #15 — phát hiện bằng chứng AC-P4 không tồn tại và phản tư của 3 người bị viết hộ; yêu cầu sửa (đã sửa đúng).
- **AI sai ở đâu:** bản nháp test `dish_ready` của tôi khẳng định tick 360, chạy trên code thật ra 361 — tôi đoán mốc "bếp bắt đầu ở tick 0" trong khi event ghi ở `k+1`. Sửa thành `cook_started.tick + 360` và ghi quy ước vào test.
- **Điều tôi học được:** test xanh không chứng minh game chạy — phải mở đúng artefact được dẫn; và một file `bench.json` thật đáng giá hơn mười dòng "Đạt".
