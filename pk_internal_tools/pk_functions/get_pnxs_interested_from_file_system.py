



from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden


def get_pnxs_interested_from_file_system(pnx_interested_list=None, string_exclude=None):
    f_func_n_txt = rf"{d_pk_root_hidden}\make_pnx_interested_list_to_text_file.txt"

    if pnx_interested_list is None:
        # todo make_pnx_interested_list_to_text_file_x f이 없으면 만들도록
        make_pnx_interested_list_to_f_txt_x(d_working_list=pnx_interested_list, exclusion_list=string_exclude)

        # PKG_CACHE_PRIVATE = rf"{d_pk_root_hidden}"
        # window_title_seg = get_nx(PKG_CACHE_PRIVATE)
        # if not is_window_opened(window_title_seg=window_title_seg):
        #     open_pnx(pnx=PKG_CACHE_PRIVATE)
    else:
        make_pnx_interested_list_to_f_txt(pnx_interested_list=pnx_interested_list, string_exclude=string_exclude)

        # window_title_seg = get_nx (f_func_n_txt)
        # if not is_window_opened(window_title_seg=window_title_seg):
        #     open_pnx(pnx=f_func_n_txt)

    return get_list_from_f(f=f_func_n_txt)
