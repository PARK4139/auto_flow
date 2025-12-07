from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
import traceback
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose


# @ensure_seconds_measured
# def get_pnxs_from_d_working(d_working, with_walking=True):
#     from pk_internal_tools.pk_functions.is_d import is_d
#     import os
#     if not os.path.exists(d_working):
#         print(f"The pnx '{d_working}' does not exist.")
#     if not is_d(d_working):
#         print(f"The pnx '{d_working}' is not d")
#     pnx_list = []
#     if with_walking == 1:
#         for root, d_nx_list, file_nxs in os.walk(d_working):
#             for d_nx in d_nx_list:
#                 pnx_list.append(os.path.join(root, d_nx))
#             for f_nx in file_nxs:
#                 pnx_list.append(os.path.join(root, f_nx))
#         return pnx_list
#     if with_walking == 0:
#         if os.path.exists(d_working) and is_d(d_working):
#             pnx_list = [os.path.join(d_working, item) for item in os.listdir(d_working)]
#         return pnx_list


@ensure_seconds_measured
def get_pnxs_from_d_working(
        d_working,
        with_walking=False,
        only_files=False,
        only_dirs=False,
        exclude_keywords=None,
):
    import os
    from pathlib import Path
    from pk_internal_tools.pk_functions.is_d import is_d

    try:
        if not os.path.exists(d_working):
            print(f"The pnx '{d_working}' does not exist.")
            return []

        if not is_d(d_working):
            print(f"The pnx '{d_working}' is not d")
            return []

        if exclude_keywords is None:
            exclude_keywords = [".venv", "__PYCACHE__", "__pycache__"]

        pnx_list = []

        # Temporarily disable exclusion logic for debugging
        # def should_exclude(pnx_path):
        #     return any(keyword.lower() in str(pnx_path).lower() for keyword in exclude_keywords)

        def append_filtered(full_path_obj, is_file_check):
            # if should_exclude(full_path_obj): # Temporarily disable exclusion
            #     return
            if only_files and not full_path_obj.is_file():
                return
            if only_dirs and not full_path_obj.is_dir():
                return
            pnx_list.append(full_path_obj)

        if with_walking:
            for root, d_nx_list, file_nxs in os.walk(d_working):
                root_path = Path(root)
                for d_nx in d_nx_list:
                    append_filtered(root_path / d_nx, is_file_check=False)
                for f_nx in file_nxs:
                    append_filtered(root_path / f_nx, is_file_check=True)
        else:
            for item in os.listdir(d_working):
                full_path_obj = Path(d_working) / item
                append_filtered(full_path_obj, is_file_check=full_path_obj.is_file())

        return pnx_list
    except Exception as e:
        ensure_debug_loged_verbose(traceback)
        return [] # Return empty list on error
