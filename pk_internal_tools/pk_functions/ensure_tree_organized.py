def ensure_tree_organized(d_working, with_walking):
    # src=rf"{USERPROFILE}\Downloads" # __init__.py   init_.py 가 되어 문제가 되었다.
    mode = 'f'
    ensure_target_files_useless_gathered(d_working=d_working)
    ensure_pnxs_renamed_2025_10_30(d_working=d_working, mode=mode, with_walking=with_walking)
    classify_pnx_list_at_tree(d_working=d_working, mode=mode, with_walking=with_walking)
    ensure_pnxs_renamed_2025_10_30(d_working=d_working, mode=mode, with_walking=with_walking)
    gather_empty_d(d_working=d_working)
    # empty_recycle_bin() # 비우기

    mode = 'd'
    ensure_target_files_useless_gathered(d_working=d_working)
    ensure_pnxs_renamed_2025_10_30(d_working=d_working, mode=mode, with_walking=with_walking)
    classify_pnx_list_at_tree(d_working=d_working, mode=mode, with_walking=with_walking)
    ensure_pnxs_renamed_2025_10_30(d_working=d_working, mode=mode, with_walking=with_walking)
    gather_empty_d(d_working=d_working)
    # empty_recycle_bin()  # 비우기
