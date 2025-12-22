import toml
import clipboard
from pk_internal_tools.pk_functions.get_nx import get_nx

import logging


def print_json_via_jq_pkg(json_str=None, json_file=None, json_list=None):
    import inspect
    import json

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if get_os_n() == 'windows':
        if get_count_none_of_list([json_str, json_file, json_list]) == 2:  # 2개가 NONE이면 1나는 BINDING 된것으로 판단하는 로직
            if json_str is not None:
                # lines=run_via_cmd_exe(cmd=rf'echo "{json_str}" | {JQ_WIN64_EXE} "."') # 나오긴 하는데 한줄로 나온다
                # lines=run_via_cmd_exe(cmd=rf'echo "{json_str}" | python -mjson.tool ')# 나오긴 하는데 한줄로 나온다
                # [print_as_success(line) for line in lines]
                json_str = json.dumps(json_str,
                                      indent=4)  # json.dumps() 함수는 JSON 데이터를 문자열로 변환하는 함수이며, indent 매개변수를 사용하여 들여쓰기를 설정하여 json 형태의 dict 를 예쁘게 출력할 수 있습니다.
                print_light_white(json_str)
            if json_file is not None:
                lines = ensure_command_executed_like_human_as_admin(cmd=rf"type {json_file} | {F_JQ_WIN64} ")
                [print_light_white(line) for line in lines]
            if json_list is not None:
                lines = ensure_command_executed_like_human_as_admin(cmd=rf'echo "{json_list}" | "{F_JQ_WIN64}" ')
                [print_light_white(line) for line in lines]
        else:
            logging.debug(rf"{inspect.currentframe().f_code.co_name}() 를 사용하려면 json_str/json_file/json_list 파라미터들 중 둘 중 하나만 데이터바인딩이 되어야합니다")
    else:
        logging.debug("리눅스 시스템에서 아직 지원되지 않는 함수입니다")
