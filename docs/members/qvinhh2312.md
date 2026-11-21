# qvinhh2312 — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  - Phụ trách module `client/ui` và vai trò UX + Demo lead.
  - Cài đặt toàn bộ hệ thống HUD cả 2 buổi (sáng: lặn/hái/bắt cá; tối: kho/bếp/bàn/khách) trong `chonoi/web/index.html` (Ticket 06).
  - Tích hợp banner nhắc phím ngữ cảnh tương tác thông minh (Contextual Prompts) khi vào tầm bến tàu [E], nút rau [E], đàn cá [Space], bếp và bàn ăn [E].
  - Thiết kế màn hình kết thúc (Game Over / Finished overlay) hiển thị rõ ràng lý do kết thúc (`docked`/`time`/`fainted`), bảng thống kê điểm và nút Chơi lại hỗ trợ cả click chuột lẫn phím R.
  - Soạn thảo kịch bản demo 3 phút chuẩn mực trong `docs/demo.md`.
- Tôi đã review (kèm link):
  - Chuẩn bị review chéo cho PR của Nguyễn Văn Minh (`@vm140205-collab`) theo quy ước luồng review vòng tròn của nhóm.
- AI sai ở đâu và tôi phát hiện thế nào:
  - Ban đầu AI đề xuất dùng hàm `alert()` và prompt dạng DOM popup tách rời gây khựng và đơ vòng lặp `requestAnimationFrame` của canvas; tôi đã kịp thời phát hiện và yêu cầu render trực tiếp in-canvas banner với độ trong suốt và bo góc hiện đại.
- Điều tôi học được:
  - Nắm vững cách thiết kế UI/UX game 2D nhẹ, tối ưu `null-safe` khi client độc lập với tiến độ viết simulation core, và tuân thủ chặt chẽ ranh giới module để không làm sai lệch headless contract.
