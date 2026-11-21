# caominhnguyen05 — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  - Phụ trách module `sim/gather` kiêm vai trò Integrator của nhóm.
  - Hoàn thành lõi lặn hái sáng P1: oxy, ngạt t+59, ngất bỏ giỏ LIFO, hái sen/điên điển, hồi chiêu ([commit `9342f9e`](https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV/commit/9342f9e)).
  - Tích hợp quái vật Cá Sấu P2 (tuần tra/truy đuổi $d \ge 10$, tấn công mất máu, rơi nửa giỏ).
  - Hoàn thiện Ticket 02 Phase 4: kịch bản soak test 10 Ngày không crash bằng bot tất định.
- Tôi đã review (kèm link):
  - Review PR #2 và PR #11 của Nhật Minh và Văn Minh, đảm bảo tính tất định không đổi byte.
- AI sai ở đâu và tôi phát hiện thế nào:
  - AI ban đầu quên kẹp trần độ sâu khi Út Sen bơi xuống đáy $d > 30$, dẫn đến quái vật Cá Sấu tính sai vector đuổi; tôi phát hiện qua assertion test biên và đã kẹp `clamp(0, 30)` chặt chẽ.
- Điều tôi học được:
  - Quản lý nhánh và giữ contract manifest bất biến là chìa khóa để 5 người làm việc song song không giẫm chân nhau.
