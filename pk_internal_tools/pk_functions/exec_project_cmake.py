from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def exec_project_cmake(project_pnx, **remote_device_target_config):
    try:

        import traceback
        import sys
        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        ip = remote_device_target_config['ip']
        pw = remote_device_target_config['pw']
        port = remote_device_target_config['port']
        user_n = remote_device_target_config['user_n']
        local_ssh_public_key = remote_device_target_config['local_ssh_public_key']
        local_ssh_private_key = remote_device_target_config['local_ssh_private_key']

        cmd = rf"cd {project_pnx}/build && ./project_cmake"  # build 를 통해서 생성된 project_cmake exec  f 이다
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        ensure_command_to_remote_os_with_pubkey(cmd='sudo apt update', **remote_device_target_config)
        if not len(std_err_list) == 0:
            for std_err_str in std_err_list:
                logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            return
        if not len(std_outs) == 0:
            for std_out_str in std_outs:
                logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')
        logging.debug(rf'''{func_n}()  ''')
    except:
        logging.debug(rf"{traceback.format_exc()}   ")
        raise
