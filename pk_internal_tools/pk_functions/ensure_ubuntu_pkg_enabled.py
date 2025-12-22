from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_pnx_ubuntu_pkg_enabled import get_pnx_ubuntu_pkg_enabled

import logging


def ensure_ubuntu_pkg_enabled(ubuntu_pkg_n):
    import shutil

    while 1:
        ubuntu_pkg_bin = shutil.which(ubuntu_pkg_n)
        if not ubuntu_pkg_bin:
            logging.debug(f"{ubuntu_pkg_n} is not installed")
            logging.debug(f"try to install {ubuntu_pkg_n} now")
            ensure_command_executed(f"sudo apt install -y {ubuntu_pkg_n}")
            ubuntu_pkg_bin = get_pnx_ubuntu_pkg_enabled(ubuntu_pkg_n)
            if ubuntu_pkg_bin is None:
                continue
        else:
            logging.debug(f"{ubuntu_pkg_n} is installed")
            break
