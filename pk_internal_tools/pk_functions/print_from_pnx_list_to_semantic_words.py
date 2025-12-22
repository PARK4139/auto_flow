from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_from_pnx_list_to_semantic_words(pnx):
    import inspect
    import re
    from collections import Counter

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    txt_to_exclude_list = [
        F_DB_YAML,
        F_SUCCESS_LOG,
        F_LOCAL_PKG_CACHE_PRIVATE,
    ]

    # d_list, f_list=get_sub_pnxs_without_walking(pnx=item_pnx, txt_to_exclude_list=txt_to_exclude_list)
    d_list, f_list = get_sub_pnx_list(pnx=pnx, txt_to_exclude_list=txt_to_exclude_list)

    # pnxs=d_list
    pnxs = f_list

    # 수십개의 f 경로에서 2개 이상의 한글로 구성된 의미론적인 단어를 추출
    special_korean_words = []

    def extract_korean_words(pnx):
        pattern = r'[가-힣]{2,}'  # 한글만 추출하는 정규식
        korean_words = re.findall(pattern=pattern, string=pnx)  # 2개 이상 한글 문자로 이루어진 단어를 찾음
        return korean_words

    for item in pnxs:
        item_pnx = item[0]
        korean_words = extract_korean_words(item_pnx)
        special_korean_words = special_korean_words + korean_words
    word_count = Counter(special_korean_words)
    logging.debug(rf'''word_count="{word_count}"  ''')
