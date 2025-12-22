

def ensure_tmux_pk_session_removed(tmux_pk_session):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    import logging

    if QC_MODE:
        logging.debug(f'''pk_session_n={tmux_pk_session} ''')
    for std_str in ensure_command_executed(f'tmux ls'):
        if tmux_pk_session in std_str:
            ensure_command_executed(f'tmux kill-session -t {tmux_pk_session}')
