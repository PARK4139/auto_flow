

def get_name_space():  # name space # namespace # 파이썬 네임스페이스
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    dir()
    return dir()
