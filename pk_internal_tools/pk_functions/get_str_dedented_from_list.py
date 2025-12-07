from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_str_dedented_from_list(texts: list):
    import textwrap
    import traceback
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    try:
        texts = ["\n"] + texts
        str_dedented = textwrap.dedent("\n".join(texts))
        return str_dedented
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
