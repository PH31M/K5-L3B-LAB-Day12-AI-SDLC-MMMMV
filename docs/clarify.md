# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

Nguồn trả lời ưu tiên: **Anh Năm hàng xóm** (trợ giảng AI ở tab Phase 1 của lab board) → giảng viên → nhóm tự đặt giả định.

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| Q1 | | `catch` khi giỏ không đủ chỗ: có đặt hồi chiêu không? PRD ghi "giữ đàn và cooldown" | Giả định: **không** đặt hồi chiêu, giữ nguyên bộ đếm cũ | PO |
| Q2 | | `paid.amount` = `base_price + tip`? | Giả định: đúng (tổng khách trả) | PO |
| Q3 | | `cook_started.items` là mảng kind đã tiêu, có lặp lại? | Giả định: có lặp, sắp theo kind | PO |
| Q4 | | `gather.amount` luôn bằng `node_yield` (hiện = 1)? | Giả định: đúng | PO |
| Q5 | | `faint.lost` khi giỏ rỗng là `[]`? | Giả định: đúng | PO |
| Q6 | | Khách ăn xong và khách mới đến cùng một tick: thứ tự event? | Giả định: trả tiền/rời trước, sinh khách sau | PO |
| Q7 | | `phase_tick` khi `time_left_ticks` bị rút ngắn vẫn bắt đầu 0? | Giả định: đúng | PO |
| Q8 | | `invuln_ticks` (starter có, PRD mục D không có) — bỏ khỏi scenario/snapshot? | Giả định: bỏ khỏi scenario; snapshot có thể giữ để không vỡ client | Integrator |

## Bàn giao PO — Nhật Minh, Phase 1 (2026-11-21)

- Ticket 03 triển khai theo **giả định Q1 hiện có**: bắt hụt vì giỏ thiếu chỗ giữ đàn, không đặt hồi chiêu mới. Test ghi rõ hành vi này; chưa có câu trả lời của trợ giảng để đóng Q1.
- Q2–Q8 vẫn là giả định, chưa có bằng chứng xác nhận. Cần đưa nguyên văn câu hỏi ở bảng trên cho Anh Năm/giảng viên và ghi nguồn trả lời trước khi đổi luật/contract.
- Phân công hiện hành lấy từ `TEAM.md`, `docs/plan/phase-1.md` và `docs/tickets/phase-1/README.md`: Nhật Minh làm ticket 03 + PO. Bảng trong conformance/team-split có phần dự kiến cũ; không tự nhận thêm luật quán của thành viên khác.
- Repo chỉ có yêu cầu Phase 1. Phase 2–4 cần nội dung board được công bố rồi mới lập ticket và triển khai; không tự suy đoán phần mở rộng.
- Đã xác minh core ticket 02 vào repo chung qua PR #1, commit `9342f9e`. Core này và helper ticket 03 đã được ghép trong bản làm việc `feat/nhat-minh`, 62/62 test qua, gồm ca ngất/kho rỗng. [Bằng chứng lát 2](proof/phase-1/nhat-minh.md). Chưa có review của người cho phần Nhật Minh.
