from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging


def reboot_vpc(**remote_device_target_config):
    import inspect
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000

    import logging

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_wireless_target
    from pk_internal_tools.pk_functions.get_wsl_distro_port import get_wsl_distro_port
    from pk_internal_tools.pk_functions.ensure_dockerfile_writen import ensure_dockerfile_writen
    from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
    from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
    from pk_internal_tools.pk_functions.ensure_wsl_distro_enabled import ensure_wsl_distro_enabled
    from pk_internal_tools.pk_functions.ensure_wsl_distro_session import ensure_wsl_distro_session
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_functions.get_wsl_distro_names_installed import get_wsl_distro_names_installed
    from pk_internal_tools.pk_functions.get_wsl_ip import get_wsl_ip
    from pk_internal_tools.pk_functions.get_wsl_pw import get_wsl_pw
    from pk_internal_tools.pk_functions.get_wsl_user_n import get_wsl_user_n
    from pk_internal_tools.pk_objects.pk_directories import D_PK_FASTAPI, d_pk_root, D_USERPROFILE
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import os

    # stdout, stderr = ensure_command_to_remote_os(cmd = "sudo reboot",**remote_device_target_config)
    stdout, stderr = ensure_command_to_wireless_target(cmd="sudo shutdown -r now", **remote_device_target_config)
    ip = remote_device_target_config['ip']
    while 1:
        if not ensure_pinged(ip):
            logging.debug(f'''ping ({ip}) ''')
            return
        ensure_slept(milliseconds=20)
