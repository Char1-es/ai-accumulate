"""Mini NPU 시뮬레이터: MAC(Multiply-Accumulate) 연산 기반 패턴 판별기."""

from modes import run_json_mode, run_user_mode


def main():
    print("=== Mini NPU Simulator ===")
    while True:
        print("\n1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")
        try:
            choice = input("선택> ").strip()
        except EOFError:
            break
        if choice == "1":
            run_user_mode()
            break
        if choice == "2":
            run_json_mode()
            break
        if choice == "0":
            break
        print("1, 2, 0 중에서 선택하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n종료합니다.")
