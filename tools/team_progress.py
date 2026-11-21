"""Tiến độ từng người: python3 tools/team_progress.py

Fetch remote, in bảng: nhánh, người, commit gần nhất, số commit vượt main, thời gian.
Dùng để cập nhật standup mà không phải mở GitHub.
"""

import subprocess
import sys

ROOT = "."
BRANCHES = [
    ("feat/cao-minh", "Cao Minh"),
    ("feat/nhat-minh", "Nhật Minh"),
    ("feat/quang-vinh", "Vinh"),
    ("feat/van-minh", "Văn Minh"),
    ("feat/duc-minh", "Đức Minh"),
]


def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else ""


def main():
    git("fetch", "--prune", "origin")
    base = git("rev-list", "--max-parents=0", "origin/main")
    print(f"{'nhánh':22} {'người':10} {'vượt main':>9}  {'commit gần nhất'}")
    print("-" * 92)
    total = 0
    for branch, who in BRANCHES:
        ref = f"origin/{branch}"
        if not git("rev-parse", "--verify", ref):
            print(f"{branch:22} {who:10} {'—':>9}  (chưa có trên remote)")
            continue
        ahead = git("rev-list", "--count", f"origin/main..{ref}") or "0"
        total += int(ahead)
        if git("rev-parse", ref) == git("rev-parse", "origin/main"):
            print(f"{branch:22} {who:10} {ahead:>9}  (chưa bắt đầu — trùng main)")
            continue
        log = git("log", "-1", "--format=%an|%ar|%s", ref)
        print(f"{branch:22} {who:10} {ahead:>9}  {log}")
    print("-" * 92)
    print(f"Tổng commit vượt main: {total}  ·  main: {git('log', '-1', '--format=%h %s', 'origin/main')}")
    print(f"Từ commit gốc của giảng viên: {git('rev-list', '--count', f'{base}..origin/main')} commit trên main")
    return 0


if __name__ == "__main__":
    sys.exit(main())
