# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| **AC-HUD-01** (HUD sáng: giờ, oxy đổi màu, máu, giỏ hàng, prompt tương tác bến/nút/cá) | Chơi thử live gather, quan sát UI | [`docs/proof/phase-1/hud-ui.md`](docs/proof/phase-1/hud-ui.md) | **Đạt** |
| **AC-HUD-02** (HUD tối: kho, khách + kiên nhẫn, bếp + timer, tay cầm, tiền, uy tín, prompt bếp/bàn) | Chơi thử live quan, quan sát UI | [`docs/proof/phase-1/hud-ui.md`](docs/proof/phase-1/hud-ui.md) | **Đạt** |
| **AC-HUD-03** (Màn kết thúc có lý do docked/time/fainted, bảng điểm, nút chơi lại click chuột + phím R) | Chạy hết giờ / cập bến / ngạt | [`docs/proof/phase-1/hud-ui.md`](docs/proof/phase-1/hud-ui.md) | **Đạt** |
| **AC-HUD-04** (Null-safety khi thiếu trường và không đổi byte headless JSONL) | Chạy headless diff byte | [`docs/proof/phase-1/hud-ui.md`](docs/proof/phase-1/hud-ui.md) | **Đạt** |

## Đánh giá ngắn
- Yêu cầu nào đạt / chưa đạt:
  - Ticket 06 (HUD cả 2 buổi, prompt ngữ cảnh, màn Game Over, âm thanh procedural, hiệu ứng bọt khí/khói) đạt 100%.
  - UI tách biệt hoàn toàn với logic mô phỏng, bảo toàn tính tất định của headless engine.
- Điều cần chỉnh cho phase sau:
  - Tiếp tục đồng bộ các sự kiện âm thanh và hiệu ứng hạt khi luật mở rộng Phase 2 được tích hợp.
