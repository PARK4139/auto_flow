import logging

from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.is_d import is_d


def classify_pnx_by_special_keyword(d_src, special_keyword, with_walking):
    import os
    import string

    d_src = d_src.strip()
    d_src = d_src.replace("\"", "")
    d_src = d_src.replace("\'", "")
    logging.debug(f'''d_src={d_src} special_keyword={special_keyword}''')
    connected_drives = []
    for drive_letter in string.ascii_uppercase:
        drive_path = drive_letter + ":\\"
        if os.path.exists(drive_path):
            connected_drives.append(drive_path)
            if d_src == drive_path:
                logging.debug(rf'''광범위진행제한 ''')
                return

    if not os.path.exists(d_src):
        logging.debug(rf"입력된 d_src 가 존재하지 않습니다 d_src={d_src}")
        return

    if d_src == "":
        logging.debug(f'''d_src == "" ''')
        return

    special_dirs_promised = [
        # "blahblahblah_boom_boom_boom",
    ]
    # previous_keyword=get_text_from_clipboard()
    # if previous_keyword == pnx:
    #     previous_keyword=""

    special_keyword = special_keyword.strip()
    if special_keyword == "":
        logging.debug("special_keyword 는 ""일 수 없습니다.")
        return
    if "\n" in special_keyword:
        f_list = special_keyword.split("\n")
    else:
        f_list = [special_keyword]
    file_nxs = [get_nx(f) for f in f_list]
    logging.debug(f'''len(f_list)={len(f_list)} ''')
    logging.debug(f'''file_nxs={file_nxs}  ''')
    for special_keyword in f_list:
        special_keyword = special_keyword.strip()
        if special_keyword != "":
            special_dirs_promised.append(special_keyword)
        for special_pnx in special_dirs_promised:
            ensure_pnx_made(rf"{D_PK_WORKING_EXTERNAL}\{special_pnx}", mode="d")
        pnxs_searched = []
        if is_d(d_src):
            if with_walking == True:
                for root, d_nx_list, file_nxs in os.walk(d_src, topdown=False):  # os.walk()는 with walking 으로 동작한다
                    for f_nx in file_nxs:
                        f = os.path.join(root, f_nx)
                        for special_keyword in special_dirs_promised:
                            if special_keyword in os.path.basename(f):
                                pnxs_searched.append(f)
            else:
                # todo : without_waling
                return

        logging.debug(rf'''len(pnxs_searched)="{len(pnxs_searched)}"  ''')  # 검색된 f 개수
        dst = None
        for index, special_dir in enumerate(special_dirs_promised):
            dst = rf"{D_PK_WORKING_EXTERNAL}\{special_dirs_promised[index]}"
            for pnx_searched in pnxs_searched:
                if special_dir in os.path.basename(pnx_searched):
                    ensure_pnx_moved(pnx=pnx_searched, d_dst=dst)
        special_dirs_promised = []
        logging.debug(rf'''dst="{dst}"  ''')
