from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def build_project_cmake(project_pnx, **remote_device_target_config):
    try:

        import traceback

        import inspect

        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        ip = remote_device_target_config['ip']
        pw = remote_device_target_config['pw']
        port = remote_device_target_config['port']
        user_n = remote_device_target_config['user_n']
        local_ssh_public_key = remote_device_target_config['local_ssh_public_key']
        local_ssh_private_key = remote_device_target_config['local_ssh_private_key']

        cmd = "cmake --version"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        if not len(std_err_list) == 0:
            for std_err_str in std_err_list:
                logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            return
        if not len(std_outs) == 0:
            for std_out_str in std_outs:
                logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')
                prompt_positive = "cmake version "
                if prompt_positive in std_out_str:
                    break

        cmd = rf"rm -rf {project_pnx}/build"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        if not len(std_err_list) == 0:
            for std_err_str in std_err_list:
                logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            return
        if not len(std_outs) == 0:
            for std_out_str in std_outs:
                logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')

        cmd = rf"mkdir -p {project_pnx}/build"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        if not len(std_err_list) == 0 and not len(std_outs) == 0:
            return

        cmd = rf"cd {project_pnx}/build && cmake .."
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        if not len(std_err_list) == 0:
            for std_err_str in std_err_list:
                logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')

            # {PkTexts.TRY_GUIDE} : sudo apt install build-essential cmake g++ make git libyaml-cpp-dev

            # cmd = rf"sudo apt update"
            # std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(ip=ip, port=port, username=username, local_ssh_private_key=local_ssh_private_key, cmd=cmd)
            # if not len(std_err_list) == 0:
            #     for std_err_str in std_err_list:
            #         logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            #     return
            # if not len(std_outs) == 0:
            #     for std_out_str in std_outs:
            #         logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')

            # cmd = rf"sudo apt install build-essential cmake g++ make git libyaml-cpp-dev"
            # std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(ip=ip, port=port, username=username, local_ssh_private_key=local_ssh_private_key, cmd=cmd)
            # if not len(std_err_list) == 0:
            #     for std_err_str in std_err_list:
            #         logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            #     return
            # if not len(std_outs) == 0:
            #     for std_out_str in std_outs:
            #         logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')

            return
        if not len(std_outs) == 0:
            for std_out_str in std_outs:
                logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')

        cmd = rf"cd {project_pnx}/build && make"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        if not len(std_err_list) == 0:
            for std_err_str in std_err_list:
                logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
            return
        if not len(std_outs) == 0:
            for std_out_str in std_outs:
                logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')

        logging.debug(rf'''{func_n}()  ''')
    except Exception as e:
        logging.debug(rf"{traceback.format_exc()}   ")
        raise
