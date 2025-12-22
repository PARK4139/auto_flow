import traceback
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

@ensure_seconds_measured
def get_test_file_prefix():
    try:
        return  "test_testcases_of_"
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
