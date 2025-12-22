from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def ensure_wsl_distro_install(distro_name):
    std_list = ensure_command_executed(cmd=f'wsl --install -d {distro_name}')

