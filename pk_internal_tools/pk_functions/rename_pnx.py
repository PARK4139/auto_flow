
from pk_internal_tools.pk_functions.is_f import is_f

import logging



def rename_pnx(src, pnx_new):
    import os
    import time
    import traceback

    # 이름을 변경하는 경우에 재귀적으로 바뀌어야 하는 것으로 생각되어 os.renames 를 테스트 후 적용하였다.
    # os.rename 사용 중에 d  인 경우는 재귀적으로 변경이 안된다
    try:
        if not Path(src).exists():
            logging.debug(f'''rename 할 f이 없습니다 {src}''')
            return

        if src == pnx_new:
            logging.debug(f'''현재f명 과 바꾸려는f명 이 같아 rename 하지 않았습니다 src={src} pnx_new={pnx_new}''')
            return

        if Path(pnx_new).exists():
            logging.debug(f'''dst에 중복된 f이 있습니다. {pnx_new}" ''')
            return

        if is_f(src):
            type_name = "f"
        else:
            type_name = "d"

        os.renames(src, pnx_new)
        time_limit = 3
        waiting_limit = 20
        time_s = time.time()
        while 1:
            if Path(pnx_new).exists():
                logging.debug(f'''rename {type_name} from {src} to {pnx_new}''')
                break
            else:
                time_e = time.time()
                time_diff = time_e - time_s
                if time_diff == time_limit:
                    return 0
                ensure_slept(milliseconds=waiting_limit)
    except Exception as e:
        logging.debug(rf'''traceback.format_exc()="{traceback.format_exc()}" rename 확인필요 src={src} pnx_new={pnx_new}  ''')
