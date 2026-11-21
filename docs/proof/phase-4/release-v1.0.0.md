# Bằng chứng nghiệm thu Phát hành v1.0.0 (AC-P4-04)

> Ticket: `docs/tickets/phase-4/04-dong-goi-release.md`  
> Người thực hiện: Phạm Hoàng Đức Minh (Integrator / Release Lead)  
> Ngày thực hiện: 2026-11-21  

---

## 1. Kiểm chứng 3 lệnh bắt đầu nhanh từ clone sạch

Đã thử nghiệm clone từ GitHub repo `https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV.git` vào thư mục tạm `/tmp/clean-test`:

```bash
# Lệnh 1: Clone repo
git clone https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV.git && cd K5-L3B-LAB-Day12-AI-SDLC-MMMMV

# Lệnh 2: Chạy toàn bộ test suite
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v

# Lệnh 3: Khởi động game trực tiếp trên trình duyệt
python3 -m chonoi.live --mode gather
```

### Kết quả chạy kiểm chứng:
- **Clone sạch:** Thành công, 100% đối tượng được tải về đầy đủ.
- **Test suite:** `Ran 191 tests in 9.940s — OK`. Toàn bộ 191 tests pass xanh (0 lỗi, 0 failure).
- **Live server:** Server khởi động mượt mà tại `http://localhost:8000`, phục vụ giao diện Canvas 60 FPS.

---

## 2. Kiểm tra khai báo Contract Manifest v1.3 (`game.contract.json`)

```json
{
  "contract_version": "1.3",
  "team": "MMMMV",
  "team_size": 5,
  "build_cmd": "true",
  "run_cmd": "python3 -m chonoi.live --mode gather",
  "headless_cmd": "python3 -m chonoi.headless",
  "bench_cmd": "python3 tools/bench.py",
  "soak_cmd": "python3 tools/soak.py",
  "extensions": [
    "net"
  ]
}
```
- Khai báo đầy đủ `bench_cmd` và `soak_cmd`.
- `contract_version` đạt chuẩn `"1.3"`.
- Không làm thay đổi schema tuning/kho/JSONL cốt lõi.

---

## 3. Tạo gói phát hành (Release Package)

Lệnh đóng gói mã nguồn (loại bỏ thư mục `.git` và file tạm):
```bash
git archive --format=zip --prefix=chonoi-v1.0.0/ -o docs/proof/phase-4/v1.0.0.zip HEAD
```

---

## 4. Release Notes v1.0.0 (Tóm tắt phát hành)

- **Tên phát hành:** `v1.0.0 - Quán Ăn Chợ Nổi`
- **Điểm mới:**
  - Lõi mô phỏng sông nước miền Tây: Út Sen lặn bắt cá, hái sen/điên điển, mở quán phục vụ khách, né Thủy quái Cá Sấu.
  - Vòng lặp ngày hoàn chỉnh 5 ngày với Chợ nâng cấp trang bị.
  - Hệ thống đồ họa Canvas tối ưu 60 FPS kèm chế độ Tương phản cao (`highContrast`, phím `C`).
  - Hệ thống âm thanh tự sinh Procedural Web Audio API.
  - Công cụ đo hiệu năng chuẩn hóa (`tools/bench.py`) và kiểm thử độ bền 10 ngày không lỗi (`tools/soak.py`).
- **Yêu cầu môi trường:** Python 3.10+, trình duyệt hiện đại (Chrome/Edge/Firefox/Safari).
