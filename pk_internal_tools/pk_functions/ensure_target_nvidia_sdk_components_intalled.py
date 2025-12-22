from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_target_nvidia_sdk_components_intalled (target_device_data):
    if target_device_data.target_device_with_flash_image == 0:
        # jetpack sdk component install 창 자동시현
        if 'no' in target_device_data.device_identifier:
            ensure_command_to_remote_os("sdkmanager --archived-versions")  # wsl 에서 수행
            pass
        elif 'nx' in target_device_data.device_identifier:
            pass
        elif 'xc' in target_device_data.device_identifier:
            pass
        elif 'evm' in target_device_data.device_identifier:
            # sdkmanager
            # show all versions
            # JETPACK 4.6.5
            # Download now. install Later 미체크  #체크 시 플래시imageCREATE 안함 #다음에는 체크해보자 불필요하게 size이 늘거 같은 생각이 든다. 왜냐면 초창기 img  f 은 회사에서는 필요없기 때문
            # APT repository access for Debian package installation(host). 에러발생
            # Skip Check
            # nvidia/nvidia/Flash
            # installation failed
            # retry # reflash
            # #팀Laptop 4.6.5 로 flash 해도 4.6.6 이 INSTALLATION_가 됨.
            pass
        else:
            logging.debug(f'''unknown target_device_data.identifier ({target_device_data.device_identifier}) ''',
                          print_color='yellow')
            raise
    elif target_device_data.target_device_with_flash_image == 1:
        pass
