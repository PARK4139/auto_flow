from tkinter import UNDERLINE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
import logging


def update_global_pkg_alba():
    import inspect
    import os
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    local_pkg = rf"{d_pk_root}\pkg_alba"
    global_pkg = rf"C:\Python312\Lib\site-packages\pkg_alba"
    updateignore_txt = rf"{d_pk_root}\pkg_alba\updateignore.txt"
    try:
        if os.path.exists(global_pkg):
            # remove시도
            # shutil.rmtree(global_pkg)

            # remove시도
            # for file in os.scandir(global_pkg):
            # os.remove(file.path)

            # 덮어쓰기
            # src= local_pkg
            # dst =os.path.dirname(global_pkg)
            # os.system(f"echo y | copy {src} {dst}")
            # shutil.copytree(local_pkg, os.path.dirname(global_pkg))
            cmd = f'echo y | xcopy "{local_pkg}" "{global_pkg}" /k /e /h /exclude:{updateignore_txt} >NUL'
            os.system(cmd)

            logging.debug(f'{cmd}')
            logging.debug(f"{UNDERLINE}")
            return "REPLACED global pkg_alba AS local_pkg"
        else:
            return "pkg_alba NOT FOUND AT GLOBAL LOCATION"

    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
