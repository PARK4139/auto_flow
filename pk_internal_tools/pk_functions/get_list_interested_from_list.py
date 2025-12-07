import logging

from pk_internal_tools.pk_functions.get_list_replaced_element_from_str_to_str import get_list_replaced_element_from_str_to_str


def get_list_interested_from_list(working_list, string_list_include=[], string_list_exclude=[], except_extensions=[],
                                  ext_list_include=[], string_list_include_any=[]):
    import os
    if working_list is None:
        logging.debug("working_list가 None입니다. 올바른 리스트를 전달하세요.")
    pnxs_included = []
    for item in working_list:
        if not string_list_include == []:
            if any(text in item for text in string_list_include):
                pnxs_included.append(item)
        else:
            pnxs_included.append(item)
    pnxs_included = get_list_replaced_element_from_str_to_str(working_list=pnxs_included, from_str="\n", to_str="")
    # print_list_as_vertical(working_list=pnxs_included, working_list_n='pnxs_included')

    pnxs_excluded = []
    for pnx in pnxs_included:
        # txt_to_exclude_list의 어떠한 요소도 포함되지 않은 경우만 추가
        if not any(exclude_text in pnx for exclude_text in string_list_exclude):  # 배제할 확장자 체크
            file_extension = os.path.splitext(pnx)[1]
            if file_extension not in except_extensions:  # 제외할 확장자 체크
                if not ext_list_include == []:
                    if any(file_extension == ext for ext in ext_list_include):  # 반드시 포함할 확장자 체크
                        pnxs_excluded.append(pnx)
                else:
                    pnxs_excluded.append(pnx)
    # print_list_as_vertical(working_list=pnxs_excluded, working_list_n="pnxs_excluded")

    pnxs_required = []
    if not string_list_include_any == []:
        for item in pnxs_excluded:
            if any(include in item for include in string_list_include_any):
                pnxs_required.append(item)
    else:
        pnxs_required = pnxs_excluded
    return pnxs_required
