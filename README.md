# Day 12 — AI SDLC: Quán Ăn Chợ Nổi

> **Làm theo nhóm 4–6 người** · Dùng AI để xây game 2D qua **4 phase** trong **3 giờ**: Út Sen lặn bắt cá, hái rau trên mặt nước rồi tối mở quán phục vụ khách.
> **Yêu cầu từng phase mở đúng mốc giờ tại lab board:** **[Chợ Nổi Lab](https://claude.ai/artifact/E35v787wSx2wDgPTNhMVDg)** (cần đăng nhập claude.ai; có trợ giảng AI cho từng phase).

## Bắt buộc (chỉ có thế)

Cách làm việc kỹ thuật là **tự do** (push thẳng, nhánh + PR, pair, có hay không CI…). Cái bắt buộc:

1. **Một repo chung:** trưởng nhóm **fork** repo này, đặt tên `K5-L3B-LAB-Day12-AI-SDLC-<ten-nhom>`, thêm mọi thành viên làm collaborator (*Settings → Collaborators*, quyền Write) và để repo **public** (giảng viên xem được, không cần mời).
2. **Cả nhóm cùng commit** bằng tài khoản GitHub của mình, mỗi người **≥ 3 commit có nội dung** (làm cặp thì ghi `Co-authored-by:`).
3. **Điền [`TEAM.md`](TEAM.md):** danh sách thành viên + thỏa thuận làm việc nhóm; sửa `team_size` trong [`game.contract.json`](game.contract.json). Commit của người không có trong `TEAM.md` không được tính.
4. **Gắn tag** `phase-1` … `phase-4` đúng hạn; chạy được tại từng tag.
5. **Ghi chép tối thiểu:** `docs/verification/phase-n.md`, `docs/clarify.md`, `docs/ai-usage-log.md`, `docs/retro.md`, `docs/members/<handle>.md`.

## Bắt đầu nhanh

```bash
git clone <fork-của-nhóm> && cd <fork-của-nhóm>
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v        # smoke test
python3 -m chonoi.live --mode gather                                # chơi thử trên trình duyệt (tùy chọn)
```

Game cần chế độ **headless** theo Test Contract (`python3 -m chonoi.headless --mode gather|quan …`) để được chạy và chấm tự động. **Công nghệ không ràng buộc**: khung Python trong `chonoi/` chỉ là gợi ý, chi tiết ở [`docs/STARTER.md`](docs/STARTER.md).

## Tự do sáng tạo

Ngoài phần đề yêu cầu, nhóm được **thêm** nhân vật, loài cá/cây, sinh vật, món, bản đồ, cơ chế, câu chuyện, đồ họa, âm nhạc… với ba điều kiện: **không phá phần cố định** (tắt ở headless), ghi mục **"Sáng tạo của nhóm"** trong README của nhóm, và **làm lõi đúng trước**.

## Lịch 3 giờ

| Mốc | Phase | Hạn tag |
|---|---|---|
| 0:00 | Phase 1 (PRD-0) | `phase-1` trước 1:00 |
| 1:00 | Phase 2 | `phase-2` trước 1:55 |
| 1:55 | Phase 3 | `phase-3` trước 2:30 |
| 2:30 | Phase 4 | `phase-4` + Release `v1.0.0` trước 3:00 |

Hết giờ mỗi phase thì gắn tag rồi đi tiếp; chỗ chưa xong ghi trung thực trong bằng chứng.

## Đánh giá (100 điểm)

| Hạng mục | Điểm |
|---|---|
| Test tự động ẩn (headless, gồm kiểm tra lại phase trước) | 25 |
| Làm việc nhóm (một repo chung, chia việc, tích hợp, đổi yêu cầu) | 25 |
| Kiểm chứng & bằng chứng | 15 |
| Harness AI (AGENTS.md, skill, nhật ký dùng AI) | 10 |
| Đánh giá & retro | 10 |
| Chất lượng sản phẩm (đúng yêu cầu, mở rộng/sáng tạo) | 10 |
| Demo | 5 |

## Quy định

- Dùng AI thoải mái; **không sao chép repo của nhóm khác**; bằng chứng phải thật.
- Nhân vật, bối cảnh là bản gốc của lab; asset ngoài chỉ dùng CC0/CC-BY/MIT hoặc tự tạo, ghi nguồn trong `CREDITS.md`. Không commit API key, token, `.env`.

---

## Nhóm MMMMV — chạy thử

Ba lệnh từ clone sạch (macOS/Linux, Python 3.10+):

```bash
git clone https://github.com/PH31M/K5-L3B-LAB-Day12-AI-SDLC-MMMMV.git && cd K5-L3B-LAB-Day12-AI-SDLC-MMMMV
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
python3 -m chonoi.live --mode gather
```

**Điều khiển:** WASD hoặc mũi tên để bơi/đi · `E` tương tác (cập bến, hái, nấu, bưng, dọn món) · `Space` bắt cá · `P`/`Esc` tạm dừng · `R` chơi lại · `M` âm thanh · `C` tương phản cao · Shop: `1/2/3` mua, `Enter` đóng. URL: `?fx=0` tắt hiệu ứng, `?hc=1` tương phản cao, `?fps=1` hiện FPS.
**Chơi trọn một ngày:** `python3 -m chonoi.live --mode day --days 1` (Gather → cập bến → Quán → Shop → tổng kết).

### Sáng tạo của nhóm

- **Đồ họa 2D làng quê Nam Bộ** (chỉ ở client trình duyệt, headless không đổi): ca sáng là mặt cắt sông với trời bình minh, núi xa có sương, ruộng lúa, lũy tre, nhà tranh/nhà ngói, bến Má Tư; nước chia tầng nông–giữa–sâu theo màu phù sa. Cá lóc, đàn cá linh, cặp cá kèo và Cá Sấu Năm Chèo có hình riêng; bông súng, điên điển, kèo nèo khác nhau và hiện vòng mọc lại. Ca tối là quán nhà bè mái ngói, gạch tàu, dây đèn vàng trên sông đêm; bảng phấn cho biết món nào đủ nguyên liệu và đơn nào bếp sẽ nấu kế tiếp. Cuối ngày là ghe hàng có cây bẹo bán nâng cấp. Mọi hình vẽ thủ tục, 0 KB ảnh (xem `CREDITS.md`).
- **Lặn/nổi nhanh khi chơi trên trình duyệt:** `chonoi.live` nhân tốc độ trục dọc ở ca sáng ×1.75 (≈ 7 m/s; ngang giữ 4 m/s). Đổi bằng `--dive-speed-mult N` (`1` = đúng contract). Headless, JSONL và test không bị ảnh hưởng vì manifest không có khóa `live_vertical_speed_mult`.
- **HUD theo pha:** cảnh, trục phím và HUD chọn theo `snapshot.phase`; kho khả dụng = tồn trừ phần khách giữ; ba cảnh báo (Thủy quái, Hết hơi, Khách sắp giận) có chữ + biểu tượng, đọc được ở tương phản cao và `?fx=0`. Bằng chứng: `docs/proof/phase-4/do-hoa-2d/`.
**Headless:** `python3 -m chonoi.headless --mode gather --seed 1 --ticks 600 --out out.jsonl`
**Tính điểm:** `score = earned + 100 × floor(reputation)`.
**Chơi trọn hai buổi:** `--mode gather --inventory-out kho.json`, rồi `--mode quan --inventory kho.json`.

Bằng chứng kiểm chứng: `python3 tools/run_checks.py` · ma trận: `docs/verification/phase-1.md` · kế hoạch: `docs/plan/`.
