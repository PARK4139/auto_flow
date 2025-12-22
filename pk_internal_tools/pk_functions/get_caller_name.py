# from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
#
#
# @ensure_seconds_measured
def get_caller_name():
    # 스택의 바로 이전 프레임이 이 함수를 호출한 프레임입니다.
    # stack()[0]은 현재 프레임(get_caller_name)
    # stack()[1]은 호출자의 프레임
    '''
        # 최상위 호출에서는
        # func_n = get_nx(__file__)

        # 함수내 호출에서는
        # func_n = inspect.currentframe().f_code.co_name

        # 판단귀찮으면
        # from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
    '''

    import inspect
    import os
    caller_frame_record = inspect.stack()[1]
    caller_name = caller_frame_record.function

    if caller_name == '<module>':
        # 최상위 레벨에서 호출됨. 파일 경로를 가져옵니다.
        module_path = caller_frame_record.filename
        caller_name = os.path.splitext(os.path.basename(module_path))[0]
        return caller_name
    else:
        return caller_name
