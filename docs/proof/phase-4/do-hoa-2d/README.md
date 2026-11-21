# Đồ họa 2D làng quê Nam Bộ + HUD theo pha — bằng chứng kiểm

Ngày kiểm: 2026-11-21 · Máy: Windows 11, Python 3.12.5, Chromium headless (Playwright) 1280×720.
Phạm vi đổi: chỉ `chonoi/web/index.html`. Không đổi `chonoi/sim/`, `runner.py`, `live.py`, `contract.py`, `game.contract.json`.

## 1. Lỗi đổi pha trong `--mode day` (đã sửa)

Tái hiện trên bản cũ: `python -m chonoi.live --mode day --days 1`, bấm E ở bến → backend chuyển `phase: "quan"` (mode vẫn `day`, `meta.bounds` = `{x, z}`).
Client cũ chọn cảnh theo `mode` nên vẫn vẽ Gather và đọc `bounds.d[1]` → **103 `pageerror`** "Cannot read properties of undefined (reading '1')" trong ~1,5 s, màn đứng ([before-day-quan.jpg](before-day-quan.jpg)).

Bản mới: cảnh, trục điều khiển, hạt và HUD chọn theo `snapshot.phase` (`gather | quan | shop`), `mode` chỉ là dự phòng; khi đổi cảnh client gửi lại trạng thái phím ngay để trục `[x,d]` → `[x,z]` đúng từ khung đầu; meta thiếu `bounds.d`/`bounds.z` thì dùng mặc định thay vì văng lỗi.

## 2. Ca đã chạy trên trình duyệt thật

Script: [ui_check.py](ui_check.py) (khởi `chonoi.live`, bấm phím thật, đọc `/state`, gom `pageerror` + `console.error/warning`).
Kết quả thô: [ui-check-results.json](ui-check-results.json), [ui-check-day-rerun.json](ui-check-day-rerun.json).

| Ca | Lệnh / fixture | Kết quả đo | Lỗi console | Ảnh |
|---|---|---|---|---|
| Gather độc lập | `--mode gather --seed 1`, giữ D rồi S | Út Sen [2,0] → [6.98,7.07]; cảnh = gather | 0 | [gather-surface](gather-surface.jpg), [gather-dive](gather-dive.jpg) |
| Cảnh báo Thủy quái + Hết hơi | scenario `player.pos [57,22]`, `oxygen_ticks 300` | M1 `chase`; hai băng cảnh báo chữ + biểu tượng + viền màn | 0 | [gather-warnings](gather-warnings.jpg) |
| Tương phản cao (C) | như trên, bấm C | cảnh báo vẫn đọc được trên nền đen, chữ viền | 0 | [gather-warnings-hc](gather-warnings-hc.jpg) |
| `?fx=0` | như trên | không hạt/sóng/mây trôi; cảnh báo hiện tĩnh | 0 | [gather-fx0](gather-fx0.jpg) |
| Quán fixture (kho, 2 bếp, 4 bàn) | `--mode quan` + B1 cooking, B2 ready, C1 kiên nhẫn 700/3600, C4 đang ăn | E ở B2 → `hand` = lẩu C3; W làm z tăng; dọn ở T3 → `dish_picked`, `served` | 0 | [quan-fixture](quan-fixture.jpg), [quan-carry](quan-carry.jpg) |
| Khách sắp giận (<25%) | C1 bàn T1 | nhãn "SẮP GIẬN · Ns" tại bàn + băng HUD | 0 | [quan-fixture](quan-fixture.jpg), [quan-hc](quan-hc.jpg) |
| Tạm dừng P | trong Quán | `state` = `paused` → bấm P lại `playing` | 0 | [quan-pause](quan-pause.jpg) |
| Quán mặc định | `--mode quan --seed 1` | khách đến theo lịch | 0 | [quan-plain](quan-plain.jpg) |
| **Luồng ngày** | `--mode day --days 1 --seed 3`, scenario `day.money 450`, `quan.time_left_ticks 600` | E ở bến → `phase quan`, cảnh client `quan`, W làm z tăng → Shop (`meta.max_ticks 600`) → phím 1 mua oxygen (450→250, `active_upgrades` vẫn `{}`) → phím 3 mua net (→0) → phím 2 `buy_failed funds` → Enter → `finished`, `days_complete` | 0 | [day-1](day-1-gather-intro.jpg) … [day-7](day-7-summary.jpg) |

