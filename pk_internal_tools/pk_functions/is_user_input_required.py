from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_user_input_required(user_input: str):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # 수정 필요.
    user_input = user_input.strip()
    logging.debug(rf'''user_input="{user_input}"  ''')
    if is_only_no(user_input):
        user_input = int(user_input)
    else:
        ensure_spoken_v2("you can input only number, please input only number again")
        return None
    return user_input
