from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS


def ensure_wsl_sdkmanager(remote_device_target_config):
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_wireless_target

    # _______________________________________________________________________

    # [how] nvidia sdkmanager download.
    # nvidia developer login.
    # click button ".deb Ubuntu" # sdkmanager_2.2.0-12028_amd64.deb downloaded at 250331

    # wsl 에서 수행
    # ensure_general_ubuntu_pkg(ubuntu_pkg_n='sdkmanager', **remote_device_target_config) #
    ensure_command_to_wireless_target(cmd='sudo apt update', **remote_device_target_config)
    ensure_command_to_wireless_target(cmd='sudo apt --fix-broken install', **remote_device_target_config)
    # mv "/mnt/c/AutonomousTODO/Downloads/pk_working/sdkmanager_2.2.0-12028_amd64.deb" "."
    # explorer.exe .
    f_nx = 'sdkmanager_2.2.0-12028_amd64.deb'
    ensure_command_to_wireless_target(cmd='mkdir -p ~/Downloads/pk_working', **remote_device_target_config)
    upload_pnx_to_remote_os(local_pnx_src=f'{D_DOWNLOADS}/pk_working/{f_nx}',
                            remote_pnx_dst=f'~/Downloads/pk_working/{f_nx}', **remote_device_target_config)
    ensure_command_to_wireless_target(cmd=f'sudo dpkg -i ~/Downloads/pk_working/{f_nx}',
                             **remote_device_target_config)  # todo sdkmanager cli 로 업그레이드 시도
