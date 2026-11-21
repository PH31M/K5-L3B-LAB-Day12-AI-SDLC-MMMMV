# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - Phase 4 (Phát hành v1.0.0 — Contract v1.3)
### Added
- **Contract v1.3:** Khai báo chính thức `bench_cmd` và `soak_cmd` trong `game.contract.json`.
- **Soak Testing 10 Ngày (`tools/soak.py`):** Lệnh kiểm thử sức bền 10 ngày headless liên tục với bot tất định, bảo toàn tiền, uy tín, nâng cấp xuyên suốt 3 pha `gather -> quan -> shop`, xuất `docs/proof/phase-4/soak.json` trong 0.77s với 0 crash.
- **Benchmark FPS Browser (`tools/bench.py`):** Đo đạc hiệu năng render 60 FPS trên trình duyệt Chromium/Playwright thật tại độ phân giải chuẩn 1280×720, xuất `docs/proof/phase-4/bench.json`.
- **Cảnh báo nguy hiểm & Chế độ tương phản cao (High Contrast):**
  - 3 cảnh báo trực quan bằng biểu tượng + chữ: 🐊 Thủy quái gần, 🫁 Hết hơi, 😡 Khách sắp giận.
  - Phím `C` và nút `👁️ Tương phản` bật giao diện tương phản cao hỗ trợ người dùng khiếm thị màu.
  - Cờ `?hc=1` trên URL khởi động trực tiếp chế độ tương phản.

## [1.2.0] - Phase 3 (Mùa Nước Nổi — Contract v1.2)

> Ghi chú: mục này trước đây đã ghi "chuyển kho sang cá thể" khi code chưa làm. Luật v1.2 chỉ thật sự bật ở
> commit tích hợp Phase 3 (manifest có khối `freshness`). Manifest hiện ghi `"1.3"`, gồm toàn bộ luật v1.2
> (spec Phase 4: v1.3 chỉ thêm lệnh) — xem `docs/clarify.md` Q14.

### ⚠ Breaking change — kho đếm → kho cá thể
- **File kho** (`--inventory`, `--inventory-out`, `gather_end.data.inventory`):
  `{"items":{"ca_loc":1}}` → `{"items":[{"id":"I1","kind":"ca_loc","fresh":100}]}`. Kho rỗng là `{"items":[]}`.
  Xuất theo id, `fresh` đủ chính xác để đọc lại đúng giá trị và nhánh ở ngưỡng 30.
- **Adapter hai schema** (`chonoi/inventory.py`, ADR-0001): manifest có `freshness` ⇒ chỉ nhận kho cá thể;
  file kho đếm, id trùng/rỗng, kind lạ, `fresh` ngoài [0, 100] hoặc không hữu hạn → **mã 2**. Manifest v1.1
  (không có `freshness`) vẫn đọc/ghi kho đếm như cũ.
- **Scenario:** `gather.hold` và `quan.stock` là mảng cá thể; `customers[].reserved` là **mảng id**.
- **JSONL:** snapshot `hold`, `stock` (quán + Shop), `customers[].reserved` theo schema mới;
  `cook_started.data.items` là mảng cá thể sắp theo kind rồi id; `lost` trong `monster_hit`/`faint` là mảng cá thể
  theo thứ tự bỏ LIFO. Payload `gather`/`fish_caught` **không đổi** so với v1.1.
- **Giá:** `cook_started.base_price = floor(giá niêm yết × trung bình fresh của các id dùng / 100)`; boa tính trên giá đã chốt.

### Added
- **Manifest:** khối `freshness {initial:100, gather_decay_per_s:0.5, quan_decay_per_s:0.25, spoiled_below:30}` (kiểm dải).
- **Độ tươi chính xác** (`chonoi/sim/freshness.py`): 1 điểm = 240 units; giỏ hao 2 units/tick, kho quán 1 unit/tick,
  kẹp đáy 0, pause dừng hao, món chín và hàng ở Shop không hao. Hàng mới `fresh = 100`, hao từ bước sau.
- **Event `spoiled {item_id, kind, location: hold|stock}`** đúng một lần khi đi từ ≥ 30 xuống < 30, theo id.
  Hàng ươn vẫn chiếm ô, không dùng nấu, không được giữ chỗ.
