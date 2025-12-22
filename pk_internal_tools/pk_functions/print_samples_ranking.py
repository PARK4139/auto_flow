from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def _log_benchmark_ranking():
    import logging
    import logging
    from pk_internal_tools.pk_functions.get_all_benchmarked_functions import get_all_benchmarked_functions
    from pk_internal_tools.pk_functions.get_benchmark_samples import get_benchmark_samples
    logging.debug("[순위] 성능 순위 (빠른 순)")
    logging.debug("=" * 60)

    all_functions = get_all_benchmarked_functions()
    if not all_functions:
        logging.debug("[오류] 순위를 매길 결과가 없습니다.")
        return

    # 함수별 평균 시간 계산
    function_times = []
    for func_name in all_functions:
        samples = get_benchmark_samples(func_name)
        if samples:
            avg_time = sum(s['execution_time'] for s in samples) / len(samples)
            function_times.append((func_name, avg_time))

    # 시간 순으로 정렬
    function_times.sort(key=lambda x: x[1])

    # 순위 출력
    for i, (func_name, avg_time) in enumerate(function_times):
        rank = i + 1
        if rank == 1:
            logging.debug(f"{rank}위: {func_name} ({avg_time:.6f}초)")
        elif rank == 2:
            logging.debug(f"{rank}위: {func_name} ({avg_time:.6f}초)")
        elif rank == 3:
            logging.debug(f"{rank}위: {func_name} ({avg_time:.6f}초)")
        else:
            logging.debug(f"{rank}위: {func_name} ({avg_time:.6f}초)")
