if __name__ == "__main__":
    import logging
    import os
    import sys
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_target_files_classified_by_ngram import ensure_target_files_classified_by_ngram
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.get_extensions_from_d import get_extensions_from_d
    from pk_internal_tools.pk_functions.get_tuple_from_set import get_tuple_from_set
    from pk_internal_tools.pk_objects.pk_file_extensions import FILE_EXTENSIONS
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_WORKING, D_DOWNLOADED_FROM_TORRENT
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        allowed_extensions = None
        if QC_MODE:
            # d_working = D_DOWNLOADED_FROM_TORRENT
            d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=[str(D_PK_WORKING), os.getcwd(), d_pk_root, D_DOWNLOADS, D_DOWNLOADED_FROM_TORRENT])
            token_splitter_pattern = r"\s+"

            # min_support = int("5")
            # max_n = int("5")

            min_support = int("3")
            max_n = int("3")

            allowed_extension_tuple = tuple(FILE_EXTENSIONS['images'])
        else:
            d_working = ensure_value_completed_2025_10_12_0000(key_name='d_working', options=[str(D_PK_WORKING), os.getcwd(), d_pk_root, D_DOWNLOADS, D_DOWNLOADED_FROM_TORRENT])
            token_splitter_pattern = ensure_value_completed_2025_10_12_0000(key_name='token_splitter_pattern', options=[
                r"\s+",  # 공백 기준으로 나눔
                r"[_]",  # 언더바(_) 기준으로 나눔
                r"[-]",  # 하이픈(-) 기준으로 나눔
                r"[ _\-]+",  # 공백, 언더바(_), 하이픈(-) 중 하나 이상이 연속되면 분리
                r"[ _\-]+",  # 공백, 언더바, 하이픈
                r"[\[\]_\\-]+",  # 대괄호([, ]), 언더바(_), 하이픈(-) 중 하나 이상 기준 (기호까지 포함)
                r"[\W_]+",  # 영문자/숫자 외 모든 문자(기호 포함) 및 언더바(_) 기준으로 분리
                r"\.",  # 마침표(.) 기준으로 분리 (확장자나 버전 구분에 유용)
            ])
            min_support = int(ensure_value_completed_2025_10_12_0000(key_name='min_support', options=["2", "3", "4", "5"]))  # 3 추천
            max_n = int(ensure_value_completed_2025_10_12_0000(key_name='max_n', options=["2", "3", "4", "5", "6", "7", "8", "9", "10"]))  # 3 or 10 추천
            allowed_extension_tuple = get_tuple_from_set(get_extensions_from_d(d_working))

        files_to_organize = [
            p for p in Path(d_working).iterdir()
            if p.is_file() and (  # 파일만 포함, 디렉토리 제외
                    allowed_extension_tuple is None or  # 확장자 제한이 없으면 모든 파일
                    p.suffix.lower() in allowed_extension_tuple  # 확장자 제한이 있으면 해당 확장자만
            )
        ]
        if not files_to_organize:
            logging.debug("대상 파일이 없습니다.")
            sys.exit()
        while 1:
            ensure_target_files_classified_by_ngram(d_working, token_splitter_pattern, min_support, max_n, files_to_organize)


    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
