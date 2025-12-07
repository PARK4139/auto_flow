from pk_internal_tools.pk_functions.get_target_core_cnt_via_scp import get_target_core_cnt_via_scp
from pk_internal_tools.pk_functions.get_target_nvidia_serial_via_scp import get_target_nvidia_serial_via_scp
from pk_internal_tools.pk_functions.get_target_processer_name_via_scp import get_target_processer_name_via_scp


def get_target_data_raw_from_target_request():
    import os
    from pk_internal_tools.pk_functions.check_latest_jetpack_version_and_get_version_seleted import check_latest_jetpack_version_and_get_version_seleted
    from pk_internal_tools.pk_functions.get_pk_token import get_pk_token
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden, D_HOME
    from pk_internal_tools.pk_objects.pk_tbd_car_structure import TODOCarDataStructure
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000

    target_device_data_raw = TODOCarDataStructure.RemoteDeviceDataStructure()

    # no
    # request_template = {}
    # request_template['target_device_type'] = 'no'
    # request_template['target_device_purpose'] = 'TODO_vehicle(undefined purpose)'  # 'TODO_vehicle(undefined purpose)', 'TODO_vehicle(For Internal TODO Development)'
    # request_template['target_device_aifw_version'] = '2.2.4.0'
    # request_template['target_device_jetpack_version'] = '5.1.2'
    # request_template['target_device_jetson_setup_ver'] = '2.0.1'
    # request_template['target_device_side'] = 'a'
    # request_template['target_device_aifw_packing_mode'] = 1  # 1 : TODO 납품차량용   , 0 : TODO 내부테스트용
    # request_template['target_device_flash_image_version'] = '1.0.0'
    # if request_template['target_device_flash_image_version'] == '':
    #     request_template['target_device_with_flash_image'] = 0  # 0 : flash image 없음
    # else:
    #     request_template['target_device_with_flash_image'] = 1  # 1 : flash image 있음
    # request_template['target_device_identifier_number'] = f'00'
    # request_template['target_device_identifier'] = f'{request_template['target_device_type']} #{request_template['target_device_identifier_number']}'

    request_template = {}
    request_template['target_device_type'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_type']=",
                                                                    options=['xc', 'nx', 'no'])
    request_template['target_device_purpose'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_purpose']=",
                                                                       options=['TODO_vehicle(undefined purpose)',
                                                                               'TODO_vehicle(undefined purpose)',
                                                                               'TODO_vehicle(For Internal TODO Development)'])
    request_template['target_device_aifw_version'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_aifw_version']=",
                                                                            options=['1.2.1', '2.2.4.1', '2.2.4.1'])
    request_template['target_device_jetpack_version'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_jetpack_version']=",
                                                                               options=['4.6.5', '5.0.2', '5.1.2'])
    request_template['target_device_jetson_setup_ver'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_jetson_setup_ver']=",
                                                                                options=['', '2.0.1', '2.0.1'])
    request_template['target_device_side'] = ensure_value_completed_2025_10_12_0000(key_name="request_template['target_device_side']", options=['a', 'b'])
    request_template['target_device_aifw_packing_mode'] = ensure_value_completed_2025_10_12_0000(
        key_name="request_template['target_device_aifw_packing_mode']", options=['1: TODO 납품차량용 ', '0: TODO 내부테스트용'])
    request_template['target_device_flash_image_version'] = ensure_value_completed_2025_10_12_0000(
        key_name="request_template['target_device_flash_image_version']", options=['1.0.0', '1.3.0', '1.0.0'])
    if request_template['target_device_flash_image_version'] == '':
        request_template['target_device_with_flash_image'] = '0'  # 0 : flash image 없음
    else:
        request_template['target_device_with_flash_image'] = '1'  # 1 : flash image 있음
    request_template['target_device_identifier_number'] = ensure_value_completed_2025_10_12_0000(
        key_name="request_template['target_device_identifier_number']=",
        options=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                '17', '18', '19', '20'])
    request_template['target_device_identifier'] = f'{request_template['target_device_type']} #{request_template['target_device_identifier_number']}'

    target_device_data_raw.target_device_local_ssh_public_key = os.path.join(D_HOME, ".ssh", "id_ed25519.pub")
    target_device_data_raw.target_device_local_ssh_private_key = os.path.expanduser("~/.ssh/id_ed25519")
    # target_device_ip_ = get_pk_token(f_token=rf'{d_pk_root_hidden}/pk_token_ip_target_side_{target_device_data_raw.target_device_side}.toml', initial_str="")
    # target_device_data_raw.target_device_ip = get_ip_available_by_user_input()
    # if request_template['target_device_side'] == 'a':
    #     target_device_data_raw.target_device_ip = get_pk_token(f_token=rf'{d_pk_root_hidden}/pk_token_ip_target_a_side.toml', initial_str="")
    # elif request_template['target_device_side'] == 'b':
    #     target_device_data_raw.target_device_ip = get_pk_token(f_token=rf'{d_pk_root_hidden}/pk_token_ip_target_b_side.toml', initial_str="")
    # else:
    #     raise
    target_device_data_raw.target_device_ip = None
    from pk_internal_tools.pk_objects.pk_directories import d_pk_tokens
    target_device_data_raw.target_device_port = get_pk_token(f_token=d_pk_tokens / 'pk_token_ssh_port_target_device.toml', initial_str="")
    target_device_data_raw.target_device_user_n = get_pk_token(f_token=d_pk_tokens / 'pk_token_user_n_target_device.toml', initial_str="")
    target_device_data_raw.target_device_pw = get_pk_token(f_token=d_pk_tokens / 'pk_token_pw_target_device.toml', initial_str="")
    target_device_data_raw.target_device_purpose = request_template['target_device_purpose']
    target_device_data_raw.target_device_available_test_ip_set = ('192.168.2.114', '192.168.2.124', '192.168.10.114',
                                                                 target_device_data_raw.target_device_ip)  # ensure ip 할때, target_device_dev_available_ip_list 에서 연결 가능한 것을 우선순위를 두고 자동선택하도록, pickle 써보자.
    target_device_data_raw.target_device_side = request_template['target_device_side']
    target_device_data_raw.target_device_aifw_packing_mode = request_template['target_device_aifw_packing_mode']
    target_device_data_raw.target_device_with_flash_image = request_template['target_device_with_flash_image']
    target_device_data_raw.target_device_flash_image_version = request_template['target_device_flash_image_version']
    # target_device_data_raw.target_device_aifw_version = check_latest_aifw_version_and_get_version_seleted (target_device_data_raw.target_device_identifier, aifw_version=request_template['target_device_aifw_version'])
    target_device_data_raw.target_device_aifw_version = request_template['target_device_aifw_version']
    target_device_data_raw.target_device_type = request_template['target_device_type']
    target_device_data_raw.target_device_identifier_number = request_template['target_device_identifier_number']
    target_device_data_raw.target_device_jetpack_version = check_latest_jetpack_version_and_get_version_seleted(target_device_data_raw.target_device_identifier,
                                                                                                               jetpack_version=
                                                                                                               request_template[
                                                                                                                   'target_device_jetpack_version'])
    target_device_data_raw.target_device_wired_connection_reset = {'wired_connection_no': '(not defined)', "address": rf"",
                                                                  "method": "auto", "gateway": "", "dns": ""}
    target_device_data_raw.target_device_wired_connection_1_new = {'wired_connection_no': 1, "address": rf"{target_device_data_raw.target_device_ip}/24",
                                                                  "method": "manual", "gateway": "", "dns": ""}
    target_device_data_raw.target_device_wired_connection_3_new = {'wired_connection_no': 3, "address": rf"{target_device_data_raw.target_device_ip}/24",
                                                                  "method": "manual", "gateway": "", "dns": ""}
    target_device_data_raw.target_device_core_cnt = get_target_core_cnt_via_scp(target_device_data_raw)
    target_device_data_raw.target_device_proceser_name = get_target_processer_name_via_scp(target_device_data_raw)
    target_device_data_raw.target_device_nvidia_serial = get_target_nvidia_serial_via_scp(target_device_data_raw)
    # target_device_data_raw.target_device_type = get_target_type_conected_via_scp (target_device_data_raw)
    # target_device_data_raw.target_device_identifier = get_target_identifier_matched_from_target_db (target_device_data_raw.target_device_nvidia_serial, target_device_data_raw.target_device_side)
    target_device_data_raw.target_device_identifier = request_template['target_device_identifier']
    return target_device_data_raw
