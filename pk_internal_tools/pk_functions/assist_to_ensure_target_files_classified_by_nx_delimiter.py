from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_directories import d_pk_root
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000


def assist_to_ensure_target_files_classified_by_nx_delimiter():
    from colorama import init as pk_colorama_init

    ensure_pk_colorama_initialized_once()

    options = [D_PK_WORKING, d_pk_root, D_DOWNLOADS]
    while 1:
        d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=options)
        options.append(d_working)
        options = get_list_deduplicated(working_list=options)
        word_set = get_word_set_from_f_list(d_working=d_working)
        word_list = get_list_from_set(working_set=word_set)
        word_list = get_list_unioned(list_a=word_list, list_b=['seg', 'SEG'])
        word_list = get_list_sorted(origins=word_list)
        nx_delimiter = ensure_value_completed_2025_10_12_0000(key_name='nx_delimiter', options=word_list)
        # for nx_delimiter in range(2000,2024):
        #     organize_f_list_by_nx_delimiter(nx_delimiter=str(nx_delimiter), d_working=d_working)
        pk_organize_f_list_by_nx_delimiter(nx_delimiter=nx_delimiter, d_working=d_working)
