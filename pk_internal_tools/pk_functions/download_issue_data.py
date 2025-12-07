from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
import logging
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing


def download_issue_data(data_required, original_log=False):
    import inspect
    import re

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 전처리
    issue_file_name = data_required["f 위치"].split('/')[-1]

    def get_origin_log_file_name(issue_file_name):
        # 정규식 패턴 정의: "_숫자(최대 2자리)_VIDEO"
        pattern = r"_\d{1,2}_VIDEO"
        original_filename = re.sub(pattern, "", issue_file_name)
        return original_filename

    origin_log_file_name = get_origin_log_file_name(issue_file_name)
    data_required["주행일자"] = data_required["f 위치"].split('/')[0]
    data_required["f 위치"] = data_required["f 위치"].replace("/", f"\\")

    # 정의
    if original_log == False:
        src = rf"\\192.168.1.33\01_Issue\{data_required["f 위치"]}"
    else:
        src = rf"\\192.168.1.33\02_Orignal\{data_required["차량"]}\{data_required["지역"]}\{data_required["주행일자"]}\{data_required["코스"]}\{origin_log_file_name}"
        logging.debug(rf'''src="{src}"  ''')

    dst = rf"C:\log"
    cmd = rf"copy {src} {dst}"
    src_nx = get_nx(pnx=src)
    src_new = rf"{dst}\{src_nx}"

    while 1:
        if is_pnx_existing(pnx=src_new):
            logging.debug(rf'''{src_new} 가 이미 있습니다."  ''')
            break
        else:
            if not is_pnx_existing(pnx=src_new):
                ensure_command_executed(cmd=cmd, mode="a")
                logging.debug(rf'''이슈데이터 다운로드 완료 "{src_new}"  ''')
                return
