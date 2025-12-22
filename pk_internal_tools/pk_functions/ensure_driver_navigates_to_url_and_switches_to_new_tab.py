from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_str_url_decoded import get_str_url_decoded
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

def ensure_driver_navigates_to_url_and_switches_to_new_tab(url, driver, seconds_s=2222, seconds_e=4333):
    import random

    # driver.get(url_decoded)
    url_decoded = get_str_url_decoded(url)
    if url_decoded.startswith(("http://", "https://")):
        logging.debug(f'''url_decoded={url_decoded}  ''')
        driver.get(url_decoded)
    else:
        logging.debug(f"WEIRED URL url_decoded={url_decoded}")
    ensure_slept(milliseconds=random.randint(a=seconds_s, b=seconds_e))  # 정적웹소스 다운로드 대기
    # focus 를 새탭으로 이동
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
