# -*- coding: utf-8 -*-
import inspect
import sys

from source.기록 import (
    일정_작성,
    일정_작성_자동,
    기록용어_표준화,
    물품_가격비교,
    기록용템플릿_출력,
    년간일정생성_4분기단위,
    물품가격비교 as 물품가격비교_func, 일정_조회  # Alias for the specific example function
)

from source.기록활용모드 import 기록활용모드


def run_기록제어():
    """
    Implements the functionality of 기록제어.py, providing a menu for
    record management operations.
    """
    print("=" * 50)
    print("Mode: '기록제어' (Record Control)")
    print("=" * 50)

    func_n = get_caller_name()
    options = [mode.value for mode in 기록활용모드]

    # The ensure_value_completed function is now available from the public API import
    execution_option = ensure_value_completed(
        key_name="execution_option",
        options=options,
        func_n=func_n,
        guide_text='실행옵션을 선택하세요'
    )

    if execution_option == 기록활용모드.일정조회.value:
        일정_조회()
    elif execution_option == 기록활용모드.일정작성.value:
        일정_작성()
    elif execution_option == 기록활용모드.일정작성자동.value:
        일정_작성_자동()
    elif execution_option == 기록활용모드.도구사용.value:
        기록용어_표준화()
    elif execution_option == 기록활용모드.수치비교.value:
        print("\n--- 수치비교 (Numerical Comparison) ---")
        try:
            item_a_name = input("물품 A의 품명 (예: 다이소 지퍼팩): ")
            item_a_count = int(input("물품 A의 개수 (예: 35): "))
            item_a_price = float(input("물품 A의 총가격 (만원 단위, 예: 0.2): "))

            item_b_name = input("물품 B의 품명 (예: a2z 지퍼팩): ")
            item_b_count = int(input("물품 B의 개수 (예: 100): "))
            item_b_price = float(input("물품 B의 총가격 (만원 단위, 예: 1.4350): "))

            result = 물품_가격비교({'품명': item_a_name, '개수': item_a_count, '총가격': item_a_price},
                             {'품명': item_b_name, '개수': item_b_count, '총가격': item_b_price})
            print(result)
        except (ValueError, TypeError) as e:
            print(f"입력 오류: {e}. 숫자를 정확히 입력해주세요.")

    elif execution_option == 기록활용모드.기록용템플릿출력.value:
        기록용템플릿_출력()
    elif execution_option == 기록활용모드.년간일정생성.value:
        년간일정생성_4분기단위()
    elif execution_option == 기록활용모드.물품가격비교.value:
        물품가격비교_func()
    else:
        print(f"'{execution_option}'은(는) 유효하지 않은 옵션입니다.")


def run_휴비츠업무관리():
    """
    Loads all functions from the '휴비츠업무관리' module and presents them
    to the user for selection and execution.
    """
    func_n = get_caller_name()

    print("=" * 50)
    print("Mode: '휴비츠업무관리' (Huvitz Work Management)")
    print("=" * 50)

    huvitz_functions = [
        name for name, func in inspect.getmembers(휴비츠업무관리, inspect.isfunction)
        if not name.startswith('_') and inspect.getmodule(func) == 휴비츠업무관리
    ]

    if not huvitz_functions:
        print("No functions found in '휴비츠업무관리.py'.")
        return

    selected_function_name = ensure_value_completed(
        key_name="Huvitz Function",
        options=huvitz_functions,
        func_n=func_n
    )

    selected_function = getattr(휴비츠업무관리, selected_function_name)
    print(f"\n--- Running '{selected_function_name}' ---\n")
    selected_function()
    print(f"\n--- Finished '{selected_function_name}' ---\n")


if __name__ == "__main__":
    """
        Main entry point of the application.
        Provides a choice between '기록제어' and '휴비츠업무관리'.
        """
    sys.stdout.reconfigure(encoding='utf-8')
    func_n = get_caller_name()
    main_options = ["기록제어 (Record Control)", "휴비츠업무관리 (Huvitz Work Management)", "Exit"]
    main_actions = {
        "기록제어 (Record Control)": run_기록제어,
        "휴비츠업무관리 (Huvitz Work Management)": run_휴비츠업무관리,
        "Exit": lambda: print("Exiting.") or sys.exit(0)
    }

    while True:
        print("\n" + "=" * 50)
        print("Main Menu")
        print("=" * 50)

        main_choice_text = ensure_value_completed(
            key_name="메인 메뉴",
            options=main_options,
            func_n=func_n
        )

        action = main_actions.get(main_choice_text)
        if action:
            action()
        else:
            print("Invalid choice returned by selection mechanism.")
