from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_routine_benchmark_executed():
    # 순환 import 문제를 해결하기 위해 지연 import 사용
    import inspect

    import logging

    from pk_internal_tools.pk_functions.ensure_cmd_exe_killed import ensure_cmd_exe_killed_v3
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
    from pk_internal_tools.pk_functions.export_benchmark_data import export_benchmark_data
    from pk_internal_tools.pk_functions.get_all_benchmarked_functions import get_all_benchmarked_functions
    from pk_internal_tools.pk_functions.get_benchmark_samples import get_benchmark_samples
    from pk_internal_tools.pk_functions.ensure_cmd_exe_killed import ensure_cmd_exe_killed_v1, ensure_cmd_exe_killed_v2

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 데모 실행
    logging.debug("[데모] 샘플링 벤치마크 데코레이터 데모")
    logging.debug(PK_UNDERLINE)

    # 함수들 실행
    logging.debug("테스트 함수들을 실행합니다...")
    for i in range(5):
        logging.debug(f"실행 {i + 1}/5...")
        ensure_cmd_exe_killed_v1()
        ensure_cmd_exe_killed_v2()
        ensure_cmd_exe_killed_v3()

    # 결과 확인
    logging.debug(f"[함수] 벤치마크된 함수들: {get_all_benchmarked_functions()}")

    for func_name in get_all_benchmarked_functions():
        samples = get_benchmark_samples(func_name)
        logging.debug(f"[결과] {func_name}: {len(samples)}개 샘플")
        if samples:
            times = [s['execution_time'] for s in samples]
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            logging.debug(f"평균: {avg_time:.6f}초, 최소: {min_time:.6f}초, 최대: {max_time:.6f}초")

    # 데이터 내보내기
    export_benchmark_data(f"{func_n}.json")
