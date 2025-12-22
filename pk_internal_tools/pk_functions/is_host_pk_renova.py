from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def is_host_pk_renova():
    import traceback

    from pk_internal_tools.pk_functions.check_hostname_match import check_hostname_match
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

    try:
        return check_hostname_match(target_hostname_value="desktop-ucr7igi", match_type="equals",
                                    pc_name_for_log="RENOVA_PC")
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
