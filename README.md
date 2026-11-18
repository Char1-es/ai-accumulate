# ai-accumulate — Mini NPU 시뮬레이터

NPU의 핵심 연산인 **MAC(Multiply-Accumulate, 곱셈 후 누적합)** 을 직접 구현하고,
패턴(입력 행렬)이 필터와 얼마나 일치하는지 점수로 비교해 **Cross(+) / X** 를 판별하는 콘솔 프로그램입니다.

## 실행 방법

Python 3.8 이상이면 되고, 외부 라이브러리는 필요 없습니다.

```bash
python3 main.py
```

```
=== Mini NPU Simulator ===

1. 사용자 입력 (3x3)
2. data.json 분석
0. 종료
```

### 모드 1: 사용자 입력 (3x3)
필터 A, 필터 B, 패턴을 한 줄씩(공백 구분) 입력하면 각 필터와의 MAC 점수, 판정 결과, 연산 시간을 출력합니다.
입력 형식이 틀리면 안내 메시지와 함께 처음부터 다시 입력받습니다.

```
필터 A (3줄, 줄마다 3개 숫자를 공백으로 구분)
  1행> 0 1 0
  2행> 1 1 1
  3행> 0 1 0
```

### 모드 2: data.json 분석
`data.json`의 필터와 패턴 케이스를 읽어 자동으로 판정하고, PASS/FAIL과 성능 표, 결과 요약을 출력합니다.

## 동작 원리

1. **MAC 연산**: 패턴과 필터의 같은 위치 값을 곱해 모두 더합니다. (`mac.py`, 반복문 직접 구현)
2. **판정**: 두 점수를 비교해 높은 쪽을 선택합니다. 차이가 `EPSILON(1e-9)` 미만이면 `UNDECIDED` 입니다.
3. **성능 측정**: MAC 연산만 10회 반복한 평균 시간(ms)을 구하고, 크기(N×N)별 연산 횟수(N²)와 함께 표로 보여줍니다.

## data.json 형식

```json
{
  "meta": { ... },
  "filters": {
    "size_5": { "cross": [[...]], "x": [[...]] }
  },
  "patterns": {
    "size_5_1": { "input": [[...]], "expected": "Cross" }
  }
}
```

- `filters`: 키는 `size_N`, 값은 `cross` / `x` 두 개의 N×N 필터
- `patterns`: 키는 `size_N_idx`, `input`은 N×N 패턴, `expected`는 기대 라벨
- 라벨은 `+`, `cross`, `x` 를 대소문자 구분 없이 받아 `Cross` / `X` 로 정규화합니다.

### 오류 처리
문제가 있는 항목은 프로그램을 멈추지 않고 해당 케이스만 FAIL 처리하고 사유를 출력합니다.

- 파일 없음, JSON 파싱 실패
- 행/열 불일치, 숫자가 아닌 값
- 필터와 패턴의 크기 불일치, 필터 누락
- 알 수 없는 라벨, 키 형식 오류

## 프로젝트 구조

```
ai-accumulate/
├── main.py          # 진입점 (메뉴 선택)
├── modes.py         # 실행 모드: run_user_mode, run_json_mode, evaluate_case
├── matrix.py        # Matrix 클래스, validate_square
├── mac.py           # mac, measure_ms, judge
├── io_utils.py      # read_matrix, normalize_label, print_perf_table
├── data_loader.py   # load_data, load_filters, parse_size
├── constants.py     # EPSILON, REPEAT, 라벨 상수 등
└── data.json        # 필터와 패턴 데이터
```

의존 방향은 `main → modes → (data_loader, io_utils, mac) → matrix → constants` 순이라 순환 참조가 없습니다.
