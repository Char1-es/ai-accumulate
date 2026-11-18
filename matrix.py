"""데이터 구조: Matrix와 크기 검증."""


class Matrix:
    """n×n 2차원 배열 (패턴/필터 공용)."""

    def __init__(self, rows):
        self.n = len(rows)
        self.data = [list(map(float, r)) for r in rows]

    def get(self, r, c):
        return self.data[r][c]

    def set(self, r, c, value):
        self.data[r][c] = float(value)

    def show(self):
        for row in self.data:
            print("  " + " ".join(f"{v:g}" for v in row))


def validate_square(rows):
    """rows가 n×n 숫자 2차원 배열인지 검증. 문제 있으면 ValueError."""
    if not isinstance(rows, list) or not rows:
        raise ValueError("2차원 배열이 아닙니다")
    n = len(rows)
    for i, row in enumerate(rows):
        if not isinstance(row, list):
            raise ValueError(f"{i + 1}번째 행이 배열이 아닙니다")
        if len(row) != n:
            raise ValueError(f"행/열 불일치: {n}행인데 {i + 1}번째 행은 {len(row)}열")
        for v in row:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValueError(f"숫자가 아닌 값 포함: {v!r}")
    return n
