"""핵심 연산: MAC, 시간 측정, 판정."""

import time

from constants import EPSILON, LABEL_UNDECIDED, REPEAT


def mac(pattern, filt):
    """위치별 곱셈 후 누적합 (반복문 직접 구현). 점수 반환."""
    n = pattern.n
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern.data[i][j] * filt.data[i][j]
    return total


def measure_ms(pattern, filt, repeat=REPEAT):
    """MAC 연산만 repeat회 측정한 평균 시간(ms)."""
    elapsed = 0.0
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        elapsed += time.perf_counter() - start
    return elapsed / repeat * 1000


def judge(score_a, score_b, label_a, label_b):
    """epsilon 기반 비교. 동점이면 UNDECIDED."""
    if abs(score_a - score_b) < EPSILON:
        return LABEL_UNDECIDED
    return label_a if score_a > score_b else label_b
