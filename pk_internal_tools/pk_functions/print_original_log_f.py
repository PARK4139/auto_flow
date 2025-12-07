from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_original_log_f(issue_log_index_data):
    import re

    original_log = True

    # 전처리
    if isinstance(issue_log_index_data["_f_ 위치"], float):
        issue_log_index_data["_f_ 위치"] = ""

    issue_file_name = issue_log_index_data["_f_ 위치"].split('/')[-1]

    def get_origin_log_file_name(issue_file_name):
        # 정규식 패턴 정의: "_숫자(최대 2자리)_VIDEO"
        pattern = r"_\d{1,2}_VIDEO"
        original_filename = re.sub(pattern, "", issue_file_name)
        return original_filename

    origin_log_file_name = get_origin_log_file_name(issue_file_name)
    issue_log_index_data["주행일자"] = issue_log_index_data["_f_ 위치"].split('/')[0]
    issue_log_index_data["_f_ 위치"] = issue_log_index_data["_f_ 위치"].replace("/", f"\\")

    src = rf"\\192.168.1.33\01_Issue\{issue_log_index_data["_f_ 위치"]}"
    logging.debug(rf'''src="{src}"  ''')
    if original_log == True:
        src = rf"\\192.168.1.33\02_Orignal\{issue_log_index_data["차량"]}\{issue_log_index_data["지역"]}\{issue_log_index_data["주행일자"]}\{issue_log_index_data["코스"]}\{origin_log_file_name}"
        logging.debug(rf'''src="{src}"  ''')
        return