- **Quán giữ theo id** (`chonoi/sim/quan_stock.py`): mỗi loại lấy cá thể khả dụng tươi nhất, hòa theo id; phần giữ
  vừa ươn → nhả toàn bộ, thử giữ lại đúng một lần (theo `order_tick` rồi id bàn); không đủ → `unfulfillable`.
- **Thứ tự tick:** gather — đồng hồ/cooldown/hồi nút → hao tươi → lịch dòng lũ → bơi…; quán — đồng hồ → hao tươi kho
  + `spoiled` → giữ lại đơn bị ảnh hưởng → bếp → di chuyển/tương tác → thanh toán/kiên nhẫn/đóng ca → khách mới.
- **day:** bàn giao trong cùng tick chuyển pha, không hao thêm, giữ id và units chính xác; Ngày đầu giữ id của mẫu
  `gather.hold`, các Ngày kế cấp id mới theo thứ tự mảng với kind/fresh ban đầu; id `I…` tăng xuyên pha và Ngày.
- **Mở rộng `current` (dòng nước lũ):** `extensions: ["net", "current"]`, `gather.current {1800, 480, 120, 10, 1.5}`.
  Event `current_warning {starts_at_phase_tick}` (t−120), `current_start {direction, duration_ticks}` (trước di chuyển
  ở t), `current_end {direction, reason: elapsed|phase_end}`; lực 1.5 m/s khi d đầu bước ≥ 10, không tích lũy vào
  `player.vel`; snapshot `current: null | {direction, ticks_left}`. Scenario `random_current:false`, `current_direction:-1|1`.
- **Test:** `tests/test_freshness_v12.py` (18 ca hộp đen: ngưỡng 30, thứ tự id, bàn giao hai tiến trình, ngưỡng sau
  bàn giao, kho rỗng khi ngất, mã 2, giữ lại khi ươn, `unfulfillable`, giá `floor`, pause, Ngày 2, dòng lũ).

### Cách cập nhật fixture (v1.1 → v1.2)
```jsonc
// gather.hold
["ca_loc", "bong_sung"]                       →  [{"id":"I1","kind":"ca_loc","fresh":100},{"id":"I2","kind":"bong_sung","fresh":100}]
// quan.stock
{"ca_loc": 2}                                 →  [{"id":"I1","kind":"ca_loc","fresh":100},{"id":"I2","kind":"ca_loc","fresh":100}]
// customers[].reserved
{"ca_loc": 1}                                 →  ["I1"]     // bỏ trống thì sim tự giữ tươi nhất theo order_tick rồi id bàn
// đơn assigned / served / unfulfillable
"reserved": {}                                →  "reserved": []
```
- Id phải duy nhất giữa các nơi chứa; muốn kiểm nhánh ươn thì đặt `fresh: 30` (ươn ở bước đầu).
- So độ tươi với dung sai ±0.01 (JSONL làm tròn 3 chữ số; file kho giữ đủ chính xác). Kiểm nhánh ngưỡng bằng event/trạng thái.
- Test cũ đổi vì luật mới: `docs/verification/phase-3.md` mục "Test phải sửa — lý do".

### Điều kiện bật v1.2 (ADR-0001) — đã đạt
Gather và quán cùng dùng kho cá thể; test migration xanh (kho đếm → mã 2); smoke hai tiến trình xanh trên schema mới
(`docs/proof/phase-3/do-tuoi/smoke-p3.txt`).

### HUD v1.2 (Ticket 05, client `chonoi/web/index.html`)
- Giỏ: số lượng theo loại kèm **độ tươi thấp nhất (%)** tô màu xanh ≥ 60 / vàng ≥ 40 / đỏ; nhãn `⚠ n ƯƠN (chiếm ô)`.
- Kho quán: kho khả dụng (tồn chưa ươn − phần giữ theo id) kèm % tươi thấp nhất và `⚠ n ươn`; bảng phấn đọc
  `reserved` là mảng id.
