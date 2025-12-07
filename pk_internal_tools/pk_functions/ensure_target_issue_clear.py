from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_target_issue_clear():
    target_device_issue_code = get_target_issue_code()
    if target_device_issue_code:
        logging.debug(f'''vpc_issue_code={vpc_issue_code} ''')
        save_target_issue_code(vpc_issue_code)
        exec_target_doctor(vpc_issue_code)  # run solution function about solution code
