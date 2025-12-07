from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
import logging
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def assist_to_perform_to_ensure_target_condition():
    # todo:  request_template_raw 를 넣고 request 를 만들고 request 대로 셋팅 수행 ...하는 로직 파이프 고민필요

    import inspect
    # lazy import로 순환 import 문제 해결
    try:
        from pk_internal_tools.pk_functions.ensure_get_caller_name import get_caller_name
    except ImportError:
        # fallback: Define a dummy function or raise an error if it's critical
        def get_caller_name():
            raise RuntimeError("get_caller_name could not be imported.")

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if is_os_windows():
        # mkr_assist_to_perform_to_ensure_target_condition
        # todo guide_to_edit_target_config_script_and_update_toml        and        save to target_device_mamnagement_map_toml
        # todo : migrate hardcoding to get_from_toml # 현업에서는 협업을 위해서 필요.
        # 고정값은 migrate to toml and get from toml
        # 가변값은 guide
        f = F_VPC_MAMNAGEMENT_MAP_TOML

        # target_device_data data model orm (OBJECT RELATIONAL MAPPING)
        target_device_data_raw = get_target_data_raw_from_target_request()
        target_device_data = TODOCarDataStructure.RemoteDeviceDataStructure()
        target_device_data.set_remote_device_data_field_all(pk_structure=target_device_data_raw)
        target_device_data.print_remote_device_data_field_all(instance_name='vpc_data_defined')

        wsl_data_raw = get_wsl_data_raw_data(target_device_data_raw)
        wsl_data = TODOCarDataStructure.RemoteDeviceDataStructure()
        wsl_data.set_remote_device_data_field_all(pk_structure=wsl_data_raw)
        wsl_data.print_remote_device_data_field_all(instance_name='wsl_data')
        # [ how ] msi/wsl_ubuntu_24_04_no_flash/login.
        # msi

        ensure_wsl_distro_enabled(wsl_distro_name=wsl_data.target_device_os_distro_name)
        ensure_wsl_distro_session(wsl_distro_name=wsl_data.target_device_os_distro_name)
        ensure_wsl_usb_ip_connection_established(wsl_distro_name=wsl_data.target_device_os_distro_name,
                                                 remote_device_target_config=remote_device_target_config)

        if target_device_data.target_device_ip:
            if QC_MODE:
                logging.debug(f'''vpc_data.ip={target_device_data.target_device_ip} ''')
            remote_device_target_config = {}
            remote_device_target_config['ip'] = target_device_data.target_device_ip
            remote_device_target_config['local_ssh_private_key'] = target_device_data.target_device_local_ssh_private_key
            remote_device_target_config['port'] = target_device_data.target_device_port
            remote_device_target_config['user_n'] = target_device_data.target_device_user_n

            ensure_ssh_public_key_to_remote_os(**remote_device_target_config)
            ensure_remote_os_as_nopasswd(**remote_device_target_config)

        # argument 유효성 검사
        # logging.debug(f'''ooo 과 ooo 이 초기화되지 않아 {target_device_identifier} 장비를 베이직 셋업과 스모크 테스트를 진행할 수 없습니다. ''')
        # logging.debug(f'''ooo TODO 외부차량탑재용으로 {target_device_identifier} 장비를 베이직 셋업과 스모크 테스트를 진행하시겠습니까? ''')
        ensure_iterable_log_as_vertical(item_iterable=remote_device_target_config)
        raise

        ensure_target_ready(wsl_data=wsl_data, target_device_data=target_device_data, **remote_device_target_config)

        assist_to_ensure_target_bit(bit_mode='p')

        assist_to_ensure_target_bit(bit_mode='c')
