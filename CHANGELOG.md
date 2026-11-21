# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - Phase 3 (Mùa Nước Nổi)
### Added
- **Kho cá thể (Individual Items):** Chuyển đổi định dạng kho sang mảng cá thể `{id, kind, fresh}`.
- **Độ tươi & Hàng ươn (Freshness & Spoiled):**
  - Độ tươi `fresh` giảm theo thời gian; cá thể có `fresh < 30` bị coi là ươn, không thể dùng để nấu.
  - Sự kiện `spoiled` phát ra khi cá thể vượt ngưỡng ươn.
- **HUD v1.2 (Ticket 05):**
  - Hiển thị thanh độ tươi mini trên từng ô giỏ hàng.
  - Gạch chéo đỏ và nhãn `ƯƠN` cho cá thể ươn.
  - Banner toast thông báo cá thể ươn (chỉ hiện đúng 1 lần cho mỗi cá thể).
  - Cờ `?fx=0` trên URL để tắt hiệu ứng hạt và sóng nước trên máy yếu.

## [1.1.0] - Phase 2
### Added
- **Âm thanh tự sinh (Procedural Web Audio API):**
  - Tự động phát âm thanh khi lặn/nổi nước, hái rau, bắt cá, chuông bếp, cập bến và trả tiền.
  - Nút Bật/Tắt âm thanh `🔊 / 🔇` trực tiếp trên canvas và phím tắt `M`.
- **Hiệu ứng đồ họa (VFX Particles):**
  - Hạt bọt khí oxy nổi lên khi lặn sâu.
  - Khói bếp bốc lên khi bếp đang nấu.
  - Sóng nước lăn tăn nhấp nhô nhẹ trên mặt sông.

## [1.0.0] - Phase 1 (Kickoff & Core Gameplay)
### Added
- Hoàn thiện trọn vẹn 2 buổi: Buổi sáng (Gather: lặn, hái rau, bắt cá, cập bến) và Buổi tối (Quán: nhận khách, nấu bếp, phục vụ, tính tiền, uy tín).
- Giao diện HUD trực quan 2 buổi (Ticket 06): Đồng hồ đếm ngược, thanh oxy đổi 3 màu, tim Máu, giỏ hàng trực quan.
- Hệ thống banner nhắc phím ngữ cảnh (Contextual Prompts) khi vào phạm vi bến tàu, nút rau, đàn cá, bếp nấu, bàn ăn.
- Màn hình kết thúc ca chơi (Game Over overlay) với lý do kết thúc, bảng điểm và nút Chơi lại (hỗ trợ chuột và phím R).
- Chuyển giao kho nguyên liệu nguyên tử giữa 2 buổi qua `inventory.json`.
