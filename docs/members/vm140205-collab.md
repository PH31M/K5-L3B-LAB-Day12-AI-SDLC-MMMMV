# vm140205-collab — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  - Phụ trách module `sim/quan_customers` kiêm QA lead của nhóm.
  - Hoàn thành logic đón khách quán tối P1, lịch đến, kiên nhẫn, rời bàn mất uy tín.
  - Mở rộng quán P2 (4 bàn T1–T4, nhịp $120+900k$, thực đơn 6 món) ([commit `413fdfd`](https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV/commit/413fdfd)).
  - Hoàn thành Ticket 01 Phase 4: viết công cụ `tools/bench.py` đo FPS cảnh chuẩn bằng Chrome headless, xuất `bench.json` chuẩn 5 trường.
- Tôi đã review (kèm link):
  - Review PR #4 và PR #12 của Đức Minh và Nhật Minh về luồng chuyển giao nguyên liệu và đóng ca.
- AI sai ở đâu và tôi phát hiện thế nào:
  - AI ban đầu tính `p1_low_fps` bằng cách lấy trung bình cộng FPS của từng frame chậm, sai lệch với công thức Harmonic Mean trong PRD; tôi phát hiện khi đối chiếu spec và đã sửa thành `1 / (tổng thời gian / n)`.
- Điều tôi học được:
  - Benchmark hiệu năng cần đo trên môi trường trình duyệt thật với tải đầy đủ (cá bơi, cá sấu, hạt VFX), không thể chỉ đo mô phỏng trần không hình ảnh.
