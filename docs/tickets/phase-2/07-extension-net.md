# 07: Mở rộng — Vợt hút cá (net)

**What to build:** Nâng cấp Vợt cho phép bắt nhiều đàn trong một lần bấm: bán kính rộng hơn, tối đa 2–3 đàn, duyệt theo id. Đây là mục **mở rộng bắt buộc tối thiểu 1** cho nhóm 5 người.

**Blocked by:** 02, 05

**Status:** implemented-awaiting-day-shop-integration

Luật vợt đã cài và kiểm qua component; CLI `day` đã kiểm với patch metadata/data trong thư mục tạm.
Các dấu tích xác nhận luật, không xác nhận shop mua nâng cấp/vòng Ngày đã hoàn tất.
[Bằng chứng và patch bàn giao](../../proof/phase-2/nhat-minh.md). Chưa áp dụng patch vào file của Integrator.

- [ ] Manifest có `extensions: ["net"]` và `shop.upgrades.net` hai cấp: 250 → bán kính 4.0 m, tối đa 2 đàn; 500 → 6.0 m, tối đa 3 đàn.
- [x] Cấp 0 dùng đúng luật lõi (đàn gần nhất trong `catch_radius`, hòa theo id).
- [x] Từ cấp 1: duyệt đàn theo id trong bán kính vợt; đàn không đủ chỗ phát `hold_full` và **giữ lại**, vẫn xét đàn kế; dừng khi đủ `max_schools` lần bắt thành công.
- [x] Hồi chiêu chỉ đặt khi có ít nhất một đàn bắt thành công; không có đàn nào → không event, không hồi chiêu.
- [x] Không bật extension → hành vi y như lõi (hidden test mặc định không thấy khác biệt).
- [x] Có test: hai cấp, giỏ gần đầy, không có đàn trong tầm, và so byte với cấu hình không bật extension.
