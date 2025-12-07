from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_installed(__file__):
    import traceback

    from pk_internal_tools.pk_functions.ensure_command_executed_like_human import ensure_command_executed_like_human
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    func_n = get_caller_name()
    try:
        if QC_MODE:
            key_name = rf"GEMINI 최신버전 설치 계속 진행합니다"
            ensure_spoken(f'{key_name}')
        else:
            key_name = rf"GEMINI 최신버전 설치 계속 진행할까요"
            ok = ensure_value_completed(key_name=key_name, options=[PkTexts.YES, PkTexts.NO], func_n=func_n)
            if ok != PkTexts.YES:
                ensure_pk_wrapper_starter_suicided(__file__)

        ensure_command_executed_like_human('npm install -g @google/gemini-cli@latest')

    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        ensure_spoken(wait=True)
