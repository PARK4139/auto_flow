from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_target_issue_code(vpc_issue_code=None):
    if not target_device_issue_code:
        logging.debug(f'''등록된 모든 테스트를 진행합니다. ''')
    else:
        logging.debug(f'''vpc_issue_code 에 대한 특정 테스트를 진행했습니다. ''')
