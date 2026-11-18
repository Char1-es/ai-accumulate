"""data.json 로딩과 필터 파싱."""

import json
import re

from constants import DATA_PATH, LABEL_CROSS, LABEL_X
from io_utils import normalize_label
from matrix import Matrix, validate_square


def load_data(path=DATA_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_size(key):
    m = re.match(r"^size_(\d+)(?:_\d+)?$", str(key))
    if not m:
        raise ValueError(f"키 형식 오류: {key!r} (size_N_idx 형태여야 함)")
    return int(m.group(1))


def load_filters(data):
    """size_N -> {표준라벨: Matrix}. 문제 있는 필터는 오류 메시지와 함께 제외."""
    filters, errors = {}, {}
    raw_filters = data.get("filters")
    if not isinstance(raw_filters, dict):
        raise ValueError("'filters' 항목이 없거나 객체가 아닙니다")
    for size_key, group in raw_filters.items():
        try:
            if not isinstance(group, dict):
                raise ValueError("필터 그룹이 객체가 아닙니다")
            parsed = {}
            for raw_label, rows in group.items():
                label = normalize_label(raw_label)
                n = validate_square(rows)
                expected_n = parse_size(size_key)
                if n != expected_n:
                    raise ValueError(f"{raw_label} 필터 크기 {n}x{n} != {size_key}")
                parsed[label] = Matrix(rows)
            for need in (LABEL_CROSS, LABEL_X):
                if need not in parsed:
                    raise ValueError(f"{need} 필터 없음")
            filters[size_key] = parsed
        except ValueError as e:
            errors[size_key] = str(e)
    return filters, errors
