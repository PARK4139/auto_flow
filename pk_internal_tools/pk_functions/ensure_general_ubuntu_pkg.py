from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

def ensure_general_ubuntu_pkg(ubuntu_pkg_n, **remote_device_target_config):
    logging.debug(f"Attempting to install {ubuntu_pkg_n} in remote OS...")

    tm = PkRemoteTargetEngine(identifier=PkDevice.undefined, setup_op=PkModesForDemo.REMOTE_TARGET)
    std_outs, std_err_list = tm.ensure_command_to_remote_target_with_pubkey(
        cmd=f'sudo apt install -y {ubuntu_pkg_n}',
        **remote_device_target_config
    )

    logging.debug(f"--- STDOUT for apt install {ubuntu_pkg_n} ---")
    if std_outs:
        for line in std_outs:
            logging.debug(rf'{line}')
    else:
        logging.debug("(empty STDOUT)")
    
    logging.debug(f"--- STDERR for apt install {ubuntu_pkg_n} ---")
    if std_err_list:
        for line in std_err_list:
            logging.debug(rf'{line}')
    else:
        logging.debug("(empty STDERR)")
    
    # Verify installation
    logging.debug(f"Verifying {ubuntu_pkg_n} installation...")
    verify_outs, verify_errs = ensure_command_to_remote_target_with_pubkey(
        cmd=f'which {ubuntu_pkg_n}',
        **remote_device_target_config
    )

    logging.debug(f"--- STDOUT for which {ubuntu_pkg_n} ---")
    if verify_outs:
        for line in verify_outs:
            logging.debug(rf'{line}')
    else:
        logging.debug("(empty STDOUT)")

    logging.debug(f"--- STDERR for which {ubuntu_pkg_n} ---")
    if verify_errs:
        for line in verify_errs:
            logging.debug(rf'{line}')
    else:
        logging.debug("(empty STDERR)")
