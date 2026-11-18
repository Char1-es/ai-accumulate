"""입출력/표시 보조 함수."""

from constants import LABEL_MAP
from matrix import Matrix


def normalize_label(raw):
    """expected/filter 키를 표준 라벨(Cross/X)로 변환. 알 수 없으면 ValueError.

    별도 함수로 분리한 이유:
    - 중앙화: 필터 키(load_filters)와 expected 값(evaluate_case)이 같은 규칙을
      쓰도록 한 곳에서만 정규화한다. 표기 규칙이 바뀌어도 LABEL_MAP만 고치면 된다.
    - 재사용: 두 호출부가 "+", "cross", "x" 등 다양한 표기를 동일하게 받는다.
    - 검증: 알 수 없는 라벨은 여기서 ValueError로 막아, 이후 로직은 표준 라벨
      (Cross/X)만 다루면 된다.
    """
    if isinstance(raw, str):
        key = raw.strip().lower()
        if key in LABEL_MAP:
            return LABEL_MAP[key]
    candidates = ", ".join(repr(k) for k in LABEL_MAP)
    raise ValueError(f"알 수 없는 라벨: {raw!r} (사용 가능: {candidates})")


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
                print(f"  올바른 예: {' '.join(['1', '0', '1', '0', '1'][:n])}")
                ok = False
                break
            try:
                rows.append([float(t) for t in line])
            except ValueError:
                print("입력 형식 오류: 숫자만 입력할 수 있습니다.")
                print(f"  올바른 예: {' '.join(['1', '0', '1', '0', '1'][:n])}")
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
