import logging
import re
import subprocess
import sys
import traceback
from pathlib import Path

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_scenarios_tested import ensure_pk_scenarios_tested, ensure_pk_scenario_executed_ver_pattern, test_function_benchmark_via_pk_benchmarker
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_values_completed_2025_12_04 import ensure_values_completed_2025_12_04
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_TEST

# Ensure the test environment is set up
ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)


# --- Fzf Custom Binding for Select All (ALT+A) ---
# This requires modifying get_value_from_fzf_routine or get_fzf_command to add the binding.
# For now, we assume ensure_values_completed can somehow support it or we'll add it there.

def get_test_files() -> list[Path]:
    """Scans the pk_tests directory for test files."""
    test_dir = D_TEST  # AssuD_TESTis correctly defined
    if not test_dir.is_dir():
        logging.error(f"테스트 디렉토리를 찾을 수 없습니다: {test_dir}")
        return []

    test_files = [f for f in test_dir.iterdir() if f.is_file() and f.name.startswith('test_') and f.suffix == '.py']
    return sorted(test_files)


def run_single_test_file(test_file: Path) -> dict:
    """Runs a single unittest file and captures its results."""
    logging.info(f"테스트 실행 중: {test_file.name}")
    command = [
        sys.executable,  # Use the current Python interpreter
        '-m', 'unittest',
        str(test_file)
    ]

    process = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

    result = {
        'file': test_file.name,
        'stdout': process.stdout,
        'stderr': process.stderr,
        'returncode': process.returncode,
        'tests': []  # To store individual test results
    }

    # Parse unittest output for results
    for line in process.stdout.splitlines():
        # Example: ok (pk_tester.TestRunner.test_example_passing)
        # Example: FAIL: test_example_failing (pk_tester.TestRunner.test_example_failing)
        # Example: ERROR: test_example_error (pk_tester.TestRunner.test_example_error)

        match = re.match(r'^(ok|FAIL|ERROR):?\s*(\S+)\s*\((.+)\)', line)
        if match:
            status = match.group(1)
            test_name = match.group(2)
            full_test_path = match.group(3)  # e.g., pk_tester.TestRunner.test_example_passing

            # Extract just the function name (e.g., test_example_passing)
            function_name_match = re.search(r'\b(test_\w+)\b', test_name)
            function_name = function_name_match.group(0) if function_name_match else test_name

            result['tests'].append({
                'status': status,
                'function_name': function_name,
                'full_test_path': full_test_path,
                'raw_line': line
            })

    # If no specific test results parsed, but returncode is 0, assume pass.
    # If returncode is not 0, and no specific test results parsed, assume general failure.
    if not result['tests'] and result['returncode'] == 0:
        result['tests'].append({'status': 'ok', 'function_name': 'UNKNOWN', 'full_test_path': 'UNKNOWN', 'raw_line': 'No detailed output, assumed OK'})
    elif not result['tests'] and result['returncode'] != 0:
        result['tests'].append({'status': 'FAIL', 'function_name': 'UNKNOWN', 'full_test_path': 'UNKNOWN', 'raw_line': 'No detailed output, assumed FAIL'})

    return result


def display_results_table(all_results: list[dict], view_mode: str):
    console = Console()
    table = Table(
        box=box.ROUNDED,
        title=Text("Test Results Summary", style="white bold"),
        header_style="white",
        row_styles=["none", "dim"]
    )

    if view_mode == "simple":
        table.add_column("File", style="white", no_wrap=True)
        table.add_column("Test Function", style="white", no_wrap=True)
        table.add_column("Status", style="bold", justify="center")
    else:  # detailed
        table.add_column("File", style="white", no_wrap=True)
        table.add_column("Test Function", style="white", no_wrap=True)
        table.add_column("Status", style="bold", justify="center")
        table.add_column("Full Path", style="dim white")
        table.add_column("Raw Output", style="dim white")

    for file_result in all_results:
        file_name = file_result['file']
        for test_case in file_result['tests']:
            status = test_case['status']
            function_name = test_case['function_name']

            status_text = ""
            if status == "ok":
                status_text = Text("PASS", style="green")
            elif status == "FAIL":
                status_text = Text("FAIL", style="red")
            elif status == "ERROR":
                status_text = Text("ERROR", style="red")
            else:
                status_text = Text(status, style="yellow")  # Unknown status

            if view_mode == "simple":
                table.add_row(
                    file_name,
                    function_name,
                    status_text
                )
            else:  # detailed
                table.add_row(
                    file_name,
                    function_name,
                    status_text,
                    test_case['full_test_path'],
                    test_case['raw_line']
                )
    console.print(table)


if __name__ == '__main__':
    try:
        func_n = get_caller_name()

        # --- 1. Select Test Files ---
        test_files = get_test_files()
        if not test_files:
            logging.info("실행할 테스트 파일을 찾을 수 없습니다.")
            sys.exit(0)

        file_options = [str(f.relative_to(D_TEST)) for f in test_files]

        # Custom binding for select all (ALT+A) would be added in get_value_from_fzf_routine
        # For now, ensure_values_completed needs to support it or it's a future enhancement.
        selected_file_names = ensure_values_completed_2025_12_04(
            key_name="select_test_files",
            func_n=func_n,
            options=file_options,
            guide_text="테스트할 파일을 다중 선택하세요 (ALT+A로 전체 선택 가능):",
            multi_select=True
        )

        if not selected_file_names:
            logging.info("선택된 테스트 파일이 없습니다. 종료합니다.")
            sys.exit(0)

        selected_paths = [D_TEST / name for name in selected_file_names]

        # --- 2. Select View Mode ---
        view_mode_options = ["simple", "detailed"]
        selected_view_mode = ensure_value_completed(
            key_name="select_view_mode",
            func_n=func_n,
            options=view_mode_options,
            guide_text="테스트 결과 출력 방식을 선택하세요:",
        )
        if not selected_view_mode:
            selected_view_mode = "simple"  # Default to simple view

        # --- 3. Run Tests and Collect Results ---
        all_test_results = []
        for test_file_path in selected_paths:
            if not test_file_path.exists():
                logging.warning(f"선택된 파일이 존재하지 않습니다: {test_file_path.name}")
                continue
            all_test_results.append(run_single_test_file(test_file_path))

        # --- 4. Display Results ---
        if all_test_results:
            display_results_table(all_test_results, selected_view_mode)
        else:
            logging.info("실행된 테스트가 없습니다.")


        # pk_test_options
        ensure_pk_scenarios_tested()
        test_function_benchmark_via_pk_benchmarker(__file__)
        ensure_pk_scenario_executed_ver_pattern(__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
