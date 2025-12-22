from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_python_pkg_to_remote_os(py_pkg_n, **remote_device_target_config):
    # 파이썬 모듈 설치기능
    import importlib

    if not is_internet_connected():
        logging.debug(f'''can not install python module for internet not connected  ''')
        raise

    # todo if remote_device_target_config['ip'] == 'localhost' or local private ip or local public ip:
    try:
        return importlib.import_module(py_pkg_n)
    except ModuleNotFoundError:
        logging.debug(f"[WARN ] '{py_pkg_n}' 모듈이 없습니다.")
        yn = input(f">> '{py_pkg_n}'를 설치하시겠습니까? (y/n): ").strip().lower()
        if yn != 'y':
            logging.debug(f"[ABORTED ] '{py_pkg_n}' 설치를 건너뜁니다.")
            return
        try:
            install_py_module(py_pkg_n)
            # todo installed 목록에서 확인 후 green
            logging.debug(f"'{py_pkg_n}' installation")
            return importlib.import_module(py_pkg_n)
        except Exception as e:
            logging.debug(f"'{py_pkg_n}' installation {e}")
            raise
