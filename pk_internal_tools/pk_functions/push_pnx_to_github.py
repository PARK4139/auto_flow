from pk_internal_tools.pk_functions.get_text_blue import get_text_blue


def push_pnx_to_github(d_working, commit_msg, branch_n):
    import os

    from pk_internal_tools.pk_functions import ensure_pnx_made
    from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging
    logging.debug(f'''commit_msg={commit_msg} ''')
    if not is_internet_connected_2025_10_21():
        return
    if not is_pnx_existing(pnx=d_working):
        ensure_pnx_made(pnx=d_working, mode='d')
    os.chdir(d_working)
    git_local_repo_checkfile = rf"{d_working}/.git"
    std_list = None
    state_done = [0, 0, 0, 0]

    while 1:
        if state_done[0] == 0:
            if not is_pnx_existing(pnx=git_local_repo_checkfile):
                std_list = ensure_command_executed(cmd=rf'git init')
                continue
        state_done[0] = 1
        logging.debug(f'''state_done={state_done} ''')
        if state_done[1] == 0:
            std_list = ensure_command_executed(cmd=rf'git add .')  # git add * 과는 약간 다름.
            # signature_list = ["The following paths are ignored by one of your .gitignore files:"]
            if not len(std_list) == 0:
                logging.debug(rf'''''')
                continue
            # if not any(text_working in std_list for text_working in signature_list):
            #     continue
        state_done[1] = 1
        logging.debug(f'''state_done={state_done} ''')
        if state_done[2] == 0:
            # std_list = ensure_command_executed(cmd=rf'git commit -m "{commit_msg}"')
            std_list = ensure_command_executed(cmd=rf'git commit -m "{get_text_blue(commit_msg)}"')
            signature_list = ["nothing to commit, working tree clean"]
            if not any(text_working in std_list for text_working in signature_list):
                logging.debug(rf'''''')
                continue
        state_done[2] = 1
        logging.debug(f'''state_done={state_done} ''')
        if state_done[3] == 0:
            std_list = ensure_command_executed(cmd=rf'git push origin {branch_n}')
            signature_list = ["Everything up-to-date", "branch 'main' set up to track 'origin/main'."]
            if not any(text_working in std_list for text_working in signature_list):
                continue
        state_done[3] = 1
        logging.debug(f'''state_done={state_done} ''')
        break