- Bắt đầu nấu: chữ nổi `Tươi x% → giá` tại bếp (giá đã chốt theo độ tươi).
- Toast + âm thanh cho `spoiled` (một lần mỗi cá thể, ghi giỏ/kho); dòng lũ: báo trước (chữ + 🌊 + âm), băng
  `NƯỚC XIẾT ← / →` khi đang chảy, báo khi dịu. Đọc được ở tương phản cao (`C`) và `?fx=0`.
- Bằng chứng ảnh: `docs/proof/phase-3/do-tuoi/`.

## [1.1.0] - Phase 2 (Một Ngày Ở Chợ Nổi — Contract v1.1)
### Added
- **Contract v1.1:** 8 đàn cá, 3 loài cá (`ca_loc`, `ca_linh`, `ca_keo`), 6 loại nguyên liệu (+`keo_neo`), thực đơn 6 món.
- **Quái vật Cá Sấu (Ticket 03):** Tuần tra 1.0 m/s, truy đuổi 3.0 m/s khi $d \ge 10$ và cách $\le 10$m, tấn công trừ 1 Máu và rơi nửa giỏ LIFO, bất tử 90 tick, recoil lùi 2m.
- **Mở rộng Quán Ăn (Ticket 04):**
  - 2 bếp nấu B1 [2,8], B2 [5,8] nấu song song độc lập không giẫm đơn nhau.
  - 4 bàn ăn T1–T4 đón khách theo nhịp $120 + 900 \cdot k$, giải phóng bàn khi khách ăn xong.
  - Thực đơn 6 món hỗ trợ đầy đủ nguyên liệu mới (`ca_keo`, `keo_neo`).
  - Hỗ trợ lọc thực đơn theo kế hoạch ngày (`day_plan.dishes`) ở chế độ `day`.
  - Phát sự kiện `no_dish` khi có bàn trống nhưng hết món đủ nguyên liệu.
- **Vòng lặp Ngày 5 Ngày:** `--mode day --days 1..5` và Shop nâng cấp bình oxy, áo phao.
- **Âm thanh tự sinh (Procedural Web Audio API):**
  - Tự động phát âm thanh khi lặn/nổi nước, hái rau, bắt cá, chuông bếp, cập bến, trả tiền, còi báo và va chạm cá sấu.
  - Nút Bật/Tắt âm thanh `🔊 / 🔇` trực tiếp trên canvas và phím tắt `M`.
- **Hiệu ứng đồ họa (VFX Particles & Ánh Sáng):**
  - Hạt bọt khí oxy nổi lên khi lặn sâu + vệt rẽ nước khi bơi nhanh.
  - Tia nắng xuyên đáy nước (God rays / Sunbeams) và ánh đèn lồng ấm cúng buổi tối.
  - Rung chấn màn hình (Screen Shake) và chữ nổi động (Floating Text).
  - Sóng nước lăn tăn nhấp nhô nhẹ trên mặt sông.

## [1.0.0] - Phase 1 (Kickoff & Core Gameplay)
### Added
- **Lõi hai buổi (contract v1.0):**
  - Lặn & hái: oxy, ngạt (choke ở `t+59`), ngất bỏ giỏ theo LIFO, hái nút + mọc lại, bắt cá (xóa đàn, hồi chiêu 30 tick), cập bến, ghi file kho.
  - Mở quán: khách đến theo lịch, giữ chỗ theo công thức, kiên nhẫn, nấc/bưng/phục vụ, boa theo ngưỡng, đóng ca.
  - Cổng kiểm một lệnh; ma trận truy vết và bằng chứng trong `docs/proof/`.
- **Giao diện HUD trực quan 2 buổi (Ticket 06):**
  - Đồng hồ đếm ngược, thanh oxy đổi 3 màu, tim Máu, giỏ hàng trực quan.
  - Hệ thống banner nhắc phím ngữ cảnh (Contextual Prompts) khi vào phạm vi bến tàu, nút rau, đàn cá, bếp nấu, bàn ăn.
  - Màn hình kết thúc ca chơi (Game Over overlay) với lý do kết thúc, bảng điểm và nút Chơi lại (hỗ trợ chuột và phím R).
  - Chuyển giao kho nguyên liệu nguyên tử giữa 2 buổi qua `inventory.json`.
