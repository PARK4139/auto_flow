import logging


def ensure_wsl_ip_printed(wsl_distro_name):
    from pk_internal_tools.pk_functions.get_wsl_ip import get_wsl_ip
    wsl_ip = get_wsl_ip(wsl_distro_name="Ubuntu-24.04")
    logging.debug(rf'wsl_ip={wsl_ip}')
