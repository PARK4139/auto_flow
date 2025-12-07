


def ensure_mail_found():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_urls import URL_NAVER_MAIL, URL_GOOGLE_MAIL
    ensure_command_executed(cmd=fr"explorer.exe {URL_NAVER_MAIL}")
    ensure_command_executed(cmd=fr"explorer.exe {URL_GOOGLE_MAIL}")
