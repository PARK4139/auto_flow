from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def print_pk_ls(index_map: list[str], limit: int = None):
    import logging

    import os
    logging.debug("실행 가능한 pk_ 프로그램 목록:")

    for idx, filepath in enumerate(index_map):

        if limit is not None and idx >= limit:
            logging.debug(f"... (이하 {len(index_map) - limit}개 생략됨)")
            break
        logging.debug(f"[pk {idx} ] {os.path.basename(filepath).replace(rf"[??????]", "")}")
