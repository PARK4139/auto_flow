def ensure_pk_project_docker_ran(f, dockerfile_script_list):
    from pk_internal_tools.pk_functions.get_wsl_distro_config import get_wsl_distro_config
    import logging

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_wireless_target
    from pk_internal_tools.pk_functions.ensure_dockerfile_writen import ensure_dockerfile_writen
    from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
    from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
    from pk_internal_tools.pk_functions.ensure_wsl_distro_enabled import ensure_wsl_distro_enabled
    from pk_internal_tools.pk_functions.ensure_wsl_distro_session import ensure_wsl_distro_session
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_objects.pk_directories import D_PK_FASTAPI, d_pk_root
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import os

    # ensure wsl
    wsl_distro_config = get_wsl_distro_config()

    ensure_wsl_distro_enabled(distro_name=wsl_distro_config.distro_name)
    ensure_wsl_distro_session(distro_name=wsl_distro_config.distro_name)

    ip = wsl_distro_config.ip
    port = wsl_distro_config.port
    user_n = wsl_distro_config.user_name

    ensure_ssh_public_key_to_remote_os(**wsl_distro_config)
    ensure_remote_os_as_nopasswd(**wsl_distro_config)
    if QC_MODE:
        logging.debug(f'''{'{PkTexts.TRY_GUIDE}'} ssh -p {port} {user_n}@{ip} ''')

    # make dockerfile
    ensure_pnx_made(pnx=f, mode='f')

    # write dockerfile
    ensure_dockerfile_writen(f=f, f_dockerfile_script_list=dockerfile_script_list)

    # send dockerfile via scp
    ensure_command_to_wireless_target(cmd=f'scp -av --delete -e "ssh -i ~/.ssh/id_ed25519" {d_pk_root} {user_n}@{ip}:~/Downloads/{get_nx(d_pk_root)}', **wsl_distro_config)
    # mkr. # todo

    # send dockerfile via rsync
    # install_ubuntu_pkg_to_remote_os_via_apt(ubuntu_pkg_n='rsync', **remote_device_target_config)
    d_pk_system = get_pnx_wsl_unix_style(pnx=D_PK_FASTAPI)
    # ensure_command_to_remote_os(cmd=f'rsync -av --delete -e "ssh -i ~/.ssh/id_ed25519" {d_project} {user_n}@{ip}:~/Downloads/{get_nx(d_project)}', **remote_device_target_config)
    # ensure_command_to_remote_os(cmd=f'rsync -av --delete {d_project} ~/Downloads/', **remote_device_target_config)

    # import ipdb
    # ipdb.set_trace()
    # while 1:
    #     # todo: 등록된 함수명 조회 with idx
    #     # print_pk_func_list_with_idx()
    #     # if user_cmd = "f 13":
    #     #     ensure_text_saved_to_clipboard(text_working=pk_input())
    #     import ipdb
    #     ipdb.set_trace()
    #     # ctrl v

    # install docker deamon
    # install_ubuntu_pkg_to_remote_os_via_apt(ubuntu_pkg_n='docker', **remote_device_target_config)

    # start docker deamon
    ensure_command_to_wireless_target(cmd=f'sudo service docker start', **wsl_distro_config)

    # edit dockerfile
    # if QC_MODE:
    #     ensure_command_executed(cmd=rf'code "{f}"')

    # build docker
    f_nx = get_nx(f)
    f_n = get_n(f)
    f_docker_img_n = rf'{f_n}'
    f_docker_tag_version = rf''  # 생략 시 latest
    # f_docker_tag_version=rf':1.0'
    f_docker_tag_n = rf'{f_docker_img_n}{f_docker_tag_version}'
    ensure_command_to_wireless_target(cmd=rf"docker build -t {f_docker_tag_n} -f ~/Downloads/{os.path.basename(d_pk_system)}/{f_nx} .",
                             **wsl_distro_config)
    std_out_str, std_err_str = ensure_command_to_wireless_target(cmd=rf"ls ~/Downloads/{os.path.basename(d_pk_system)}/{f_nx}",
                                                        **wsl_distro_config)
    logging.debug(f'''std_out_str={std_out_str} ''')
    raise
    # ensure_command_to_remote_os(cmd=rf"ls", **remote_device_target_config)
    # ensure_command_to_remote_os(cmd=rf"ls ~/Downloads/{os.path.basename(d_pk_system)}/{f_nx}", **remote_device_target_config)
    # ensure_command_to_remote_os(cmd=rf"ls ~/Downloads/{os.path.basename(d_pk_system)}/{f_nx}", **remote_device_target_config)
    # raise
    # ensure_command_to_remote_os(cmd=rf"pwd", **remote_device_target_config)

    # docker run
    f_n = get_n(f)
    docker_container_n = rf'{f_n}'
    cmd_list = [
        f"sudo docker run --rm -d \\",
        f"--name {docker_container_n} {f_docker_img_n} \\",
        # f"-p <로컬_포트>: <컨테이너_포트>\\",
        # f"-v ~/Downloads/mariadb_data:/var/lib/mysql \\",  # 볼륨 마운트
        # f"mariadb \\",  # exec 할 이미지 (선택적)
    ]
    cmd = get_str_from_list(working_list=cmd_list)
    ensure_command_to_remote_os(cmd=cmd, **wsl_distro_config)

    # check docker container
    # ensure_command_executed(cmd=rf"wsl docker ps -a")  # 중지된 컨테이너 포함

    # 이 설정을 완료하면
    # WSL Docker deamon tcp://0.0.0.0:2375에서 외부 요청 수신대기
    config_content = """{
        "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
    }"""
    ensure_command_to_remote_os_with_pubkey(cmd=rf"sudo sh -c 'echo \"{config_content}\" | tee /etc/docker/daemon.json'",
                                 **wsl_distro_config)
    ensure_command_to_remote_os_with_pubkey(cmd=rf"sudo service docker restart", **wsl_distro_config)

    # wsl docker_ip
    std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(
        cmd=f"docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' {docker_container_n}")  # 이거되나?
    # std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=f"docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' {f_docker_container_name}")
    docker_ip = std_outs[0]
    logging.debug(f'''docker_ip="{docker_ip}"  ''')

    # wsl 내부 docker deamon 제어(wsl 외부에서)
    # Docker SDK # TCP로 노출 또는 Unix 소켓
    client = docker.DockerClient(base_url=rf"tcp://{docker_ip}:2375")  # Docker deamon 에 연결 (WSL 외부에서)
    print(client.info())  # Docker 정보 확인

    ensure_pnx_removed(f)

    # send_f(f=f_dockerfile, ip=xc)
