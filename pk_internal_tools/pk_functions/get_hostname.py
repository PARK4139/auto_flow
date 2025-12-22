from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_hostname():
    return get_hostname_v3()


def get_hostname_v1():
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human_as_admin import ensure_command_executed_like_human_as_admin

    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    lines = ensure_command_executed_like_human_as_admin('hostname')
    for line in lines:
        line = line.strip()
        return line


def get_hostname_v2():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_str_url_decoded import get_str_url_decoded
    hostname = ensure_command_executed("hostname")[0]
    hostname = get_str_url_decoded(hostname)
    return hostname


def get_hostname_v3():
    from pk_internal_tools.pk_functions.get_str_url_decoded import get_str_url_decoded
    import socket
    hostname = socket.gethostname()
    hostname = get_str_url_decoded(hostname)
    return hostname
