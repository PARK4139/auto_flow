def get_categorized_f_dict_by_priority_ngrams(f_list, min_support, max_n, token_splitter_pattern):
    from pk_internal_tools.pk_functions.get_all_ngram_list import get_all_ngram_list
    from pk_internal_tools.pk_functions.is_valid_ngram import is_valid_ngram
    from collections import defaultdict, Counter
    ngram_counter = Counter()
    all_ngram_set = {}

    for f in f_list:
        all_ngram_list = get_all_ngram_list(f, max_n, token_splitter_pattern)
        all_ngram_set[f] = all_ngram_list
        ngram_counter.update(all_ngram_list)

    sorted_keywords = sorted(
        [k for k, v in ngram_counter.items() if v >= min_support and is_valid_ngram(k)],
        key=lambda x: -len(x.split())
    )

    categorized = defaultdict(list)
    assigned_files = set()

    for keyword in sorted_keywords:
        for f in f_list:
            if f in assigned_files:
                continue
            if keyword in all_ngram_set[f]:
                categorized[keyword].append(f)
                assigned_files.add(f)

    for f in f_list:
        if f not in assigned_files:
            categorized["기타"].append(f)
    return dict(categorized)
