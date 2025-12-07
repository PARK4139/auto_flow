

def ensure_target_ubuntu_pkg_enabled (target_device_data, remote_device_target_config):
    # todo 1개씩 나눠서 설치 후 설치여부 재확인    # wsl 환경에 설치
    ensure_command_to_remote_os(cmd='sudo apt install -y libxml2-utils', **remote_device_target_config)
    ensure_command_to_remote_os(cmd='sudo apt install -y simg2img', **remote_device_target_config)  # 설치 실패
    # Package simg2img is not available, but is referred to by another package.
    # This may mean that the package is missing, has been obsoleted, or
    # is only available from another source
    # However the following packages replace it:
    #   android-sdk-libsparse-utils
    #
    # E: Package 'simg2img' has no installation candidate
    ensure_command_to_remote_os(cmd='sudo apt install -y abootimg liblz4-tool binutils', **remote_device_target_config)
    if 'no' in target_device_data.device_identifier:
        pass
    if 'nx' in target_device_data.device_identifier:
        pass
