from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_target_type_conected_via_scp (target_device_data_raw):
    # todo : jetson_setup identify.py 참고
    # todo : processer name    core cnt    로 target_device 특징을 판단

    return 'no'

    remote_device_target_config = {}
    remote_device_target_config['ip'] = target_device_data_raw.target_device_ip
    remote_device_target_config['port'] = target_device_data_raw.target_device_port
    remote_device_target_config['user_n'] = target_device_data_raw.target_device_user_n
    remote_device_target_config['local_ssh_private_key'] = target_device_data_raw.target_device_local_ssh_private_key

    target_device_type = None
    target_device_ip = remote_device_target_config['ip']

    target_device_core_cnt_of_evm = 8
    target_device_core_cnt_of_xc = 8
    target_device_core_cnt_of_nx = 8
    target_device_core_cnt_of_no = 8
    target_device_processser_name_of_evm = 'todo'
    target_device_processser_name_of_xc = 'todo'
    target_device_processser_name_of_nx = 'todo'
    target_device_processser_name_of_no = 'todo'
    # target_device_current_upper_limit =
    # target_device_power_upper_limit =
    # target_device_cpu_clock_upper_limit =

    target_device_identifier_and_target_nvidia_serial_map_dict = get_target_identifier_and_target_nvidia_serial_map()
    for target_device_nvidia_serial, target_device_identifier in target_device_identifier_and_target_nvidia_serial_map_dict.items():
        if target_device_nvidia_serial != target_device_data_raw.target_device_nvidia_serial:
            continue
        elif target_device_nvidia_serial == target_device_data_raw.target_device_nvidia_serial:
            target_device_type = target_device_nvidia_serial.split(f"{PK_BLANK}#")[0]
            return target_device_type
        else:
            logging.debug(rf'''unkown exception.  ''')
            raise

    target_device_core_cnt = target_device_data_raw.target_device_core_cnt
    processer_name_of_remote_os = target_device_data_raw.target_device_proceser_name
    if target_device_core_cnt == target_device_core_cnt_of_no and processer_name_of_remote_os == target_device_processser_name_of_no:
        target_device_type = 'no'
    elif target_device_core_cnt == target_device_core_cnt_of_nx and processer_name_of_remote_os == target_device_processser_name_of_nx:
        target_device_type = 'nx'
    elif target_device_core_cnt == target_device_core_cnt_of_xc and processer_name_of_remote_os == target_device_processser_name_of_xc:
        target_device_type = 'xc'
    elif target_device_core_cnt == target_device_core_cnt_of_evm and processer_name_of_remote_os == target_device_processser_name_of_evm:
        target_device_type = 'evm'
    else:
        logging.debug(rf'''unkown target_device_type (vpc_ip={vpc_ip}, target_device_core_cnt={vpc_core_cnt}, processer_name_of_remote_os={processer_name_of_remote_os} ).  ''')
        raise
    return target_device_type.lower()
