from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_dip_switch_position_right (target_device_data):
    target_device_identifier = target_device_data.device_identifier
    if 'no' in target_device_identifier:
        locate_dip_switchitch_on_board_to_left_down()
    elif 'nx' in target_device_identifier:
        pass
    elif 'xc' in target_device_identifier:
        pass
    elif 'evm' in target_device_identifier:
        pass
    else:
        logging.debug(f'''unknown target_device_identifier ({target_device_identifier}) ''')
        raise
