from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging
from pathlib import Path



def ensure_target_smoke_test (target_device_data):
    import traceback

    import os

    import inspect
    # IT에서 XC로 docker image전송
    # IT에서 XC로 docker image run 명령
    # IT에서 XC에서 제어PC로 결과 수집

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    target_device_aifw_version = target_device_data.target_device_aifw_version
    target_device_id = target_device_data.target_device_id
    target_device_side_mode = target_device_data.target_device_side
    target_device_type = target_device_data.target_device_type

    # 초기 설정 및 유효성 검사

    remote_device_target_config = {}
    remote_device_target_config['ip'] = get_ip_available_by_user_input()
    remote_device_target_config['pw'] = target_device_data.target_device_pw
    remote_device_target_config['port'] = target_device_data.target_device_port
    remote_device_target_config['user_n'] = target_device_data.target_device_user_n
    remote_device_target_config['local_ssh_public_key'] = os.path.join(D_USERPROFILE, ".ssh", "id_ed25519.pub")

    ensure_ssh_public_key_to_remote_os(**remote_device_target_config)

    # 임시 _d_ 설정
    d_temp = make_and_get_d_temp()

    check_manual_task_iteractively(
        question=rf'''did you verify lan6 connected and indicator is dimming ?  ''')
    if not ensure_target_ip (target_device_data, **remote_device_target_config):
        ip = get_ip_available_by_user_input()

    # input(f"{get_colorful_text_working_with_stamp_enviromnet(func_n=func_n)} >")  # [SUGGEST] sleep() 하는게 어떤가?

    ensure_auto_reboot_test()

    try:
        # set_remote_os_as_nopasswd_v1(**remote_device_target_config)
        ensure_remote_os_as_nopasswd(**remote_device_target_config)

        # remove f remote (vpc_info_collector.sh)
        f_nx = 'vpc_info_collector.sh'
        std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"rm -rf ~/Downloads/{f_nx}", **remote_device_target_config)
        if std_outs == [] or std_err_list == []:
            logging.debug(f'''''')
        else:
            logging.debug(rf'''''')
            raise

        # send f (vpc_info_collector.sh)
        f_nx = 'vpc_info_collector.sh'
        f_local = os.path.join(D_PK_VSTEST, f_nx)
        f_remote = os.path.join('/home/nvidia/Downloads', f_nx)
        upload_pnx_to_remote_os(local_pnx_src=f_local, remote_pnx_dst=f_remote, **remote_device_target_config)

        # chmod +x (vpc_info_collector.sh)
        cmd = rf"chmod +x {f_remote}"
        std_outs, std_err_list = ensure_command_to_remote_os(cmd=cmd, **remote_device_target_config)
        if std_outs != [] or std_err_list != []:
            return

        # run f (vpc_info_collector.sh)
        cmd = rf"cd {get_p(f_remote)} && {f_remote}"
        # cmd = rf"{remote_f}"
        std_outs, std_err_list = ensure_command_to_remote_os(cmd=cmd, **remote_device_target_config)
        if std_outs == [] or std_err_list == []:
            logging.debug(f'''''')
        else:
            logging.debug(rf'''''')
            return

        target_device_id = target_device_id.strip()
        yymmdd = get_yymmdd()

        # download f (vpc_info_collector.txt)
        f_remote_src = "/home/nvidia/Downloads/vpc_info_collector.txt"
        f_local_new = rf"{D_PK_VSTEST}/{vpc_id}_smoke_test_report_at_{yymmdd}.txt"
        download_pnx_from_remote_os(f_remote_src, f_local_new, **remote_device_target_config)

        # check f_local_dst
        f_local_new = Path(f_local_new)
        if f_local_new.exists():
            ensure_command_executed(cmd=f'explorer "{f_local_new}" ', mode='a')

        # convert from lf to crlf # todo for not working
        f_n = get_n(f_nx)
        f_x = get_x(f_nx)
        f_to = rf"{D_PK_VSTEST}/{f_n}_crlf{f_x}"
        f_to = get_pnx_windows_style(f_to)
        convert_lf_to_crlf(f_from=f_local_new, f_to=f_to)

        # convert from binary to txt
        # f_from = f_to
        # f_to = rf"{PROJECT_DIRECTORY}/{f_n}_binary{f_x}"
        # convert_binary_to_text(binary_f=f_from, txt_f=f_to)

        # rename target_device_info_collector.txt
        f_remote_src = "/home/nvidia/Downloads/vpc_info_collector.txt"
        f_remote_new = f'/home/nvidia/Downloads/{vpc_id}_smoke_test_report_at_{yymmdd}.txt'
        std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"mv {f_remote_src} {f_remote_new}", **remote_device_target_config)
        if std_outs == [] or std_err_list == []:
            logging.debug(f'''''')
        else:
            logging.debug(rf'''''')
            return

        # remove target_device_info_collector.sh
        std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"rm -rf ~/Downloads/vpc_info_collector.sh",
                                                      **remote_device_target_config)
        if std_outs == [] or std_err_list == []:
            logging.debug(f'''''')
        else:
            logging.debug(rf'''''')
            return

        # compare target_device tree
        target_device_aifw_version = target_device_aifw_version.replace('.', "_")
        f_target_ref_tree2 = rf"{D_PK_VSTEST}\{get_n(f_to)}_tree_{yymmdd}.toml"
        f_target_tree_answer = rf"{D_PK_VSTEST}/{vpc_type}_{vpc_aifw_version}_tree_{vpc_side_mode}_ref.toml"
        save_target_tree_to_f_toml(f=f_target_ref_tree2, remote_device_target_config=remote_device_target_config)
        ignore_list = [
            "/home/nvidia/.local",
            # "/home/nvidia/.compiz",
            "/home/nvidia/.cache",
            "/home/nvidia/works/log",
            "/home/nvidia/works/TODO_remote_target_launcher/log",
            "/home/nvidia/.ssh/known_hosts",
            "/home/nvidia/.config",
        ]
        compare_target_tree(f_target_tree_answer_list=f_target_tree_answer, f_target_ref_tree2_list=f_target_ref_tree2,
                         ignore_list=ignore_list)

        ensure_pnx_removed(d_temp)

        import ipdb
        ipdb.set_trace()

        print_wired_connection_list(wired_connection_no_range=range(1, 5), **remote_device_target_config)

        reset_wired_connection_list(wired_connection_no_range=range(1, 5), **remote_device_target_config)

        # set target_device ip
        ensure_target_ip (target_device_data, **remote_device_target_config)

        # input(f"{get_colorful_text_working_with_stamp_enviromnet(func_n=func_n)} >")

        # set target_device ip as custom
        wired_connection_3_new = {'wired_connection_no': 3, "address": rf"", "method": "auto", "gateway": "",
                                  "dns": ""}  # reset target_device ip
        wired_connection_3_new = {'wired_connection_no': 3, "address": rf"192.168.2.124/22", "method": "manual",
                                  "gateway": "192.168.1.1", "dns": "8.8.8.8"}
        wired_connection_3_new = {'wired_connection_no': 3, "address": rf"192.168.2.114/22", "method": "manual",
                                  "gateway": "192.168.1.1", "dns": "8.8.8.8"}
        wired_connection_3_new = {'wired_connection_no': 3, "address": rf"192.168.10.114/22", "method": "manual",
                                  "gateway": "", "dns": ""}
        set_wired_connection(wired_connection_3_new, **remote_device_target_config)

        # if xc
        # TODO_component_f, TODO_component_m %CPU 확인
        # 카메라 미연결 시, TODO_component_f, %CPU=100~110
        ensure_command_to_remote_os(cmd=f"top", **remote_device_target_config)

        # cmd = f"sudo dmesg"
        ensure_command_to_remote_os(cmd=f"sudo dmesg -w", **remote_device_target_config)

        ensure_command_to_remote_os(cmd=f"timedatectl", **remote_device_target_config)

        # 로거 설정확인
        ensure_command_to_remote_os(cmd=f"cat ./autorun.sh", **remote_device_target_config)

        # 로거 테스트
        # TODO_remote_target_launcher.zip
        std_outs, std_err_list = ensure_command_to_remote_os(
            cmd=f"cd ~/works/TODO_wavier_launcher && sudo python3 SystemLogger.py", **remote_device_target_config)
        if std_outs == [] or std_err_list == []:
            logging.debug(f'''''')
        else:
            logging.debug(rf'''''')
            return

        # 로그 확인
        # find /home/nvidia/works/log/ -ctime +4 -delete

        # 로그 수집

        # 강제전원remove 후 재부팅 시 AI_Framework 동작여부 확인 테스트
        check_manual_task_iteractively(question=rf'''remove power of XC, forcely ? ''')
        check_manual_task_iteractively(question=rf'''connect power of XC, again ? ''')
        check_manual_task_iteractively(
            question=rf'''AI frame work is restarted, again ? ''')

    except Exception as e:
        logging.debug(rf"{traceback.format_exc()}   ")
        return
    finally:
        ensure_pnx_removed(d_temp)
