# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| Phase 1 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế & code HUD Canvas 2 buổi (Ticket 06), prompt ngữ cảnh, overlay kết thúc, kịch bản demo | ~15.000 tokens | AI ban đầu dùng alert() làm dừng animation frame; đã sửa thành canvas overlay mượt mà |
| Phase 2 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế Web Audio API synthesis (tiếng lặn, cá, rau, chuông, tiền) và particle system | ~12.000 tokens | AI ban đầu đề xuất nạp tệp âm thanh WAV ngoài, vi phạm quy định hạn chế asset nặng; đã chuyển sang tổng hợp sóng dao động hoàn toàn |
| Phase 3 | Tào Quang Vinh | Gemini 3.8 Flash (High) | Thiết kế hiển thị độ tươi v1.2, toast spoiled và cờ ?fx=0 (Ticket 05 Phase 3) | ~10.000 tokens | AI ban đầu lọc mảng stock liên tục trong loop vẽ gây sụt frame; đã tối ưu bộ đệm dữ liệu |
| 1 | Nhật Minh | Codex (GPT-6) | Đọc ticket 03/contract; viết helper hái/bắt và 25 test hộp đen; nối core Cao Minh trên `feat/nhat-minh`, ghi bằng chứng và bàn giao PO | Không có số liệu token/chi phí | 62/62 test qua trong bản làm việc, gồm ngất/kho rỗng. Console cp1258 từng lỗi khi in log Unicode; đã lưu/đọc log UTF-8. Chưa có review của người, chưa commit/push/merge trong lượt này. |
| Phase 1 | Phạm Hoàng Đức Minh | Gemini 3.8 Flash (High) | Code module quan_service.py (Ticket 05) và 14 test unit kiểm thử các luồng interact/nấu/phục vụ/đóng ca | ~25.000 tokens | AI ban đầu tăng ready_ticks ngay tick món chín; đã sửa lại chỉ tăng từ tick sau cho món đã ready ở đầu bước theo PRD |
| Phase 2 | Phạm Hoàng Đức Minh | Gemini 3.8 Flash (High) | Code mở rộng Ticket 04: 2 bếp song song, 4 bàn, 6 món, lọc theo day_plan và bộ test test_quan_p2.py | ~20.000 tokens | AI ban đầu nhầm tưởng day_plan giới hạn trần bán; đã hiệu chỉnh lại để khách vẫn gọi được tiếp khi còn nguyên liệu |
