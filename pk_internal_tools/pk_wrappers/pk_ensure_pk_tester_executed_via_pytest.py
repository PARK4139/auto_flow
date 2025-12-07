import subprocess
import sys

import logging
from pk_internal_tools.pk_functions.get_list_contained_element import get_list_contained_element
from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
from pk_internal_tools.pk_functions.get_str_from_list import get_str_from_list
from pk_internal_tools.pk_objects.pk_directories import d_pk_tests


def _run_pytest_file(path: str):
    cmd_list = ""
    # verbose_mode = True
    verbose_mode = False
    verbose_option = '-s'
    if verbose_mode:
        cmd_list = [sys.executable, "-m", "pytest", verbose_option, path]
    else:
        cmd_list = ["pytest", path]
    cmd = get_str_from_list(working_list=cmd_list, item_connector=" ")
    logging.debug(f"[RUNNING] {cmd}")
    result = subprocess.run(cmd_list)
    if result.returncode != 0:
        logging.debug(f"[FAIL] 테스트 실패: {path}")
    else:
        logging.debug(f"[PASS] 테스트 성공: {path}")


if __name__ == "__main__":
    test_files = get_pnxs_from_d_working(d_working=d_pk_tests)
    test_suffix = 2025
    test_files_filtered = get_list_contained_element(working_list=test_files, suffix=f"_{test_suffix}")

    logging.debug(f"[STARTED] TEST files of {d_pk_tests}")

    tested_file_cnt = 0
    for file in test_files_filtered:
        logging.debug(f"[DETECTED] {file}")
        _run_pytest_file(file)
        tested_file_cnt += 1

    skipped_file_cnt = len(test_files) - tested_file_cnt

    logging.debug(f"[ENDED] TEST VIA PYTEST {tested_file_cnt}EA files of {d_pk_tests} (skipped {skipped_file_cnt} files of len({len(test_files)})")
