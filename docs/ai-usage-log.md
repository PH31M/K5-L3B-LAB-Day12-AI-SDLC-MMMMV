# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | Nhật Minh | Codex (GPT-6) | Đọc ticket 03/contract; viết helper hái/bắt và 25 test hộp đen; nối core Cao Minh trên `feat/nhat-minh`, ghi bằng chứng và bàn giao PO | Không có số liệu token/chi phí | 62/62 test qua trong bản làm việc, gồm ngất/kho rỗng. Console cp1258 từng lỗi khi in log Unicode; đã lưu/đọc log UTF-8. Chưa có review của người, chưa commit/push/merge trong lượt này. |
| 2 | Nhật Minh | Codex (GPT-6) | Cài cá bơi/sinh, net, test CLI và command kiểm trong thư mục tạm; chuẩn bị patch hooks/data cho Integrator | Không có số liệu token/chi phí | Test hồi quy P1 dùng random_fish:false để giữ fixture đứng yên; không đổi assertion luật. Không Git merge/push và không sửa contract gốc. |
| 3 | Nhật Minh | Codex (GPT-6) | Cài freshness, spoiled, ID/LIFO, current; kiểm qua subprocess component và ghép thử Cá Sấu | Không có số liệu token/chi phí | Probe ban đầu giữ tham chiếu snapshot đến cuối, làm vị trí cũ đổi theo bước sau; đã sửa xuất JSONL ngay mỗi bước, giữ nguyên assertion. Chưa có Stock để kiểm migration v1.2. |
| 4 | Nhật Minh | Claude Code (Sonnet 5.5) | Đọc phần được giao, chạy lại test (104 qua, 2 skip), viết phản tư cá nhân ≤ 200 từ, mục Nhật Minh trong retro | Không có số liệu token/chi phí | Không sửa luật/test. Không bịa link review hay số token: ghi rõ "chưa có". P2–P3 vẫn chưa commit/push, cần người đọc lại trước khi đẩy. |
