from pk_internal_tools.pk_functions.is_f import is_f


def collect_f_list_recursive(d_working):
    import os
    results = []
    for dirpath, _, filenames in os.walk(d_working):
        for fname in filenames:
            full_path = os.path.join(dirpath, fname)  # ← 전체 경로 생성
            if is_f(full_path):  # ← 전체 경로를 넘김
                results.append(full_path)
    return results
