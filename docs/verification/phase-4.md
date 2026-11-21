# Ma trận truy vết Phase 4 — Phát hành v1.0.0 (contract v1.3)

> Nguyên tắc: Bằng chứng phải thật tại thời điểm kiểm tra. Không ghi nhận "Đạt" khi chưa có artefact thật trong repo.

Cách kiểm chung: `python tools/run_checks.py`, `python tools/bench.py`, chạy headless 10 ngày soak test, và kiểm tra live UI tương phản cao.
Bằng chứng thô: `docs/proof/phase-4/`. Cột Kết quả ghi trạng thái trung thực tại commit kiểm tra hiện tại.

## Ma trận Acceptance Criteria Phase 4 (AC-P4)

| AC | Mô tả yêu cầu | Cách kiểm tra | Bằng chứng kiểm chứng | Kết quả |
|---|---|---|---|---|
| **AC-P4-01** | `bench_cmd` đo FPS cảnh chuẩn 1280×720 (3s warm-up, 30s đo), xuất `bench.json` đúng 5 trường (`avg_fps, p1_low_fps, frames, measured_s, load_ms`), mã thoát 2 nếu thiếu Chrome | `python tools/bench.py --seed 42 --duration 30 --out bench.json` | `docs/proof/phase-4/bench.json` (Playwright/Chromium 159, WSL2, seed 42) | **Đạt** — 60.002 FPS trung bình, 1% low 59.524, 1801 khung trong 30.015 s, load 1960 ms; artifact đã commit |
| **AC-P4-02** | `soak_cmd` chạy 10 Ngày headless bằng bot tất định không crash (`crashes == 0`, `days_completed == 10`), ghi `soak.json` | Chạy 10 ngày liên tục với bot tự động qua 3 pha gather → quan → shop | `docs/proof/phase-4/soak.json` | **Đạt** (Đã có `tools/soak.py`, khai báo `soak_cmd`, chạy hoàn tất 10 ngày không crash `crashes == 0`, `days_completed == 10` trong 0.77s, artefact thật đã commit) |
| **AC-P4-03** | 3 Cảnh báo nguy hiểm nhận biết ngay bằng chữ + biểu tượng (không phụ thuộc màu): 🐊 Thủy quái gần, 🫁 Hết hơi, 😡 Khách sắp giận. Đọc tốt trong Chế độ tương phản cao (phím `C`, `?hc=1`) | Mở trình duyệt thử 3 tình huống với phím `C`, nút HUD `👁️ Tương phản` và `?hc=1` | `docs/proof/phase-4/canh-bao-tuong-phan.md` | **Đạt** (Chữ viền đen 3.5px, icon trực quan, tắt hiệu ứng rườm rà, lưu `sessionStorage`, artefact thật đã commit) |
| **AC-P4-04** | Đóng gói phát hành v1.0.0: `contract_version: "1.3"`, README 3 lệnh từ clone sạch, release zip không kèm `.git`, `CHANGELOG.md` theo phase | Clone repo vào thư mục tạm, chạy 3 lệnh README; kiểm tra commit tag | `docs/proof/phase-4/release-v1.0.0.md` | **Đạt** (Đã nâng manifest lên contract 1.3, kiểm chứng 3 lệnh clone sạch chạy 191 test xanh, tài liệu đóng gói release v1.0.0 đã sẵn sàng) |
| **AC-P4-05** | Mở rộng Leaderboard: lưu top 10 điểm cục bộ, xuất JSON `{"entries":[{name,score,days_completed,seed}]}`, không đổi JSONL | Chạy `day` đủ 5 ngày với cờ `--leaderboard` và `--player-name` | Cần `docs/proof/phase-4/leaderboard.json` | **Chưa đạt** (Chưa triển khai code mở rộng leaderboard) |
| **AC-P4-06** | Hồi quy toàn diện Regression P1–P3: toàn bộ test suite chạy xanh trên commit tag phát hành | `python -m unittest discover -s tests -v` | `docs/proof/phase-4/regression-all.txt` | **Đạt** (191 tests OK trong 9.498s trên môi trường sạch, 0 failures, 0 errors, artefact đã commit) |

---

## Hiện trạng các mục kiểm chứng

1. **Phần đã hoàn thành và có bằng chứng thật:**
   - **Ticket 01 Phase 4 (`bench_cmd` — Văn Minh):**
     - Mã nguồn: `tools/bench.py`.
     - Tài liệu kiểm chứng: [bench.json](../proof/phase-4/bench.json) (1801 khung/30s, 60.002 FPS).
   - **Ticket 02 Phase 4 (`soak_cmd` — Cao Minh / Đức Minh):**
     - Mã nguồn: `tools/soak.py`.
     - Manifest: khai báo `soak_cmd` trong `game.contract.json`.
     - Tài liệu kiểm chứng: [soak.json](../proof/phase-4/soak.json) (10 ngày, `crashes == 0`, `duration_s: 0.77s`).
   - **Ticket 03 Phase 4 (Cảnh báo & Tương phản cao — Vinh):**
     - Mã nguồn: `chonoi/web/index.html`.
     - Tài liệu kiểm chứng: [canh-bao-tuong-phan.md](../proof/phase-4/canh-bao-tuong-phan.md).
   - **Ticket 04 Phase 4 (Đóng gói Release v1.0.0 — Đức Minh):**
     - Manifest: `contract_version: "1.3"`.
     - Tài liệu kiểm chứng: [release-v1.0.0.md](../proof/phase-4/release-v1.0.0.md) (3 lệnh clone sạch, 191 test OK).
   - **Hồi quy Regression P1–P3 (AC-P4-06):**
     - Bằng chứng kiểm chứng: [regression-all.txt](../proof/phase-4/regression-all.txt) (191 tests pass 100%).
   - **Phản tư cá nhân:** Đầy đủ 5 thành viên trong `docs/members/` (`caominhnguyen05.md`, `PH31M.md`, `qvinhh2312.md`, `trandinhnhatminh1452.md`, `vm140205-collab.md`).
2. **Mở rộng tuỳ chọn (Optional):**
   - Ticket 05 (`leaderboard` - Nhật Minh): Tính năng mở rộng điểm số cục bộ (chưa triển khai).
