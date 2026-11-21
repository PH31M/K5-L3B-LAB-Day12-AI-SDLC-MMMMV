# qvinhh2312 — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  - Phụ trách module `client/ui` và vai trò UX + Demo lead.
  - Cài đặt toàn bộ hệ thống HUD cả 2 buổi (sáng: lặn/hái/bắt cá; tối: kho/bếp/bàn/khách) trong `chonoi/web/index.html` (Ticket 06).
  - Tích hợp banner nhắc phím ngữ cảnh tương tác thông minh (Contextual Prompts) khi vào tầm bến tàu [E], nút rau [E], đàn cá [Space], bếp và bàn ăn [E].
  - Thiết kế màn hình kết thúc (Game Over overlay) hiển thị rõ lý do (`docked`/`time`/`fainted`), bảng điểm chi tiết và nút Chơi lại hỗ trợ cả click chuột lẫn phím R.
  - Sáng tạo hệ thống âm thanh tự sinh bằng Web Audio API (0 KB asset ngoài) và hệ thống hạt bọt khí / khói bếp / sóng nước.
  - Soạn thảo kịch bản demo 3 phút trong `docs/demo.md` và bằng chứng nghiệm thu trong `docs/proof/phase-1/hud-ui.md`.
- Tôi đã review (kèm link):
  - Chuẩn bị review chéo cho PR của Nguyễn Văn Minh (`@vm140205-collab`) theo quy ước luồng review vòng tròn của nhóm.
- AI sai ở đâu và tôi phát hiện thế nào:
  - Ban đầu AI đề xuất dùng hàm `alert()` và prompt dạng DOM popup tách rời gây khựng vòng lặp `requestAnimationFrame` của canvas; tôi đã kịp thời phát hiện và chuyển sang render trực tiếp in-canvas banner với độ trong suốt và bo góc hiện đại.
- Điều tôi học được:
  - Thiết kế UI/UX game 2D nhẹ, `null-safe` khi client độc lập với tiến độ viết simulation core, và tuân thủ chặt chẽ ranh giới module để không làm sai lệch headless contract.
