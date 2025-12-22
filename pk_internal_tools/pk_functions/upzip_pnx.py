

from selenium.webdriver.common.action_chains import ActionChains
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from concurrent.futures import ThreadPoolExecutor

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def upzip_pnx(pnx):
    import os
    import traceback

    try:
        while 1:
            # 전처리
            pnx = pnx.replace("\n", "")
            pnx = pnx.replace("\"", "")

            if pnx.strip() == "":
                logging.debug("백업할 대상이 입력되지 않았습니다")
                break

            pnx_dirname = os.path.dirname(pnx)
            pnx_basename = os.path.basename(pnx).split(".")[0]
            target_zip = rf'{pnx_dirname}\{pnx_basename}.zip'

            os.chdir(pnx_dirname)

            if os.path.exists(target_zip):
                # cmd=f'bandizip.exe bx "{target_zip}"'
                cmd = f'bz.exe x -aoa "{target_zip}"'  # x 는 경로 보존, -aoa :Overwrite All existing files without prompt
                ensure_command_executed_like_human_as_admin(cmd)
                if os.path.exists(pnx):
                    cmd = rf'echo y | del /f "{target_zip}"'
                    ensure_command_executed_like_human_as_admin(cmd)
                else:
                    logging.debug("압축해제 후 압축f을 삭제에 실패")
            else:
                logging.debug("압축해제할 f이 없었습니다")
            os.chdir(D_PK_ROOT)
            print_success("압축해제 성공")
            break
    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        os.chdir(D_PK_ROOT)
