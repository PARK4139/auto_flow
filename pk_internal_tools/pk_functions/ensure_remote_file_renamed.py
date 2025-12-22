from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_remote_file_renamed(remote_f_src, pnx_remote_d_dst, **remote_device_target_config):
    std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"mv {remote_f_src} {pnx_remote_d_dst}", **remote_device_target_config)
    if std_outs == [] or std_err_list == []:
        logging.debug(f'''''')
    else:
        logging.debug(rf'''''')
        raise
