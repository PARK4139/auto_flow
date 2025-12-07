from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
import logging


def log_success_to_f(FEATURE_NICK_NAME, FEATURE_ID, FEATURE_REMOVAL_ID, f):
    import os

    try:
        working_list = []
        if not os.path.exists(f):
            with open(file=f, mode='w', encoding=PkEncoding.UTF8.value) as f_obj:
                f_obj.write("")  # 빈 f 생성

        with open(file=f, mode='r', encoding=PkEncoding.UTF8.value) as f_obj:
            working_list = f_obj.readlines()

        # 리스트 정리: 공백 remove 및 중복 remove
        # working_list = list(set([item.strip() for item in working_list]))

        hashed_stamp_success = rf'#{"[ SUCCEEDED ]"}'
        for item in working_list:
            if hashed_stamp_success in item:
                working_list.remove(item)
                logging.debug(f"{FEATURE_ID} removed from working_list.")

        working_list.append(f"{hashed_stamp_success} {FEATURE_ID:30s} {FEATURE_NICK_NAME} ")

        # 리스트 저장 (정렬 필요 시 주석 해제)
        # working_list = sorted(working_list)

        with open(file=f, mode='w', encoding=PkEncoding.UTF8.value) as f:
            f.write("\n".join(working_list) + "\n")

    except:
        import traceback
        DESCRIPTION = f"log {FEATURE_ID} \n {traceback.format_exc()}"
        logging.debug(f"{DESCRIPTION}  ")
