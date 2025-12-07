from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def check_latest_aifw_version_and_get_version_seleted(target_device_identifier, aifw_version):
    return aifw_version  # code for temp

    target_device_identifier = target_device_identifier.strip()
    target_device_identifier = target_device_identifier.lower()
    if 'no' in target_device_identifier:
        # todo gitlab 에서 latest 파싱하도록 후 target_device_aifw_version 와 비교, 같으면 진행, 다르면 질의(latest 는 몇입니다. 업데이트 할까요?)
        pass
    elif 'nx' in target_device_identifier:
        pass
    elif 'xc' in target_device_identifier:
        pass
    elif 'evm' in target_device_identifier:
        pass
    else:
        logging.debug(f'''unknown target_device_identifier ({target_device_identifier}) ''')
        raise
    if QC_MODE:
        logging.debug(f'''aifw_version={aifw_version} ''')
    return aifw_version
