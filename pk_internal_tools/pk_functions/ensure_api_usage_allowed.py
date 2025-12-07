from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_api_usage_allowed(api_key_id):
    from pk_internal_tools.pk_functions import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_urls import URL_OPEN_API_USAGE_DASHBOARD

    if api_key_id == "OPENAI_API":
        ensure_command_executed(cmd=fr"explorer.exe {URL_OPEN_API_USAGE_DASHBOARD}")

    question = rf"are you sure {api_key_id} usage proper"
    decision = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
    if decision == PkTexts.YES:
        return True
    else:
        return False


