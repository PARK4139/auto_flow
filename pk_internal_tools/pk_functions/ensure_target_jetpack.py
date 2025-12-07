from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_target_jetpack(**remote_device_target_config):
    # todo

    a, b = ensure_command_to_remote_os(cmd='todo', **remote_device_target_config)
    if 'Ubuntu' not in a:
        logging.debug(f'''ubuntu is not installed({a}) ''')
        raise
