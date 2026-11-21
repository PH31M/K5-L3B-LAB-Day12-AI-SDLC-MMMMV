"""Adapter file kho hai schema (ADR-0001). Một chỗ duy nhất quyết định schema theo contract.

- v1.0/v1.1 (tuning không có `freshness`): kho đếm `{"items": {kind: số nguyên >= 0}}`.
- v1.2+ (tuning có `freshness`): kho cá thể `{"items": [{"id", "kind", "fresh"}, ...]}`.

Đọc: từ chối schema còn lại, sai schema, kind lạ, id trùng, fresh ngoài [0, 100] (BadInput -> mã 2).
Ghi: qua file tạm cùng thư mục rồi thay thế nguyên tử, byte-ổn-định; kho cá thể xuất theo id.
"""

import json
import math
import os
import tempfile

from .errors import BadInput
from .ids import sort_by_id

KINDS_P1 = ("ca_loc", "ca_linh", "ca_keo", "bong_dien_dien", "bong_sung", "keo_neo")


def individual_schema(tuning) -> bool:
    """True khi contract dùng kho cá thể (v1.2 trở lên: có khối `freshness`)."""
    return bool(tuning) and tuning.get("freshness") is not None


def validate_items(items, kinds=KINDS_P1):
    """Kho đếm (v1.0/v1.1)."""
    if not isinstance(items, dict):
        raise BadInput("items phải là object đếm theo loại (kho v1.1)")
    out = {}
    for k, v in items.items():
        if k not in kinds:
            raise BadInput(f"nguyên liệu lạ: {k}")
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise BadInput(f"số lượng không hợp lệ cho {k}: {v!r}")
        if v > 0:
            out[k] = v
    return out


def validate_individuals(items, kinds=KINDS_P1, name="items"):
    """Kho cá thể (v1.2): mảng {id, kind, fresh}; id chuỗi khác rỗng, duy nhất; fresh hữu hạn trong [0, 100]."""
    if not isinstance(items, list):
        raise BadInput(f"{name} phải là mảng cá thể {{id, kind, fresh}} (kho v1.2)")
    seen = set()
    out = []
    for it in items:
        if not isinstance(it, dict) or set(it) != {"id", "kind", "fresh"}:
            raise BadInput(f"{name}: mỗi cá thể phải có đúng các khóa id, kind, fresh")
        ident, kind, fresh = it["id"], it["kind"], it["fresh"]
        if not isinstance(ident, str) or not ident:
            raise BadInput(f"{name}: id phải là chuỗi khác rỗng")
        if ident in seen:
            raise BadInput(f"{name}: id trùng {ident}")
        seen.add(ident)
        if kind not in kinds:
            raise BadInput(f"{name}.{ident}: nguyên liệu lạ {kind!r}")
        if (isinstance(fresh, bool) or not isinstance(fresh, (int, float)) or not math.isfinite(fresh)
                or not 0 <= fresh <= 100):
            raise BadInput(f"{name}.{ident}: fresh phải hữu hạn trong [0, 100]")
        out.append({"id": ident, "kind": kind, "fresh": fresh})
    return out


def _reject_constant(name):
    raise ValueError(f"giá trị {name} không phải số hữu hạn")


def read_inventory(path: str, kinds=KINDS_P1, individual=False):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f, parse_constant=_reject_constant)
    except (OSError, ValueError) as e:
        raise BadInput(f"không đọc được file kho {path}: {e}")
    if not isinstance(data, dict) or set(data.keys()) != {"items"}:
        raise BadInput("file kho chỉ được có khóa gốc 'items'")
    if individual:
        if isinstance(data["items"], dict):
            raise BadInput("contract v1.2 không nhận file kho đếm theo loại")
        return validate_individuals(data["items"], kinds)
    if isinstance(data["items"], list):
        raise BadInput("contract v1.1 không nhận file kho cá thể")
    return validate_items(data["items"], kinds)


def hold_to_items(hold: list) -> dict:
    """Khoang (mảng id theo thứ tự nhặt) -> object đếm, sắp theo id nguyên liệu."""
    counts = {}
    for k in hold:
        counts[k] = counts.get(k, 0) + 1
    return {k: counts[k] for k in sorted(counts)}


def write_inventory(path: str, items):
    """`items` là dict (kho đếm) hoặc mảng cá thể đã xuất {id, kind, fresh} (kho v1.2)."""
    if isinstance(items, list):
        payload = sort_by_id([{"id": it["id"], "kind": it["kind"], "fresh": it["fresh"]} for it in items])
    else:
        payload = {k: items[k] for k in sorted(items) if items[k] > 0}
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".inv-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"items": payload}, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
