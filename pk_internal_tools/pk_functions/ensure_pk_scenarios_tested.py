import io
import logging
import os
import sys

import pytest

from pk_internal_tools.pk_functions.ensure_debug_log_seperated import ensure_log_seperated_by_pk_debug_line
from pk_tests.test_testcases_of_get_pk_interesting_info import test_testcases_of_get_pk_interesting_info
from pk_tests.test_pk_wifi_util import test_pk_wifi_util


def ensure_pk_scenarios_tested():
    """Discovers and runs all automated tests in the pk_tests directory using pytest."""
    # lazy import
    from pk_internal_tools.pk_objects.pk_directories import d_pk_tests
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG

    logging.debug("Starting automated test execution with pytest...")

    # Set FORCE_COLOR environment variable to force colored output
    os.environ['FORCE_COLOR'] = '1'

    pytest_args = [str(d_pk_tests), "-v", "-s", "--ignore=pk_tests/TODO", "--color=yes"]

    # --- First run: For console output with colors ---
    logging.debug("Running pytest for console output...")
    try:
        result_code_console = pytest.main(pytest_args)
    finally:
        # Unset FORCE_COLOR environment variable
        del os.environ['FORCE_COLOR']

    # --- Second run: For capturing output to log file ---
    logging.debug("Running pytest for log file capture...")
    # Re-set FORCE_COLOR for the second run if needed, though it might not affect captured output
    os.environ['FORCE_COLOR'] = '1'  # Ensure it's set for the second run too

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    sys.stderr = redirected_output

    try:
        result_code_log = pytest.main(pytest_args)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        del os.environ['FORCE_COLOR']  # Unset after second run

    pytest_output = redirected_output.getvalue()

    with open(F_PK_LOG, "w", encoding="utf-8") as f:
        f.write(pytest_output)

    logging.debug(f"Automated test execution finished. Pytest results saved to {F_PK_LOG}.")
    # Return the result code from the console run, as that's what the user sees
    return result_code_console


@ensure_log_seperated_by_pk_debug_line
def test_function_benchmark_via_pk_benchmarker(__file__):
    # todo : fix

    from pk_internal_tools.pk_functions.print_samples_ranking import _log_benchmark_ranking

    from pk_internal_tools.pk_functions.analyze_samples_results import _analyze_benchmark_result
    from pk_internal_tools.pk_functions.clear_benchmark_data import clear_benchmark_data
    import logging

    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

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

        # 모드별 추가 정보
        if mode == "non_cumulative":
            logging.debug(f"Non-cumulative 모드: 이번 테스트에서 생성된 샘플만 포함 (기존 데이터 무시)")
        else:
            logging.debug(f"Cumulative 모드: 전체 누적 샘플 포함 (트렌드 분석 가능)")

        logging.debug(PK_UNDERLINE)

        # n. 성능 테스트 실행
        logging.debug(PK_UNDERLINE)
        logging.debug(f"# 성능 테스트 실행")
        logging.debug(f"{iterations}회")

        for i in range(iterations):
            logging.debug(PK_UNDERLINE)
            logging.debug(f"실행 {i + 1}/{iterations}...")
            test_testcases_of_get_pk_interesting_info()

        for i in range(iterations):
            logging.debug(PK_UNDERLINE)
            logging.debug(f"실행 {i + 1}/{iterations}...")
            test_pk_wifi_util()

        # n. 결과 분석
        logging.debug(PK_UNDERLINE)
        logging.debug("# 결과 분석")
        _analyze_benchmark_result()

        # n. 성능 순위
        logging.debug(PK_UNDERLINE)
        logging.debug("# 성능 순위")
        _log_benchmark_ranking()
        logging.debug(PK_UNDERLINE)


        logging.debug("모든 테스트가 성공적으로 완료되었습니다!")

    except KeyboardInterrupt:
        logging.error("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.error("테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()


def ensure_pk_scenario_executed_ver_pattern(__file__):
    # TODO : fix
    # test flow :
    # without refresh 에서 실행 한 로그에서 특정부분 수집
    # 파싱 elapsed_seconds
    # 통계

    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_restarted_self_as_not_child_process import ensure_python_file_executed_advanced
    from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS

    for i in range(10):
        file_sample = D_PK_FUNCTIONS / "ensure_pk_wrapper_starter_executed.py"
        ensure_python_file_executed_advanced(file_sample)

    for i in range(10):
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
        from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS
        from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE
        # pk_option
        file_sample = D_PK_FUNCTIONS / "ensure_pk_wrapper_starter_executed.py"
        cmd = get_text_chain(F_UV_PYTHON_EXE, file_sample)
        ensure_command_executed(cmd)

        # pk_option
        # ensure_python_file_executed_advanced(file_sample)

        # target_file = d_pk_wrappers  / "pk_ensure_pnx_backed_up.py"
        # ensure_pk_python_file_executed_in_uv_venv_windows(target_file)