Shop phân biệt cấp **đã mua** (viền vàng, "hiệu lực Ngày sau") với cấp **đang dùng** (ô xanh) theo `upgrades` / `active_upgrades`; giá và hiệu ứng đọc từ `meta.upgrades` server trả về.

## 3. FPS (cách repo đo: `tools/bench.py --seed 42 --duration 30`, 1280×720, Chromium headless)

| Bản | avg_fps | p1_low_fps | File |
|---|---|---|---|
| Client cũ (HEAD 6002b5d) | 59.10 | 27.70 | [bench-old.json](bench-old.json) |
| Client mới | **59.74** | **41.40** | [bench-new.json](bench-new.json) |

Mục tiêu lab ≥ 30 FPS trung bình: đạt trên máy này. Lần đo đầu của bản mới chỉ 51.3 / 16.8; sau khi nhớ đệm phép đo chữ và chuyển mây/vệt sáng sang sprite vẽ sẵn thì đạt số trên. FPS trung bình theo khung trong các ca UI (EMA trong trang): Gather 56–59, Quán 51–55, Day 59,8.

## 4. Cổng kiểm và tất định

- `PYTHONUTF8=1 python tools/run_checks.py`: unittest 191 OK · smoke gather→kho→quan PASS · tất định 52 973 byte PASS · bằng chứng PASS. (Không đặt `PYTHONUTF8=1` thì trên Windows `run_checks.py` dừng ở `UnicodeDecodeError` cp1252 — lỗi môi trường, có cả trước thay đổi này.)
- `python -m chonoi.headless --mode day --days 2 --seed 7 --ticks 30000` chạy hai lần: giống từng byte (4 954 733 byte, sha256 `C19586D426C8E1B2…`).

## 5. Lặn/nổi nhanh hơn (chỉ bản live)

Yêu cầu: Út Sen bơi lên/xuống nhanh hơn khi dùng WASD/mũi tên. Tốc độ là luật (`swim_speed` 4 m/s, test `test_move_01` kiểm ngang = xuống = chéo), nên chỉ bật ở `chonoi.live`: `live.py` gắn `live_vertical_speed_mult` (mặc định 1.75, cờ `--dive-speed-mult`) vào tuning trong bộ nhớ; `sim/gather.py` `_move` nhân tốc độ trục d với khóa này, vắng thì 1.0.

- Chromium thật, giữ phím 1 s (kể cả 6 tick tăng tốc): mặc định — xuống 7.47 m, lên 7.12 m, ngang 4.07 m; `--dive-speed-mult 1` — 4.07 / 4.07 / 4.07 m. 0 lỗi console.
- Test mới `tests/test_live.py::test_live_vertical_speed_mult_only_when_set`: không có khóa → quãng đúng `swim_speed`; ×1.75 → tỉ lệ 1.75.
- `run_checks.py`: 192 test OK, smoke/tất định/bằng chứng PASS. `headless --mode day --days 2 --seed 7` sau sửa giống từng byte bản trước.

## 6. Chưa kiểm / còn thiếu

- Chỉ đo trên Chromium headless của một máy Windows; chưa thử Firefox/Safari, màn nhỏ hơn 1000 px (bảng phấn tự ẩn) hay màn HiDPI thật.
- Âm thanh chỉ kiểm không lỗi; không nghe được trong headless.
- Chưa có menu chính / nút "Về menu" (repo chưa có trạng thái menu trong snapshot); pause có Tiếp tục và Chơi lại.
- Luồng nhiều ngày (`--days 2..5`) chưa chạy trên trình duyệt; mới kiểm 1 ngày trọn.
- Bảng phấn dùng công thức học từ snapshot (`customers[].reserved`, `cook_started.items`), thiếu thì dùng bản sao hiển thị của `menu` v1.1 trong client — nếu manifest đổi công thức mà chưa có khách gọi món đó, bảng phấn có thể lệch đến khi học được.
