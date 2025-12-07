from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical


def print_wired_connection_list(remote_device_target_config, wired_connection_no_range):
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

    import re
    ensure_distro_pkg_installed_to_remote_os(ubuntu_pkg_n='net-tools', **remote_device_target_config)

    for wired_connection_no in wired_connection_no_range:
        stdout_list = []

        # 한 번만 호출하여 전체 정보를 가져오기
        cmd = f"sudo nmcli connection show 'Wired connection {wired_connection_no}'"
        std_outs, std_err_list = ensure_command_to_wireless_target(cmd=cmd, **remote_device_target_config)

        # list to str
        std_out = get_str_from_list(working_list=std_outs)

        # parse
        ipv4_address = re.search(r'ipv4.addresses\s*:\s*([\d\.\/]+)', std_out)  # 수정된 정규식
        ipv4_method = re.search(r'ipv4.method\s*:\s*(\S+)', std_out)
        ipv4_gateway = re.search(r'ipv4.gateway\s*:\s*(\S+)', std_out)
        ipv4_dns = re.search(r'ipv4.dns\s*:\s*(\S+)', std_out)

        # None filter
        not_parsed = "(not parsed)"
        ipv4_address = ipv4_address.group(1) if ipv4_address else not_parsed
        ipv4_method = ipv4_method.group(1) if ipv4_method else not_parsed
        ipv4_gateway = ipv4_gateway.group(1) if ipv4_gateway else not_parsed
        ipv4_dns = ipv4_dns.group(1) if ipv4_dns else not_parsed

        # strip() filter
        ipv4_address = ipv4_address.strip()
        ipv4_method = ipv4_method.strip()
        ipv4_gateway = ipv4_gateway.strip()
        ipv4_dns = ipv4_dns.strip()

        # add to list
        stdout_list.append(f"___________________________________________________________")
        if not_parsed in ipv4_address:
            stdout_list.append(f"{not_parsed}")
        else:
            stdout_list.append(f"ipv4.address: {ipv4_address}")
            stdout_list.append(f"ipv4.method: {ipv4_method}")
            stdout_list.append(f"ipv4.gateway: {ipv4_gateway}")
            stdout_list.append(f"ipv4.dns: {ipv4_dns}")
        stdout_list.append(f"___________________________________________________________")

        # 수직으로 출력
        ensure_iterable_log_as_vertical(item_iterable=stdout_list, item_iterable_n=f"Wired connection {wired_connection_no}")
