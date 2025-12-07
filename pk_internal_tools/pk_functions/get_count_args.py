def get_count_args(func):
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    return func.__code__.co_argcount
