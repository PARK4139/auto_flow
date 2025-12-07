

def ensure_pnxs_renamed_2025_10_30(d_working, mode, with_walking, debug_mode=False):
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    logging.debug(rf'''d="{d_working}" mode="{mode}"  ''')

    ensure_pnxs_renamed_2025_10_30_from_keywords_to_keyword_new_at_d(d=d_working, mode=mode, with_walking=with_walking)
    ensure_pnxs_renamed_2025_10_30_from_pattern_to_pattern_new_via_routines_at_d(d=d_working, mode=mode, with_walking=with_walking)
    ensure_pnxs_renamed_2025_10_30_from_keywords_to_keyword_new_at_d(d=d_working, mode=mode, with_walking=with_walking)
