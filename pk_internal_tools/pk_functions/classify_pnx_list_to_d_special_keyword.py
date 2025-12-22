from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN


def classify_pnx_list_to_d_special_keyword(d_src, with_walking):
    f = rf'{D_PK_ROOT_HIDDEN}/collect_magnets_from_nyaa_si.txt'
    special_keywords_from_f_txt = get_list_from_f(f=f)
    special_keywords_from_f_txt = get_list_removed_element_contain_prompt(working_list=special_keywords_from_f_txt,
                                                                          prompt="#")
    # special_keywords_from_f_txt = get_list_replaced_element_from_str_to_str(working_list=special_keywords_from_f_txt, from_str='\n', to_str='')
    special_keywords_from_f_txt = get_list_striped_element(working_list=special_keywords_from_f_txt)
    special_keywords_from_f_txt = get_list_deduplicated(working_list=special_keywords_from_f_txt)
    special_keywords_from_f_txt = get_list_removed_empty(working_list=special_keywords_from_f_txt)
    special_keywords_from_f_txt = get_list_without_none(working_list=special_keywords_from_f_txt)
    special_keywords = [  # special_keywords는 텍스트의 길이가 길수록 분류가 잘될 확률이 높다
                           "[]",
                       ] + special_keywords_from_f_txt
    for special_keyword in special_keywords:
        classify_pnx_by_special_keyword(d_src=d_src, special_keyword=special_keyword, with_walking=with_walking)
