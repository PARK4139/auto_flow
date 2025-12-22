from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def is_host_pk_l_cam_pc():
    """
        TODO: Write docstring for is_host_pk_l_cam_pc.
    """
    try:
        import traceback

        from pk_internal_tools.pk_functions.check_hostname_match import check_hostname_match
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

        return check_hostname_match(target_hostname_value="LAPTOP-485DCU40", match_type="equals",
                                        pc_name_for_log="L_CAM_PC")

    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
