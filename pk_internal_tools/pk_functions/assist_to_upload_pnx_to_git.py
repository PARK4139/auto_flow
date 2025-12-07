from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
from pk_internal_tools.pk_functions.ensure_d_size_stable import ensure_d_size_stable
from pk_internal_tools.pk_functions.ensure_input_preprocessed import ensure_input_preprocessed
import logging
from pk_internal_tools.pk_functions.push_pnx_to_github import push_pnx_to_github
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def assist_to_upload_pnx_to_git(d_working, git_repo_url, branch_n):
    logging.debug(f'''d_working={d_working} ''')
    loop_cnt = 1
    while 1:
        try:
            if loop_cnt == 1:
                commit_msg = ensure_input_preprocessed(text_working=f"commit_msg=", upper_seconds_limit=60,
                                                       return_default=f"feat: make save point by auto at {get_pk_time_2025_10_20_1159('%Y-%m-%d %H:%M')}")
                push_pnx_to_github(d_working=d_working, commit_msg=commit_msg,
                                   branch_n=branch_n)
                loop_cnt = loop_cnt + 1
            if not ensure_d_size_stable(d_working, limit_seconds=30):
                if ensure_d_size_stable(d_working, limit_seconds=30):
                    logging.debug("change stable after  change detected")
                    commit_msg = ensure_input_preprocessed(text_working=f"commit_msg=", upper_seconds_limit=60,
                                                           return_default=f"feat: make save point by auto at {get_pk_time_2025_10_20_1159('%Y-%m-%d %H:%M')}")
                    push_pnx_to_github(d_working=d_working, commit_msg=commit_msg,
                                       branch_n=branch_n)
        except:
            import traceback
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
            break
