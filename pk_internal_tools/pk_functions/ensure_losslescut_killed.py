from pk_internal_tools.pk_functions.ensure_process_killed_by_image_name import ensure_process_killed_by_image_name
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_losslescut_killed():
    return ensure_process_killed_by_image_name('losslesscut.exe')
