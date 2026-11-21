# Changelog
## Unreleased

## Phase 2 — Một ngày ở chợ nổi (contract v1.1)

- Contract v1.1: 8 đàn cá, 3 loài cá (`ca_loc`, `ca_linh`, `ca_keo`), 6 loại nguyên liệu (+`keo_neo`), thực đơn 6 món.
- Quái vật Cá Sấu (Ticket 03): tuần tra 1.0 m/s, truy đuổi 3.0 m/s khi d ≥ 10 và cách ≤ 10 m, tấn công trừ 1 Máu và rơi nửa giỏ LIFO, bất tử 90 tick, recoil lùi 2m.
- Mở rộng Quán Ăn (Ticket 04):
  - 2 bếp nấu B1 [2,8], B2 [5,8] nấu song song độc lập không giẫm đơn nhau.
  - 4 bàn ăn T1–T4 đón khách theo nhịp 120 + 900·k, giải phóng bàn khi khách ăn xong.
  - Thực đơn 6 món hỗ trợ đầy đủ nguyên liệu mới (`ca_keo`, `keo_neo`).
  - Hỗ trợ lọc thực đơn theo kế hoạch ngày (`day_plan.dishes`) ở chế độ `day`.
  - Phát sự kiện `no_dish` khi có bàn trống nhưng hết món đủ nguyên liệu.
- Vòng lặp Ngày 5 Ngày (`--mode day --days 1..5`) và Shop nâng cấp bình oxy, áo phao.

## Phase 1 — lõi hai buổi (contract v1.0)

- Lặn & hái: oxy, ngạt (choke ở `t+59`), ngất bỏ giỏ theo LIFO, hái nút + mọc lại, bắt cá (xóa đàn, hồi chiêu 30 tick), cập bến, ghi file kho.
- Mở quán: khách đến theo lịch, giữ chỗ theo công thức, kiên nhẫn, nấc/bưng/phục vụ, boa theo ngưỡng, đóng ca.
- HUD hai buổi; cổng kiểm một lệnh; ma trận truy vết và bằng chứng trong `docs/proof/`.
