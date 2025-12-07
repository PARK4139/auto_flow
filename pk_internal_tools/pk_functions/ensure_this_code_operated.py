from types import ModuleType


def ensure_this_code_operated(ipdb: ModuleType):
    from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
    import logging
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP

    # based on from types import ModuleType
    logging.debug(f"{PK_ANSI_COLOR_MAP['CYAN']}here! here! here! here! here! here! here! here! here! here! here! here! {PK_ANSI_COLOR_MAP['RESET']}")
    ensure_pk_log_editable(ipdb)
