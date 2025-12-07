from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_filenames_to_display(files):
    from pk_internal_tools.pk_functions.get_nx import get_nx
    return [get_nx(p) for p in files]
