# !/usr/bin/env python   # shebang
# -*- coding: utf-8 -*-  # encoding declaration
__author__ = 'junghoon.park'

import traceback

from pk_internal_tools.pk_functions.ensure_git_cloned_project_from_git_hub import ensure_git_cloned_project_from_git_hub
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_urls import URL_GIT_HUB_PK_TASK_ORCHESTRATOR_CLI_GIT
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # db = PkSqlite3()

        func_n = get_caller_name()

        key_name = 'git_hub_repository_url'
        options = [URL_GIT_HUB_PK_TASK_ORCHESTRATOR_CLI_GIT]
        repository_url = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        key_name = 'git_branch_name'
        options = ["main", "dev"]
        git_branch_name = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        key_name = 'checkout_path'
        options = ["test", "pk_sytsem"]
        checkout_path = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        ensure_git_cloned_project_from_git_hub(repository_url=repository_url, branch_name=git_branch_name, checkout_path=checkout_path)



    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
