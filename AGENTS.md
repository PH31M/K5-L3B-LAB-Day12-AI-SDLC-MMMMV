# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật file này qua các phase (lịch sử git phải cho thấy điều đó). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan --seed 1 --ticks 600 --out out.jsonl`
- Headless (chế độ Ngày P2): `python3 -m chonoi.headless --mode day --seed 1 --days 1 --out day.jsonl`
- Cổng kiểm 1 lệnh: `python3 tools/run_checks.py`
- Kiểm tra tiến độ nhóm: `python3 tools/team_progress.py`
- Chơi thử trên trình duyệt: `python3 -m chonoi.live --mode gather|quan` (mở địa chỉ in ra; WASD, E, Space, R)

## Cấu trúc & quy ước
- (Starter Python là TÙY CHỌN; nhóm có thể dùng ngôn ngữ khác nếu giữ Test Contract.) Khung do giảng viên cấp: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/`. Hạn chế sửa; nếu phải sửa thì báo cả nhóm và ghi lại lý do.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/quan.py`, `chonoi/sim/quan_service.py`, `chonoi/sim/quan_customers.py`, `chonoi/sim/monsters.py`, `chonoi/sim/day.py`.
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.

## Điểm nhấn Phase 2 (Contract v1.1)
- Lặn sáng: 8 đàn cá ban đầu, 3 loài cá (`ca_loc`, `ca_linh`, `ca_keo`). Quái vật Cá Sấu tuần tra/truy đuổi ở độ sâu $d \ge 10$, tấn công mất 1 Máu và rơi nửa giỏ LIFO.
- Mở quán tối: 2 bếp nấu song song (`B1`, `B2`), 4 bàn ăn (`T1`–`T4`), thực đơn 6 món.
- Chế độ Ngày (`mode == "day"`): Lọc món theo `day_plan.dishes` trước khi xét kho khả dụng. Không đặt trần bán theo số suất kế hoạch.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills / hooks của nhóm
- `phase-gate` (`.agents/skills/phase-gate/SKILL.md`): Cổng kiểm tra toàn diện tự động trước khi gắn tag `phase-n` (kiểm tra test, smoke, tính tất định).
- `headless-probe` (`.agents/skills/headless-probe/SKILL.md`): Dựng ca kiểm thử bằng scenario + inputs, phân tích JSONL để chứng minh luật chạy đúng chuẩn headless.
