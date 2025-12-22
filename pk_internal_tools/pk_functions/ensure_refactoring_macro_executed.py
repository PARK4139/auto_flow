from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_refactoring_macro_executed(macro):
    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_wrappers.pk_ensure_refactoring_macro_executed import PkMacros

    import logging
    import os
    import time

    from pk_internal_tools.pk_functions.ensure_pycharm_module_optimize import ensure_pycharm_module_import_script_optimize

    # log start
    logging.debug(f"LOCAL LEPO :  {os.getcwd()}")
    logging.debug(f"STARTED AT :  {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # do macro routine
    if macro == PkMacros.PYCHARM_CODE_OPTIMIZATION:
        ensure_pycharm_module_import_script_optimize()
    else:
        ensure_not_prepared_yet_guided()
