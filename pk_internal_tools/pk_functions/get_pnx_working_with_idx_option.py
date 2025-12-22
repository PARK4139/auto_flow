def get_pnx_working_with_idx_option(origin_list, minus_list=None, plus_list=None):
    from pk_internal_tools.pk_functions.get_list_differenced import get_list_differenced
    from pk_internal_tools.pk_functions.get_list_unioned import get_list_unioned
    if plus_list is not None:
        origin_list = get_list_unioned(list_a=origin_list, list_b=plus_list)
    if minus_list is not None:
        origin_list = get_list_differenced(list_a=origin_list, list_b=minus_list)
    pnx_working_with_idx_dict = {}
    for index, pnx_working in enumerate(origin_list):
        pnx_working_with_idx_dict[index] = pnx_working
    return pnx_working_with_idx_dict
