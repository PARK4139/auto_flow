from tkinter import UNDERLINE

from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
import logging


def save_all_drive_pnxs_to_txt_f():  # 이 함수는 Everything.exe 를 대체할 f탐색기 용도로 만들었으나 거의 필요 없을 것 같다. 관심d만 확인하는 것으로 충분해 보인다.
    """모든 f d에 대한 정보를 텍스트 f로 저장하는 함수"""
    import os

    # 윈도우냐 아니야에 따라
    # os.system('chcp 65001 >nul')
    # os.system('export LANG=en_US.UTF-8 >nul')

    opening_d = os.getcwd()
    proper_tree_txt = rf"{D_PK_ROOT}\pkg_all_tree\proper_tree.txt"
    all_tree_txt = rf"{D_PK_ROOT}\pkg_all_tree\all_tree.txt"
    if not os.path.exists(os.path.dirname(all_tree_txt)):
        os.makedirs(os.path.dirname(all_tree_txt))
        # os.system(f'echo. >> "{all_tree_txt}"')
        os.system(f'echo. >> "{all_tree_txt}" >NUL')
        os.system(f'echo. >> "{proper_tree_txt}" >NUL')
    with open(file=all_tree_txt, mode='w', encoding=PkEncoding.UTF8.value) as f:
        f.write(" ")
    with open(file=proper_tree_txt, mode='w', encoding=PkEncoding.UTF8.value) as f:
        f.write(" ")

    drives = "foo"

    f_cnt = 0
    f = open(D_PK_ROOT + '\\all_list.txt', 'a', encoding=PkEncoding.UTF8.value)  # >>  a    > w   각각 대응됨.
    for drive in drives:
        os.chdir(drive)
        for root, d_nx_list, file_nxs in os.walk(os.getcwd()):  # 여기 또 os.getcwd() 있는 부분 수정하자..
            for f_nx in file_nxs:
                f_cnt = f_cnt + 1
                f.write(str(f_cnt) + " " + os.path.join(root, f_nx) + "\n")
    f.close()  # close() 를 사용하지 않으려면 with 문을 사용하는 방법도 있다.
    logging.debug(f"{UNDERLINE}{UNDERLINE}all_list.txt writing e")
    logging.debug(f"{UNDERLINE}{UNDERLINE}all_list_proper.txt rewriting s")
    texts_black = [
        rf"C:\$WinREAgent",
        rf"C:\mingw64",
        rf"C:\PerfLogs",
        rf"C:\Program Files (x86)",
        rf"C:\Program Files",
        rf"C:\ProgramData",
        rf"C:\Temp",
        rf"C:\Users\All Users",
        rf"C:\Windows\servicing",
        rf"C:\Windows\SystemResources",
        rf"C:\Windows\WinSxS",
        rf"C:\Users\Default",
        rf"C:\Users\Public",
        rf"C:\Windows.old",
        rf"C:\Windows",
        rf"C:\$Recycle.Bin",
        rf"D:\$RECYCLE.BIN",
        rf"E:\$RECYCLE.BIN",
        rf"E:\$Recycle.Bin",
        rf"F:\$RECYCLE.BIN",
        rf"{D_HOME}\AppData",
    ]
    texts_white = [
        ".mkv",
    ]
    f = open(rf'{D_PK_ROOT}\all_list.txt', 'r+', encoding=PkEncoding.UTF8.value)
    f2 = open(rf'{D_PK_ROOT}\all_list_proper.txt', 'a', encoding=PkEncoding.UTF8.value)
    lines_cnt = 0
    while 1:
        line = f.readline()
        if not line:
            break
        lines_cnt = lines_cnt + 1
        if any(text_black not in line for text_black in texts_black):
            # logging.debug(line)
            if any(text_white in line for text_white in texts_white):
                # logging.debug(line.split("\n")[0] + " o")
                f2.write(line.split("\n")[0] + " o " + "\n")
                # logging.debug('o')
                pass
            else:
                # logging.debug(line.split("\n")[0] + " x")
                # f2.write(line.split("\n")[0] + " x "+"\n")
                # logging.debug('x')
                pass
    f.close()
    f2.close()
    logging.debug(f"{UNDERLINE}{UNDERLINE}all_list_proper.txt rewriting e")

    logging.debug(f"{UNDERLINE}{UNDERLINE}files opening s")
    os.chdir(os.getcwd())

    # 윈도우냐 아니냐
    os.system("chcp 65001 >NUL")
    os.system('export LANG=en_US.UTF-8 >NUL')

    # os.system("type all_list.txt")
    # os.system("explorer all_list.txt")
    os.system("explorer all_list_proper.txt")
    logging.debug(f"{UNDERLINE}{UNDERLINE}files opening e")

    # os.system('del "'+os.getcwd()+'\\all_list.txt"')
    # mk("all_list.txt")
    logging.debug(f"{UNDERLINE}{UNDERLINE}e")
