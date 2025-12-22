from typing import Optional

from pk_internal_tools.pk_functions.pk_mark_function_test_done import pk_mark_function_test_done


# @ensure_seconds_measured # 시간성능측정이 필요없는 함수는 주석으로 명시적으로 남겨둠.
@pk_mark_function_test_done
def ensure_env_var_completed(
        key_name: str,
        func_n=None,
        mask_log: bool = True,
        sensitive_masking_mode=None,
        options=None,
        history_reset=False,
        guide_text=None,
) -> Optional[str]:
    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_12_12 import ensure_env_var_completed_2025_12_12
    return ensure_env_var_completed_2025_12_12(key_name=key_name, func_n=func_n, mask_log=mask_log, sensitive_masking_mode=sensitive_masking_mode, options=options, history_reset=history_reset, guide_text=guide_text)
