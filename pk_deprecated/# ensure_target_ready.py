import numpy as np
import ipdb
import datetime
import clipboard
from PySide6.QtWidgets import QApplication
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from moviepy import VideoFileClip
from datetime import timedelta

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_target_ready (target_device_data, wsl_data, **remote_device_target_config):
    if not QC_MODE:
        ensure_hardware_right (target_device_data)

    wsl_distro_name = wsl_data.target_device_os_distro_name
    target_device_type = target_device_data.target_device_type
    with_flash_image = target_device_data.target_device_with_flash_image

    ensure_wsl_flash_directory_flashable (target_device_data)
    ensure_wsl_sdkmanager(remote_device_target_config)

    ensure_target_ubuntu_pkg_enabled (target_device_data, remote_device_target_config)
    ensure_target_bsp_enabled (target_device_data, remote_device_target_config)
    ensure_target_recovery_mode_entered (target_device_data, wsl_data, remote_device_target_config)

    ensure_wired_target_flashed (target_device_data, remote_device_target_config)

    ensure_target_network_eh0_connected()  # 114

    ensure_target_nvidia_sdk_components_intalled (target_device_data)

    ensure_target_smoke_test (target_device_data)

    ensure_target_flash_image_saved()

    save_target_tracking_map_with_nvidia_serial_to_target_mamnagement_map_toml (target_device_data)

    ensure_target_report_about_target_basic_setup()

    ensure_target_os_poweroff()
