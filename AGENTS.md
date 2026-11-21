# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật qua các phase (P1: Khởi tạo · P2: Âm thanh & VFX · P3: Kho cá thể & Độ tươi). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan --seed 1 --ticks 600 --out out.jsonl`
- Chơi thử trên trình duyệt: `python3 -m chonoi.live --mode gather|quan` (mở địa chỉ in ra; WASD, E, Space, R, M bật/tắt âm thanh)
- Kiểm tra hiệu năng máy yếu: `http://127.0.0.1:<port>/?fx=0` (tắt hiệu ứng hạt và sóng nước)

## Cấu trúc & quy ước
- Khung Python chuẩn: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/index.html`.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/gather_actions.py`, `chonoi/sim/quan_customers.py`, `chonoi/sim/quan_service.py`.
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.
- **Client Web UI (`chonoi/web/index.html`):** Chỉ đọc snapshot từ `/state`, không can thiệp logic backend, an toàn `null-safe` khi server thiếu trường.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test toàn bộ.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.
- Không nạp tệp âm thanh/đồ họa ngoài nặng vào repo; âm thanh và VFX ưu tiên tự sinh bằng Web Audio API và Canvas particles.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills của nhóm (tại `.agents/skills/`)
1. **`check-headless`** (`.agents/skills/check-headless/SKILL.md`): Lệnh kiểm tra nhanh tính tất định (cùng seed $\rightarrow$ cùng byte) và chuỗi chuyển giao file kho `gather -> kho -> quan`.
2. **`ui-verify`** (`.agents/skills/ui-verify/SKILL.md`): Quy trình kiểm tra toàn diện giao diện người dùng trực tiếp (Live UI/HUD), âm thanh procedural Web Audio và cờ `?fx=0`.
