


def build_aifw (target_device_data, remote_device_target_config):
    from pk_internal_tools.pk_functions.todo import todo
    if target_device_data.target_device_type == 'no':
        # 도커 컨테이너 내부의 특정경로에서 build 해야함, 도커내부에 명령어를 수행해야함. ensure_command_to_remote_os 로 docker container 제어 가능한지 확인이 필요.
        d_packing_mode = target_device_data.target_device_aifw_packing_mode
        aifw_branch_n = target_device_data.target_device_aifw_branch_n  # 이 거 build 에서만 필요한 거 같은데
        if d_packing_mode == 1:
            # TODO내부개발용 # without packing mode
            # cd ~/Workspace/ai_framwork/build
            # cmake .. -DPACKING=1     # DPACKING = 0 이면  PACKING ? 확인필요
            todo('%%%FOO%%%')
        elif d_packing_mode == 0:
            # TODO외부차량탑재용 # with packing mode
            todo('%%%FOO%%%')
    elif target_device_data.target_device_type == 'nx':
        # cd ~/works/ai_framework/build
        # cmake --version
        # sudo apt-get install cmake
        # wget https://cmake.org/files/v3.16/cmake-3.16.3.tar.gz
        # tar -xvf cmake-3.16.3.tar.gz
        # cmake ..
        # make -j8  # 8 은 코어의 수 참조
        todo('%%%FOO%%%')
    elif target_device_data.target_device_type == 'xc':
        # build ai_framework
        # vscode/Remote Explorer/SSH/192.168.2.114/~/works/ai_framework/build
        # vscode/Remote Explorer/SSH/192.168.2.114/~/works/ai_framework/build make -j8
        todo('%%%FOO%%%')
