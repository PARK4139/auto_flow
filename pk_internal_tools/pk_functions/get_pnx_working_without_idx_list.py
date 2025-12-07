

def get_pnx_working_without_idx_list(pnx_working_with_idx_dict):
    pnx_working_list = []
    for idx, pnx_working_with_idx in enumerate(pnx_working_with_idx_dict):
        pnx_working_list.append(pnx_working_with_idx_dict[idx])
    return pnx_working_list
