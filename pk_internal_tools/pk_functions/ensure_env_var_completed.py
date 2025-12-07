from typing import Optional

from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_env_var_completed(
        key_name: str,
        func_n,
        mask_log: bool = True,
        sensitive_masking_mode=None,
        options=None,
        history_reset=False,
        guide_text=None,
) -> Optional[str]:
    return ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n, mask_log=mask_log, sensitive_masking_mode=sensitive_masking_mode, options=options, history_reset=history_reset, guide_text=guide_text)
