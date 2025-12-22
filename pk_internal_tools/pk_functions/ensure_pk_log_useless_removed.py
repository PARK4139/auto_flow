def ensure_pk_log_useless_removed(text, loop_mode=False):
    import logging
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_last_lines_removed_from_file import ensure_last_lines_removed_from_file
    from pk_internal_tools.pk_functions.get_line_number_from_file import get_line_number_from_file
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    if QC_MODE:
        if loop_mode == True:
            while 1:
                line_number = get_line_number_from_file(text=text, from_reverse_mode=True, file_path=F_PK_LOG)
                if line_number:
                    if int(line_number):
                        ensure_last_lines_removed_from_file(file=F_PK_LOG, lines_to_remove_from_end=line_number)
                        return True
                ensure_slept(milliseconds=77)

        else:
            line_number = get_line_number_from_file(text=text, from_reverse_mode=True, file_path=F_PK_LOG)
            if line_number is not None:
                ensure_last_lines_removed_from_file(file=F_PK_LOG, lines_to_remove_from_end=int(line_number))
                logging.debug(rf"line_number={line_number}")
                return True
            else:
                logging.debug(f"Text '{text[:10]}...' not found in log file. No lines removed.")
                return False
