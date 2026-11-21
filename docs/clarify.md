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
