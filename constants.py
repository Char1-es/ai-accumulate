"""공용 상수."""

import os

EPSILON = 1e-9
REPEAT = 10
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

LABEL_CROSS = "Cross"
LABEL_X = "X"
LABEL_UNDECIDED = "UNDECIDED"

# 라벨 정규화 테이블 (소문자 기준)
LABEL_MAP = {"+": LABEL_CROSS, "cross": LABEL_CROSS, "x": LABEL_X}
