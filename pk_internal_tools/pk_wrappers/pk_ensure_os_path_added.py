import sys
import traceback

from pk_internal_tools.pk_functions.ensure_os_path_added import ensure_os_path_added

if __name__ == "__main__":
    try:
        ensure_os_path_added()
    except Exception:
        print(traceback.format_exc())
        sys.exit(1)
