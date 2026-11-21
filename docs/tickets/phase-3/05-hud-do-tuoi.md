# 05: HUD độ tươi / hàng ươn

**What to build:** Người chơi nhìn là biết con nào sắp bỏ: số độ tươi hoặc thanh, và dấu hiệu rõ cho hàng đã ươn — trong giỏ lẫn trong kho quán.

**Blocked by:** 01 (mềm: 02, 03 — thiếu trường thì fallback)

**Status:** ready-for-agent

- [ ] Giỏ buổi sáng: mỗi ô hiện độ tươi (số hoặc thanh), đổi màu theo ngưỡng 30; cá thể ươn có nhãn/biểu tượng riêng.
- [ ] Kho quán + Shop: hiện độ tươi từng cá thể, hàng ươn bị làm mờ/gạch và không gợi ý nấu.
- [ ] `spoiled` hiện thông báo ngắn đúng một lần cho mỗi cá thể (không spam khi đang hao liên tục).
- [ ] Có `?fx=0` tắt hiệu ứng nặng; không che vùng chơi.
- [ ] Thiếu trường `fresh` (chạy v1.0/1.1) thì HUD ẩn phần độ tươi, không văng lỗi.
- [ ] Không thêm mã vào `chonoi/`; headless không đổi một byte.
