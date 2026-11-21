# PH31M — phản tư cá nhân (≤ 200 từ)

- Tôi đã làm (kèm link commit):
  - Phụ trách module `sim/quan_service` kiêm Scrum Master và Release Manager.
  - Hoàn thành bếp nấu, `ready_ticks`, bốc món, phục vụ, boa tiền ([commit `1fafcdd`](https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV/commit/1fafcdd)).
  - Mở rộng 2 bếp song song B1/B2 độc lập, vòng Ngày 5 Ngày và Shop nâng cấp P2.
  - Đóng gói v1.0.0, nâng cấp manifest contract v1.3 và điều phối Ticket 06 (Retro & Ma trận AC-P4).
- Tôi đã review (kèm link):
  - Review PR của Cao Minh và Quang Vinh về tích hợp HUD và cổng kiểm headless.
- AI sai ở đâu và tôi phát hiện thế nào:
  - AI ban đầu tăng `ready_ticks` ngay tại tick món ăn chín, làm hụt mất 1 tick của khách; tôi phát hiện khi chạy bộ test unit `test_quan_service.py` và sửa lại chỉ tăng từ tick kế tiếp theo đúng PRD.
- Điều tôi học được:
  - Tự động hóa cổng kiểm và phân chia rõ ràng trách nhiệm từng thành viên giúp đội ngũ phối hợp nhịp nhàng, release đúng tiến độ không vỡ contract.
