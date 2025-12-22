from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_text_chain(*args, wrapping_string='"'):
    return " ".join([f'{wrapping_string}{arg}{wrapping_string}' for arg in args])
