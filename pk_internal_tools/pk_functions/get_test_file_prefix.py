import traceback
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

@ensure_seconds_measured
def get_test_file_prefix():
    try:
        return  "test_testcases_of_"
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
