from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
import logging


def get_ip_wsl_another_way():
    wsl_ip = None
    std_list = ensure_command_executed("wsl ip -4 addr show eth0")
    signature_str = 'inet '
    for std_str in std_list:
        if signature_str in std_str:
            wsl_ip = std_str.split('/')[0].split(signature_str)[1]
            if QC_MODE:
                logging.debug(rf'''wsl_ip="{wsl_ip}" ''')
    return wsl_ip
