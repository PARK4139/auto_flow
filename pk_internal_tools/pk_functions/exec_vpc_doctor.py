from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def exec_target_doctor(vpc_issue_code):
    # todo 3 번 재시도 후, loop out,   logging.debug(f'''solution_code를 3번 해결하려고 했으나  issue_code를 해결할 수 없었습니다. ''')
    solution_code = None
    while 1:
        report_target_issue_discovered()
        if target_device_issue_code:
            solution_code = get_solution_code_from_map_issue_and_solution_code()
            if solution_code:
                solve_issue(solution_code)
                target_device_issue_code = get_target_issue_code(vpc_issue_code)
                if not target_device_issue_code:
                    logging.debug(f'''issue_code is solved ''')
                    remove_issue_code()
                    break
            elif not solution_code:
                logging.debug(f'''solution_code is not found ''')
            continue
    report_target_test_report(vpc_issue_code, solution_code)
