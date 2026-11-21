# Credits

## 1. Asset & Âm thanh tự sinh
- **Hệ thống âm thanh (Audio FX):** Tự sinh bằng Web Audio API (`AudioContext`, Oscillator procedural synthesis), không sử dụng tệp âm thanh bên ngoài, dung lượng 0 KB, giấy phép MIT / CC0 (tác giả: Tào Quang Vinh `@qvinhh2312`).
- **Hiệu ứng đồ họa (VFX Particles):** Hệ thống hạt bọt khí lặn sâu, gợn sóng mặt nước và khói bếp tự sinh trên Canvas HTML5 (tác giả: Tào Quang Vinh `@qvinhh2312`).
- **Đồ họa 2D làng quê Nam Bộ (tự tạo, 0 KB ảnh):** toàn bộ nền và sprite trong `chonoi/web/index.html` được vẽ thủ tục bằng Canvas 2D rồi lưu vào canvas ẩn để tái dùng — bầu trời bình minh, núi thấp và sương, ruộng lúa, lũy tre, dừa, dừa nước, nhà tranh, nhà ngói đỏ, cầu gỗ, xuồng ba lá, bến Má Tư; Út Sen (áo bà ba, khăn rằn, giỏ lưới) ba tư thế; cá lóc, đàn cá linh, cặp cá kèo, Cá Sấu Năm Chèo; bông súng, bông điên điển, kèo nèo; quán nhà bè của Má Tư (mái ngói, gạch tàu, cột gỗ, dây đèn), bếp lò đất, bàn ghế đẩu, chén men lam, sáu món ăn, khách đội nón lá; ghe hàng có cây bẹo. Không dùng ảnh, font hay thư viện ngoài. Giấy phép như mã nguồn repo. Ảnh trong `docs/game-design-ref.md` (Overcooked, Shark! Shark!, ảnh phong cảnh) chỉ dùng để tham khảo cách đọc gameplay và màu sắc, **không** đưa vào game.

## 2. Công cụ AI hỗ trợ
- **Google Antigravity:** Mô hình Gemini 3.8 Flash (High) hỗ trợ thiết kế giao diện Canvas, kiến trúc Web Audio procedural sound, tài liệu ma trận truy vết và kịch bản demo.
- **Claude Code (Claude Opus 5.5):** viết lại client Canvas (đồ họa 2D làng quê, HUD theo `snapshot.phase`, Shop, tạm dừng, tổng kết), sửa lỗi đổi pha trong `--mode day`, kịch bản kiểm Playwright trong `docs/proof/phase-4/do-hoa-2d/`.
