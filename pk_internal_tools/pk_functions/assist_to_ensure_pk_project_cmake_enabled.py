from pk_internal_tools.pk_functions.get_wsl_distro_config import get_wsl_distro_config
from pk_internal_tools.pk_functions.get_wsl_distro_name_installed import get_wsl_distro_name_installed


def assist_to_ensure_project_cmake_executed_at_remote_device_target():
    from pk_internal_tools.pk_functions.build_project_cmake import build_project_cmake
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os_with_pubkey import ensure_command_to_wireless_target_with_pubkey
    from pk_internal_tools.pk_functions.exec_project_cmake import exec_project_cmake
    from pk_internal_tools.pk_objects.pk_directories import D_PK_CMAKE

    import logging

    from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
    from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
    from pk_internal_tools.pk_functions.ensure_wsl_distro_session import ensure_wsl_distro_session
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    wsl_distro_name = get_wsl_distro_name_installed()

    ensure_wsl_distro_session(distro_name=wsl_distro_name)

    wsl_distro_config = get_wsl_distro_config()

    ensure_ssh_public_key_to_remote_os(**wsl_distro_config)
    ensure_remote_os_as_nopasswd(**wsl_distro_config)

    project_pnx = D_PK_CMAKE
    try:
        std_outs, std_err_list = ensure_command_to_wireless_target_with_pubkey(cmd=rf"sudo apt update", **wsl_distro_config)
        std_outs, std_err_list = ensure_command_to_wireless_target_with_pubkey(cmd=rf"echo y | sudo apt install build-essential", **wsl_distro_config)
        std_outs, std_err_list = ensure_command_to_wireless_target_with_pubkey(cmd=rf"echo y | sudo apt install libyaml-cpp-dev", **wsl_distro_config)
    except:
        logging.debug(f'''{'{PkTexts.TRY_GUIDE}'} ssh -p {wsl_distro_config.port} {wsl_distro_config.user_name}@{wsl_distro_config.ip} ''')

    build_project_cmake(project_pnx=project_pnx, **wsl_distro_config)
    exec_project_cmake(project_pnx=project_pnx, **wsl_distro_config)
