from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def _analyze_benchmark_result():
    import logging
    import logging
    from pk_internal_tools.pk_functions.get_all_benchmarked_functions import get_all_benchmarked_functions
    from pk_internal_tools.pk_functions.get_benchmark_samples import get_benchmark_samples
    logging.debug("[분석] 성능 결과 분석")
    logging.debug("=" * 60)

    # 전체 결과 가져오기
    all_functions = get_all_benchmarked_functions()

    if not all_functions:
        logging.debug("[오류] 분석할 결과가 없습니다.")
        return

    logging.debug(f"[통계] 총 {len(all_functions)}개 함수가 벤치마크되었습니다.")

    # 각 함수의 성능 통계
    for func_name in all_functions:
        samples = get_benchmark_samples(func_name)
        if samples:
            times = [s['execution_time'] for s in samples]
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            logging.debug(f"[함수] {func_name}:")
            logging.debug(f"평균: {avg_time:.6f}초")
            logging.debug(f"최소: {min_time:.6f}초")
            logging.debug(f"최대: {max_time:.6f}초")
            logging.debug(f"샘플: {len(samples)}개")
