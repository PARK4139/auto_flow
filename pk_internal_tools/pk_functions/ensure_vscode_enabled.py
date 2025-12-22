from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_vscode_enabled():
    from pk_internal_tools.pk_functions.ensure_target_executed_2025_10_17_1649 import ensure_target_executed_2025_10_17_1649

    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    from pk_internal_tools.pk_objects.pk_files import F_VSCODE_LNK
    ensure_target_executed_2025_10_17_1649(F_VSCODE_LNK, D_PK_ROOT)
