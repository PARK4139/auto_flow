



from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def get_userprofile_via_cmd_exe():
    userprofile = ensure_command_executed("echo %USERPROFILE%")[0]
    userprofile = get_str_url_decoded(userprofile)
    return userprofile
