from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE


def ensure_scenario_as_cmd_exe_kill_v1_v2_performance_comparison_test_ran():
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE, F_PK_ENSURE_TEST_SCENARIO_EXECUTED_PY
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    import logging
    import logging

    from pk_internal_tools.pk_functions.ensure_dummy_100_windows_made import ensure_dummy_100_windows_made
    from pk_internal_tools.pk_functions.print_samples_ranking import _log_benchmark_ranking

    import sys

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    from pk_internal_tools.pk_functions.analyze_samples_results import _analyze_benchmark_result
    from pk_internal_tools.pk_functions.clear_benchmark_data import clear_benchmark_data
    from pk_internal_tools.pk_functions.ensure_cmd_exe_killed import ensure_cmd_exe_killed_v1, ensure_cmd_exe_killed_v2
    from pk_internal_tools.pk_functions.export_benchmark_data import export_benchmark_data
    from pk_internal_tools.pk_functions.get_test_scenario_result_filename import get_test_scenario_result_filename
    from pk_internal_tools.pk_functions.ensure_powershell_environment_detected import ensure_powershell_environment_detected
    from pk_internal_tools.pk_functions.ensure_terminal_info_retrieved import ensure_terminal_info_retrieved

    logging.debug(PK_UNDERLINE)
    logging.debug("현재 터미널 환경을 확인 중...")
    logging.debug("현재 환경:", ensure_terminal_info_retrieved())
    logging.debug(PK_UNDERLINE)

    if not ensure_powershell_environment_detected():
        logging.debug("️PowerShell 환경이 아닙니다")
        logging.debug("")
        logging.debug("")
        logging.debug(f"{PkTexts.WARNING}")
        logging.debug("cmd.exe 등에서 실행하면 cmd.exe를 닫는 함수 때문에")
        logging.debug("  자기 자신도 닫히는 문제가 발생할 수 있습니다!")
        logging.debug("")
        logging.debug("실행 튜토리얼 :")
        logging.debug("1. PowerShell을 관리자 권한으로 실행")
        logging.debug("2. 다음 명령어 실행(절대경로):")
        logging.debug(f"{get_text_chain(F_UV_PYTHON_EXE, F_PK_ENSURE_TEST_SCENARIO_EXECUTED_PY, wrapping_string="")}")
        logging.debug("")
        logging.debug("")
        logging.debug("PowerShell 환경에서 실행을 권장합니다. 종료합니다.")
        sys.exit(0)

    # PowerShell 환경인 경우에만 실행
    logging.debug("PowerShell 환경이 확인되었습니다!")
    logging.debug(PK_UNDERLINE)
    logging.debug("PowerShell 환경에서 테스트 시나리오를 실행합니다!")
    logging.debug(PK_UNDERLINE)

    # 실행 전 최종 확인
    logging.debug("테스트를 시작하시겠습니까? (y/N): ")
    try:
        confirm = input().strip().lower()
        if confirm not in ['y', 'yes', '예']:
            logging.debug("테스트가 취소되었습니다.")
            sys.exit(0)
    except KeyboardInterrupt:
        logging.debug("사용자에 의해 중단되었습니다.")
        sys.exit(0)

    # mode = "cumulative" # pk_option
    mode = "non_cumulative"  # pk_option
    iterations = 3

    logging.debug(PK_UNDERLINE)
    logging.debug("함수 성능 테스트 및 벤치마크")
    logging.debug("이 프로그램은 다양한 함수들의 성능을 간단하게 측정하고 비교합니다.")

    try:
        if mode == "cumulative":
            logging.debug("[모드] Cumulative 모드로 실행합니다. 기존 데이터를 보존합니다.")
        else:
            logging.debug("[모드] Non-cumulative 모드로 실행합니다. 기존 데이터를 초기화하고 새로 시작합니다.")
            clear_benchmark_data()

        logging.debug(f"[자동] {mode} 모드로 모든 테스트를 순차적으로 실행합니다...")
        logging.debug(PK_UNDERLINE)

        # n. 성능 테스트 실행
        logging.debug(PK_UNDERLINE)
        logging.debug("[1단계] 성능 테스트 실행 (10회)")
        logging.debug(f"[테스트] 성능 테스트 실행 ({iterations}회)")
        logging.debug(PK_UNDERLINE)

        for i in range(iterations):
            logging.debug(PK_UNDERLINE)
            logging.debug(f"실행 {i + 1}/{iterations}...")
            # 테스트 환경 재현
            ensure_dummy_100_windows_made()
            ensure_slept(milliseconds=200)
            ensure_cmd_exe_killed_v1()

        for i in range(iterations):
            logging.debug(PK_UNDERLINE)
            logging.debug(f"실행 {i + 1}/{iterations}...")
            # 테스트 환경 재현
            ensure_dummy_100_windows_made()
            ensure_slept(milliseconds=200)
            ensure_cmd_exe_killed_v2()
            logging.debug(PK_UNDERLINE)

        # n. 결과 분석
        logging.debug(PK_UNDERLINE)
        logging.debug("[2단계] 결과 분석")
        _analyze_benchmark_result()
        logging.debug(PK_UNDERLINE)

        # n. 성능 순위
        logging.debug(PK_UNDERLINE)
        logging.debug("[3단계] 성능 순위")
        _log_benchmark_ranking()
        logging.debug(PK_UNDERLINE)

        # n. 리포트 생성 (d_pk_logs 디렉토리에 동적 파일명으로 저장)
        # logging.debug(PK_UNDERLINE)
        # logging.debug("[4단계] 리포트 생성")
        # result_filename = get_test_scenario_result_filename("foo", mode)
        # result_path = d_pk_logs / result_filename
        # report_path = export_benchmark_data(str(result_path))
        # logging.debug(f"[완료] {mode} 모드 리포트가 생성되었습니다: {result_filename}")
        # logging.debug(f"[경로] 저장 위치: {result_path.absolute()}")
        # logging.debug(PK_UNDERLINE)

        # 모드별 추가 정보
        if mode == "non_cumulative":
            logging.info(f"Non-cumulative 모드: 이번 테스트에서 생성된 샘플만 포함 (기존 데이터 무시)")
        else:
            logging.info(f"Cumulative 모드: 전체 누적 샘플 포함 (트렌드 분석 가능)")

        logging.debug("모든 테스트가 성공적으로 완료되었습니다!")

    except KeyboardInterrupt:
        logging.error("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.error("테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
