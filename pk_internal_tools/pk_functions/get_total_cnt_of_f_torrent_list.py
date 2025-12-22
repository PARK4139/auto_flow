def get_total_cnt_of_f_torrent_list(h3_text):
    import logging

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import re
    total_cnt_of_f_torrent_list = None
    logging.debug(f'''h3_text={h3_text}  ''')
    match = re.search(r"\((\d+)\)", h3_text)
    if match:
        matched_group = match.group(1)  # 첫 번째 캡처 그룹 (숫자) 반환
        logging.debug(f'''matched_group={matched_group}  ''')
        total_cnt_of_f_torrent_list = int(matched_group)
        logging.debug(f'''total_cnt_of_f_torrent_list={total_cnt_of_f_torrent_list}  ''')
    return total_cnt_of_f_torrent_list
