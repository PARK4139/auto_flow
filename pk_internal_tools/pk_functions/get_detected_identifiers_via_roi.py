from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_detected_identifiers_via_roi(identifiers, history_reset, text_to_find="준비"):
    """
        TODO: Write docstring for get_detected_identifiers_via_roi.
    """
    try:
        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
        from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
        from pk_internal_tools.pk_functions.ensure_text_appears_in_roi import ensure_text_appears_in_roi

        detected_identifiers = []
        for id in identifiers:
            key_name = id
            roi_id = rf'{key_name} ROI'
            if ensure_text_appears_in_roi(key_name=key_name, text=text_to_find, history_reset=history_reset):
                alert_as_gui(text=f"{text_to_find} found\n in {roi_id}")
                detected_identifiers.append(id)
            else:
                alert_as_gui(text=f"{text_to_find} not found\n in {roi_id}")
                # ensure_paused()
        return detected_identifiers
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
