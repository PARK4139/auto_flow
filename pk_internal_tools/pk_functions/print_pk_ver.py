

def print_pk_ver():
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging

    if QC_MODE:
        logging.debug(f'''''')
    print('pk_ver.1.32.12')
