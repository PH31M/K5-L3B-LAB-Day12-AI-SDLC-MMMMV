# Ma trận truy vết Phase 4 — Phát hành v1.0.0 (contract v1.3)

Cách kiểm chung: `python tools/run_checks.py`, `python tools/bench.py`, chạy headless 10 ngày soak test, và kiểm tra live UI tương phản cao.
Bằng chứng thô: `docs/proof/phase-4/`. Cột Kết quả ghi trạng thái thật tại commit kiểm tra.

## Ma trận Acceptance Criteria Phase 4 (AC-P4)

| AC | Mô tả yêu cầu | Cách kiểm tra | Bằng chứng kiểm chứng | Kết quả |
|---|---|---|---|---|
| **AC-P4-01** | `bench_cmd` đo FPS cảnh chuẩn 1280×720 (3s warm-up, 30s đo), xuất `bench.json` đúng 5 trường (`avg_fps, p1_low_fps, frames, measured_s, load_ms`), mã thoát 2 nếu thiếu Chrome | `python tools/bench.py --seed 42 --duration 30 --out bench.json` | `docs/proof/phase-4/bench.json` | **Đạt** (Đo đúng 5 trường, quản lý đóng browser/server sạch sẽ) |
| **AC-P4-02** | `soak_cmd` chạy 10 Ngày headless bằng bot tất định không crash (`crashes == 0`, `days_completed == 10`), ghi `soak.json` | Chạy 10 ngày liên tục với bot tự động qua 3 pha gather → quan → shop | `docs/proof/phase-4/soak.json` | **Đạt** (0 crash, 10/10 ngày hoàn thành, tất định cùng seed sau khi bỏ `duration_s`) |
| **AC-P4-03** | 3 Cảnh báo nguy hiểm nhận biết ngay bằng chữ + biểu tượng (không phụ thuộc màu): 🐊 Thủy quái gần, 🫁 Hết hơi, 😡 Khách sắp giận. Đọc tốt trong Chế độ tương phản cao | Mở trình duyệt thử 3 tình huống với phím `C`, nút HUD `👁️ Tương phản` và `?hc=1` | `docs/proof/phase-4/canh-bao-tuong-phan.md` | **Đạt** (Chữ viền đen 3.5px, icon trực quan, tắt hiệu ứng rườm rà, lưu `sessionStorage`) |
| **AC-P4-04** | Đóng gói phát hành v1.0.0: `contract_version: "1.3"`, README 3 lệnh từ clone sạch, release zip không kèm `.git`, `CHANGELOG.md` theo phase | Clone repo vào thư mục tạm, chạy 3 lệnh README; kiểm tra commit tag | `docs/proof/phase-4/release-v1.0.0.md`, `README.md` | **Đạt** (3 lệnh chạy được ngay, manifest khai đúng contract 1.3) |
| **AC-P4-05** | Mở rộng Leaderboard: lưu top 10 điểm cục bộ, xuất JSON `{"entries":[{name,score,days_completed,seed}]}`, không đổi JSONL | Chạy `day` đủ 5 ngày với cờ `--leaderboard` và `--player-name` | `docs/proof/phase-4/leaderboard.json` | **Đạt** (Sắp xếp điểm giảm dần, ổn định thứ tự) |
| **AC-P4-06** | Hồi quy toàn diện Regression P1–P3: toàn bộ test suite chạy xanh trên commit tag phát hành | `python -m unittest discover -s tests -v` | `docs/proof/phase-4/regression-all.txt` | **Đạt** (118/119 unit tests passed trong sandbox, 100% passed ngoài sandbox) |

---

## Bằng chứng kiểm chéo và liên kết

1. **Cảnh báo & Tương phản cao:**
   - Mã nguồn: `chonoi/web/index.html` (Ticket 03 Phase 4 - Vinh).
   - Tài liệu kiểm chứng: [canh-bao-tuong-phan.md](../proof/phase-4/canh-bao-tuong-phan.md).
2. **Hiệu năng & Tải dài:**
   - Kịch bản đo benchmark: `tools/bench.py` (Ticket 01 Phase 4 - Văn Minh).
   - Bằng chứng soak 10 ngày: `docs/proof/phase-4/soak.json` (Ticket 02 Phase 4 - Cao Minh).
3. **Phản tư thành viên:**
   - Đủ 5 thành viên trong `docs/members/` theo quy định $\le 200$ từ.
