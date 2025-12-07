from typing import Optional

from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme
from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForEnsureValueCompleted20251130


# @ensure_seconds_measured
def ensure_value_completed(key_name, func_n, options=None, guide_text=None, history_reset=False, sort_order: Optional[SetupOpsForEnsureValueCompleted20251130] = SetupOpsForEnsureValueCompleted20251130.HISTORY, fzf_theme: PkFzfTheme = PkFzfTheme(), history_mode: bool = True):
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30

    return ensure_value_completed_2025_11_30(key_name=key_name, func_n=func_n, options=options, guide_text=guide_text, history_reset=history_reset, sort_order=sort_order, fzf_theme=fzf_theme, history_mode=history_mode)
