from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_refactor_py_files():
    import os
    import glob
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    # Build refactor_dir path (absolute)
    current_dir = os.path.dirname(__file__)
    refactor_dir = os.path.abspath(os.path.join(current_dir, "..", "refactor"))

    # Print refactor_dir path for debugging
    log_msg = f"refactor_dir={refactor_dir}"
    logging.debug(log_msg + (" %%%FOO%%%" if QC_MODE else ""))

    # List all .py files in refactor_dir
    pattern = os.path.join(refactor_dir, "*.py")
    return sorted(glob.glob(pattern))
