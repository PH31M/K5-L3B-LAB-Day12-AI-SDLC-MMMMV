# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | Nhật Minh | Codex (GPT-6) | Đọc ticket 03/contract; viết helper hái/bắt và 25 test hộp đen; nối core Cao Minh trên `feat/nhat-minh`, ghi bằng chứng và bàn giao PO | Không có số liệu token/chi phí | 62/62 test qua trong bản làm việc, gồm ngất/kho rỗng. Console cp1258 từng lỗi khi in log Unicode; đã lưu/đọc log UTF-8. Chưa có review của người, chưa commit/push/merge trong lượt này. |
| Phase 1 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế & code HUD Canvas 2 buổi (Ticket 06), prompt ngữ cảnh, overlay kết thúc, kịch bản demo | ~15.000 tokens | AI ban đầu dùng alert() làm dừng animation frame; đã sửa thành canvas overlay mượt mà |
| Phase 2 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế Web Audio API synthesis (tiếng lặn, cá, rau, chuông, tiền) và particle system | ~12.000 tokens | AI ban đầu đề xuất nạp tệp âm thanh WAV ngoài, vi phạm quy định hạn chế asset nặng; đã chuyển sang tổng hợp sóng dao động hoàn toàn |
| Phase 3 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế hiển thị độ tươi v1.2, toast spoiled và cờ ?fx=0 (Ticket 05 Phase 3) | ~10.000 tokens | AI ban đầu lọc mảng stock liên tục trong loop vẽ gây sụt frame; đã tối ưu bộ đệm dữ liệu |
