from types import ModuleType


def ensure_this_code_operated(ipdb: ModuleType):
    from pk_internal_tools.pk_functions.ensure_pk_system_log_editable import ensure_pk_system_log_editable
    import logging
    from pk_internal_tools.pk_objects.pk_colors import PkColors

    # based on from types import ModuleType
    logging.debug(f"{PkColors.CYAN}here! here! here! here! here! here! here! here! here! here! here! here! {PkColors.RESET}")
    ensure_pk_system_log_editable(ipdb)
