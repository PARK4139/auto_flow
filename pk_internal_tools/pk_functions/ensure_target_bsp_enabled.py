import zlib

import webbrowser
import traceback
import toml
from zipfile import BadZipFile
from selenium.common.exceptions import ElementClickInterceptedException
from pynput import mouse
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from os import path
from functools import lru_cache
from fastapi import HTTPException
from datetime import date
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_target_bsp_enabled (target_device_data, remote_device_target_config):
    if 'no' in target_device_data.device_identifier:
        #  \\TODO_AINas_2\30_VISION_DEV\ACU_NO\90_received\20250325 ACU_NO 최종 제출 자료 2차\몹티콘-ACUNO 최종결과물\몹티콘-ACUNO 최종결과물\5.SW 자료\01.BSP\BSP_250312.tar.bz2
        if not is_module_flashed_by_mtc():
            # mtc 모듈은 flash 되어 들어와서 bsp flash 이미지를 tar
            # LINUX_for_Tegra 의 상위 폴더 에서 sudo 붙여서 BSP 압축해제 # 꽤 걸림
            ensure_command_to_remote_os("cd ~/working_directory_for_flash", remote_device_target_config)
            # ensure_command_to_remote_os("sudo tar -xvf BSP20240305.tar", remote_device_target_config)  # BSP20240305.tar 는 초기버전.
            ensure_command_to_remote_os("sudo tar -jxvf Flash_Image_Release_1.3.0.tar.bz2 ",
                             remote_device_target_config)  # TODO 40 nas/30_VISION_DEV/ACU_NX/20_flash/의 최신디렉토리의 파일을 받아야함.
            # tar 인 경우: -j remove->-xvf
        pass
    elif 'nx' in target_device_data.device_identifier:
        pass
    elif 'xc' in target_device_data.device_identifier:
        pass
    elif 'evm' in target_device_data.device_identifier:
        # Driver Package (BSP) DOWNLOAD
        # sudo mv "/mnt/c/Users/wjdgns/Downloads/Jetson_LINUX_R32.7.5_aarch64.tbz2" /Downloads/flash/EVM_flash/
        # sudo tar -jxvf /Downloads/flash/EVM_flash/Jetson_LINUX_R32.7.5_aarch64.tbz2 #압축해제
        # sudo find -type f -name "Jetson_LINUX_R32.7.5_aarch64.tbz2"

        # ensure existance JETSON_LINUX_R32.7.5_AARCH64.TBZ2
        #    explorer https://developer.nvidia.com/jetpack-sdk-465  # jetpack 4.6.5 Driver for Jetson AGX Xavier
        #    sudo mv /mnt/c/Users/wjdgns/Downloads/Tegra_LINUX_Sample-Root-Filesystem_R32.7.5_aarch64.tbz2 /Downloads/flash/EVM_flash/LINUX_for_Tegra/rootfs

        # ensure tar
        # sudo tar -jxvf /Downloads/flash/EVM_flash/LINUX_for_Tegra/rootfs/Tegra_LINUX_Sample-Root-Filesystem_R32.7.5_aarch64.tbz2 #압축해제
        # sudo find -type f -name "Tegra_LINUX_Sample-Root-Filesystem_R32.7.5_aarch64.tbz2"
        pass
    else:
        logging.debug(f'''unknown target_device_data.identifier ({target_device_data.device_identifier}) ''',
                      print_color='yellow')
        raise
