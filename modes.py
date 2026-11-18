"""실행 모드: 사용자 입력 모드 / data.json 분석 모드."""

import json

from constants import DATA_PATH, LABEL_CROSS, LABEL_UNDECIDED, LABEL_X, REPEAT
from data_loader import load_data, load_filters, parse_size
from io_utils import normalize_label, print_perf_table, read_matrix
from mac import judge, mac, measure_ms
from matrix import Matrix, validate_square


# ---------------------------------------------------------------- 모드 1
def run_user_mode():
    print("\n[필터 입력]")
    filt_a = read_matrix("필터 A")
    filt_b = read_matrix("필터 B")
    print("\n저장 확인 - 필터 A:")
    filt_a.show()
    print("저장 확인 - 필터 B:")
    filt_b.show()

    print("\n[패턴 입력]")
    pattern = read_matrix("패턴")
    print("저장 확인 - 패턴:")
    pattern.show()

    score_a = mac(pattern, filt_a)
    score_b = mac(pattern, filt_b)
    ms = measure_ms(pattern, filt_a)
    result = judge(score_a, score_b, "A", "B")

    print("\n[결과]")
    print(f"A 점수: {score_a:g}")
    print(f"B 점수: {score_b:g}")
    print(f"연산 시간: {ms:.6f} ms (평균 {REPEAT}회)")
    print(f"판정: {'판정 불가' if result == LABEL_UNDECIDED else result}")

    print("\n[성능 분석 (3x3)]")
    print_perf_table([(3, ms)])


# ---------------------------------------------------------------- 모드 2
def evaluate_case(key, item, filters, filter_errors):
    """패턴 1건 평가. (결과 dict) 반환, 예외는 FAIL로 변환."""
    res = {"key": key, "cross": None, "x": None, "judge": None, "pass": False, "reason": ""}
    try:
        if not isinstance(item, dict) or "input" not in item or "expected" not in item:
            raise ValueError("스키마 오류: 'input'/'expected' 필요")
        n = parse_size(key)
        size_key = f"size_{n}"
        if size_key in filter_errors:
            raise ValueError(f"필터 오류({size_key}): {filter_errors[size_key]}")
        if size_key not in filters:
            raise ValueError(f"{size_key} 필터 없음")
        expected = normalize_label(item["expected"])
        pn = validate_square(item["input"])
        if pn != n:
            raise ValueError(f"크기 불일치: 패턴 {pn}x{pn}, 필터 {n}x{n}")
        pattern = Matrix(item["input"])
        res["cross"] = mac(pattern, filters[size_key][LABEL_CROSS])
        res["x"] = mac(pattern, filters[size_key][LABEL_X])
        res["judge"] = judge(res["cross"], res["x"], LABEL_CROSS, LABEL_X)
        res["pass"] = res["judge"] == expected
        if not res["pass"]:
            res["reason"] = f"판정 {res['judge']} != expected {expected}"
    except (ValueError, TypeError, KeyError) as e:
        res["reason"] = str(e)
    return res


def run_json_mode():
    print("\n[data.json 로드]")
    try:
        data = load_data()
    except FileNotFoundError:
        print(f"오류: data.json을 찾을 수 없습니다 ({DATA_PATH})")
        return
    except json.JSONDecodeError as e:
        print(f"오류: data.json 파싱 실패 - {e}")
        return
    if not isinstance(data, dict):
        print("오류: data.json 최상위가 객체가 아닙니다.")
        return

    try:
        filters, filter_errors = load_filters(data)
    except ValueError as e:
        print(f"오류: {e}")
        return
    for k in filters:
        print(f"필터 로드 완료: {k} (Cross, X)")
    for k, msg in filter_errors.items():
        print(f"필터 로드 실패: {k} - {msg}")

    patterns = data.get("patterns")
    if not isinstance(patterns, dict):
        print("오류: 'patterns' 항목이 없거나 객체가 아닙니다.")
        return

    print("\n[패턴 판정]")
    results = []
    for key, item in patterns.items():
        r = evaluate_case(key, item, filters, filter_errors)
        results.append(r)
        if r["judge"] is None:
            print(f"--- {key}: FAIL ({r['reason']})")
        else:
            status = "PASS" if r["pass"] else "FAIL"
            print(f"--- {key}")
            print(f"  Cross 점수: {r['cross']:g}")
            print(f"  X 점수: {r['x']:g}")
            print(f"  판정: {r['judge']} | {status}"
                  + (f" ({r['reason']})" if r["reason"] else ""))

    # 성능 분석: 3x3(내장 샘플) + 로드된 필터 크기별
    print("\n[성능 분석]")
    perf = []
    cross3 = Matrix([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    perf.append((3, measure_ms(cross3, cross3)))
    for size_key in sorted(filters, key=parse_size):
        n = parse_size(size_key)
        f = filters[size_key][LABEL_CROSS]
        perf.append((n, measure_ms(f, f)))
    print_perf_table(perf)

    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    print("\n[결과 요약]")
    print(f"전체 테스트: {total}")
    print(f"통과: {passed}")
    print(f"실패: {failed}")
    if failed:
        print("실패 케이스:")
        for r in results:
            if not r["pass"]:
                print(f"  - {r['key']}: {r['reason']}")
