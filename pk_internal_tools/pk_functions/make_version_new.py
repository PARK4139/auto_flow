from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed


def make_version_new(via_f_txt, working_list=None):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    make_version_new_v_1_0_1(via_f_txt=via_f_txt, working_list=working_list)
    pass
