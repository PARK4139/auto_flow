import logging


def ensure_state_printed(state, pk_id, state_header=None):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    if state_header is not None:
        logging.debug(f'''{state_header} {f'{pk_id}' if QC_MODE else ''}''')
    logging.debug(f'''{state} {f'{pk_id}' if QC_MODE else ''}''')
