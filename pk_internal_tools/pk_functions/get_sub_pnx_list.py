import webbrowser
import tomllib
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux


def get_sub_pnx_list(pnx, txt_to_exclude_list=None, with_walking=True):
    import os
    txt_to_exclude_list = txt_to_exclude_list or []
    if with_walking == 1:
        d_list = []
        f_list = []
        # 모든 하위 검색
        for root, d_nx_list, file_nxs in os.walk(pnx):
            for d_nx in d_nx_list:
                item_pnx = os.path.join(root, d_nx)
                if is_d(item_pnx):
                    for txt_to_exclude in txt_to_exclude_list:
                        if txt_to_exclude in item_pnx:
                            break  # d에 제외할 문자열이 있으면 추가하지 않음
                    else:
                        d_list.append([item_pnx, os.path.getmtime(item_pnx)])

            for f_nx in file_nxs:
                item_pnx = os.path.join(root, f_nx)
                for txt_to_exclude in txt_to_exclude_list:
                    if txt_to_exclude in item_pnx:
                        break  # f 경로에 제외할 문자열이 있으면 추가하지 않음
                else:
                    f_list.append([item_pnx, os.path.getmtime(item_pnx)])
        return d_list, f_list
    elif with_walking == 0:
        import os

        d_list = []
        f_list = []

        # 현재 d만 순회
        for item in os.listdir(pnx):
            item_pnx = os.path.join(pnx, item)
            # d인 경우
            if is_d(item_pnx):
                for txt_to_exclude in txt_to_exclude_list:
                    if txt_to_exclude in item_pnx:
                        break  # d에 제외할 문자열이 있으면 추가하지 않음
                else:
                    d_list.append([item_pnx, os.path.getmtime(item_pnx)])

            # f인 경우
            if is_f(item_pnx):
                for txt_to_exclude in txt_to_exclude_list:
                    if txt_to_exclude in item_pnx:
                        break  # f 경로에 제외할 문자열이 있으면 추가하지 않음
                else:
                    # f 경로에 제외할 문자열이 없다면 f_list에 추가
                    # logging.debug(rf'''item_pnx       ="{item_pnx}"  ''')
                    # logging.debug(rf'''txt_to_exclude="{txt_to_exclude}"  ''')
                    f_list.append([item_pnx, os.path.getmtime(item_pnx)])

        # print_list_as_vertical(texts=d_list, list_name='d_list')
        # print_list_as_vertical(texts=f_list, list_name='f_list')

        return d_list, f_list
