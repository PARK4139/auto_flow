from typing import Optional

from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureValueCompleted
from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme


# @ensure_seconds_measured
def ensure_value_completed(key_name, func_n=None, options=None, guide_text=None, history_reset=False, sort_order: Optional[PkModesForEnsureValueCompleted] = PkModesForEnsureValueCompleted.HISTORY, fzf_theme: PkFzfTheme = PkFzfTheme(), history_mode: bool = True):
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_12_12 import ensure_value_completed_2025_12_12
    return ensure_value_completed_2025_12_12(key_name=key_name, func_n=func_n, options=options, guide_text=guide_text, history_reset=history_reset, sort_order=sort_order, fzf_theme=fzf_theme, history_mode=history_mode)
