"""입출력/표시 보조 함수."""

from constants import LABEL_MAP
from matrix import Matrix


def normalize_label(raw):
    """expected/filter 키를 표준 라벨(Cross/X)로 변환. 알 수 없으면 ValueError."""
    if isinstance(raw, str):
        key = raw.strip().lower()
        if key in LABEL_MAP:
            return LABEL_MAP[key]
    raise ValueError(f"알 수 없는 라벨: {raw!r}")


def read_matrix(title, n=3):
    """한 줄씩(공백 구분) 입력받아 n×n Matrix 반환. 오류 시 재입력."""
    while True:
        print(f"{title} ({n}줄, 줄마다 {n}개 숫자를 공백으로 구분)")
        rows = []
        ok = True
        for i in range(n):
            line = input(f"  {i + 1}행> ").split()
            if len(line) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                ok = False
                break
            try:
                rows.append([float(t) for t in line])
            except ValueError:
                print("입력 형식 오류: 숫자만 입력할 수 있습니다.")
                ok = False
                break
        if ok:
            return Matrix(rows)
        print("처음부터 다시 입력해 주세요.\n")


def print_perf_table(rows):
    print("\n" + "-" * 44)
    print(f"{'크기(NxN)':<12}{'평균 시간(ms)':>16}{'연산 횟수(N²)':>16}")
    print("-" * 44)
    for n, ms in rows:
        print(f"{f'{n}x{n}':<12}{ms:>16.6f}{n * n:>16}")
    print("-" * 44)
