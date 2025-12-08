from pk_internal_tools.pk_functions.ensure_cursor_worked_done import ensure_cursor_worked_done
from pk_internal_tools.pk_functions.ensure_pk_log_error_log_sent_to_cursor import ensure_pk_log_error_log_sent_to_cursor
from pk_internal_tools.pk_functions.ensure_slept_by_following_history import ensure_slept_by_following_history
from pk_internal_tools.pk_functions.ensure_debug_log_seperated import ensure_log_seperated_by_pk_debug_line
from pk_internal_tools.pk_functions.ensure_edited_code_tested import ensure_edited_code_tested


@ensure_log_seperated_by_pk_debug_line
def ensure_draft_scenario_executed(__file__):
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_not_organized import PK_UNDERLINE

    func_n = get_caller_name()
    try:
        ensure_cursor_worked_done()
        ensure_slept_by_following_history(key_name="GUI 렌더링 대기", func_n=func_n)
        ensure_edited_code_tested()
        ensure_pk_log_error_log_sent_to_cursor()
        input("continue:enter")
    except:
        logging.debug(PK_UNDERLINE)
        ensure_debug_loged_verbose(traceback)
        logging.debug(PK_UNDERLINE)
    finally:
        ensure_spoken(wait=True)


def _execute_sample_2025_11_11():
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS
    from pk_internal_tools.pk_objects.pk_files import F_VENV_PYTHON_EXE

    file = Path(D_pk_FUNCTIONS) / "ensure_pk_wrapper_started_minimal.py"
    cmd = get_text_chain(F_VENV_PYTHON_EXE, file)
    ensure_command_executed(cmd)


def _execute_sample_2025_11_10():
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS
    from pk_internal_tools.pk_objects.pk_files import F_VENV_PYTHON_EXE

    file_sample2 = Path(D_pk_FUNCTIONS) / "ensure_pk_wrapper_started.py"
    cmd = get_text_chain(F_VENV_PYTHON_EXE, file_sample2)
    ensure_command_executed(cmd)


@ensure_log_seperated_by_pk_debug_line
def ensure_draft_scenario_smaples_performance_compared(__file__):
    # todo : fix

    from pk_internal_tools.pk_functions.print_samples_ranking import log_samples_ranking

    from pk_internal_tools.pk_functions.analyze_samples_results import analyze_samples_results
    from pk_internal_tools.pk_functions.clear_benchmark_data import clear_benchmark_data
    import logging

    from pk_internal_tools.pk_objects.pk_not_organized import PK_UNDERLINE

    # mode = "cumulative" # pk_option
    mode = "non_cumulative"  # pk_option
    iterations = 10

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
            _execute_sample_2025_11_09()

        for i in range(iterations):
            logging.debug(PK_UNDERLINE)
            logging.debug(f"실행 {i + 1}/{iterations}...")
            _execute_sample2()

        # n. 결과 분석
        logging.debug(PK_UNDERLINE)
        logging.debug("[2단계] 결과 분석")
        analyze_samples_results()
        logging.debug(PK_UNDERLINE)

        # n. 성능 순위
        logging.debug(PK_UNDERLINE)
        logging.debug("[3단계] 성능 순위")
        log_samples_ranking()
        logging.debug(PK_UNDERLINE)

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


def _execute_sample_2025_11_09():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS
    from pk_internal_tools.pk_objects.pk_files import F_VENV_PYTHON_EXE
    # pk_option
    file_sample = D_pk_FUNCTIONS / "ensure_pk_wrapper_started.py"
    cmd = get_text_chain(F_VENV_PYTHON_EXE, file_sample)
    ensure_command_executed(cmd)

    # pk_option
    # ensure_python_file_executed_advanced(file_sample)

    # target_file = d_pk_wrappers  / "pk_ensure_pnx_backed_up.py"
    # ensure_pk_python_file_executed_in_uv_venv_windows(target_file)


def _execute_sample2():
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_restarted_self_as_not_child_process import ensure_python_file_executed_advanced
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS
    file_sample = D_pk_FUNCTIONS / "ensure_pk_wrapper_started.py"
    ensure_python_file_executed_advanced(file_sample)


def _ensure_draft_scenario_executed_ver_pattern(__file__):
    # TODO : fix
    # test flow :
    # without refresh 에서 실행 한 로그에서 특정부분 수집
    # 파싱 elapsed_seconds
    # 통계
    for i in range(10):
        _execute_sample2()

    for i in range(10):
        _execute_sample_2025_11_09()
