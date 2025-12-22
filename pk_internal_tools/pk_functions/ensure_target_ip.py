from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_target_ip (target_device_data, **remote_device_target_config):
    target_device_ip = target_device_data.target_device_ip
    target_device_side_mode = target_device_data.target_device_side
    target_device_type = target_device_data.target_device_type
    target_device_identifier = target_device_data.device_identifier
    ip_new = target_device_data.target_device_ip
    while 1:
        set_target_ip (target_device_data, **remote_device_target_config)
        if not ensure_pinged(ip_new):
            logging.debug(rf'''{vpc_type} set as {vpc_side_mode} side ''')
            raise
        else:
            break
