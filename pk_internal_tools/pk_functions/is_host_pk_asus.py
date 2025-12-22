import traceback

from pk_internal_tools.pk_functions.check_hostname_match import check_hostname_match
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def is_host_pk_asus():
    try:
        def is_host_pk_asus():
            """Checks if the current PC is the Anyang house desktop."""
            return check_hostname_match(target_hostname_value="pk", match_type="contains", pc_name_for_log="Anyang house PC")

        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
