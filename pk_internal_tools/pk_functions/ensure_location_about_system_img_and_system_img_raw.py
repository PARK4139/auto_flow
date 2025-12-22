from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_location_about_system_img_and_system_img_raw(remote_device_target_config):
    # ~/Downloads/flash/xc_flash/Linux_for_Tegra/bootloader/ 안에 system.img* 이 있으면 정상.
    dst = '~/Downloads/flash/xc_flash/Linux_for_Tegra/bootloader/'
    cmd = rf'sudo find {dst} -type f -name "system.img*"'
    std_out, std_err = ensure_command_to_remote_os(cmd=cmd, **remote_device_target_config)
    std_list = std_out.split('\n')
    if not check_signature_in_loop(time_limit=10, working_list=std_list, signature="/bootloader/system.img",
                                   signature_found_ment=rf'system.img found in {dst}'):
        logging.debug(rf'''system.img* not found in the expected path ({dst}).  ''',
                 print_color='yellow')
        raise  # todo raise 보다는 ipdb 로 대체하여 에러가 난 위치에서 수동으로 재시도 해볼 수 있도록 하는게 나을것 같다. ipdb 가 함수 호출부에서 이루어져도록 수정필요할 수도 있다.
