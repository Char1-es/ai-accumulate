"""공용 상수."""

import os

# 부동소수점 누적 오차(약 1e-15)보다 충분히 크고, 의미 있는 점수 차이(0.1 단위)보다
# 충분히 작은 값. 점수 스케일이 크게 달라지면 이 값을 조정한다.
EPSILON = 1e-9
REPEAT = 10
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

LABEL_CROSS = "Cross"
LABEL_X = "X"
LABEL_UNDECIDED = "UNDECIDED"

# 라벨 정규화 테이블 (소문자 기준)
LABEL_MAP = {"+": LABEL_CROSS, "cross": LABEL_CROSS, "x": LABEL_X}
