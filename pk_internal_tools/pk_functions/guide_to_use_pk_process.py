

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def guide_to_use_pk_process(pk_process_pnx_list, nx_by_user_input):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    
    from pk_internal_tools.pk_functions.get_nx import get_nx
    import logging
    if QC_MODE:
        logging.debug(f'''''')
    for idx, pnx_working in enumerate(pk_process_pnx_list):

        if nx_by_user_input in pnx_working:
            if QC_MODE:
                logging.debug(f'''pnx_working={pnx_working} ''')
            if nx_by_user_input in get_nx(pnx_working):

                if nx_by_user_input != get_nx(pnx_working):
                    print(rf'''{'{PkTexts.TRY_GUIDE}'} pk {idx} ({get_nx(pnx_working)}) ''')
            else:
                if QC_MODE:
                    logging.debug(f'''''')
                break
