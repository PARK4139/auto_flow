from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def check_min_non_null_or_warn(*args, func_n="UNKNOWN", arg_none_required=1):
    non_null_count = sum(arg is not None for arg in args)
    if non_null_count < arg_none_required:
        logging.debug(rf"{func_n}() 동작 조건 불충족 (요구 조건: 최소 {arg_none_required}개, 현재 {non_null_count}개)  ")
        return False
    return True
