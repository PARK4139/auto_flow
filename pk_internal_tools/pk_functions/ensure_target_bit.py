from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def assist_to_ensure_target_bit(bit_mode):
    # 개요 : target_device 트래킹 시스템, 이슈발생 target_device 이슈트래킹시스템 필요.
    # BIT # Built in Test
    # P BIT # non-continuous : pilot or maintenance
    # C BIT # continuous     : os
    # 프로그램 대기능 정의 : target_device 테스트/이슈레포팅/해결 자동시스템
    # 프로그램명 : oo.py
    # 프로그램 설치위치 : vpc/도커/oo.py or IT/도커/oo.py
    # 개발순서 : P BIT > C BIT

    if not QC_MODE:
        if not is_internet_connected():
            logging.debug(f'''{PkTexts.INTERNET_CONNECTION_REQUIRED} {PkTexts.VPC_BIT_PROGRESS}. ''')

    # ensure ping to acu_it # [acu_it] from toml

    # ensure ping to target_device side a # [vpc side a] from toml

    # ensure ping to target_device side b # [vpc side b] from toml

    state_c_bit_activated = 1
    if bit_mode == "p":
        state_c_bit_activated = 0
    if bit_mode == "c":
        state_c_bit_activated = 1
    while 1:
        logging.debug(f'''bit_mode={bit_mode} ''')
        if ensure_target_issue_clear():
            pass
        if state_c_bit_activated == 0:
            break
        ensure_slept(milliseconds=1000)
