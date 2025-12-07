from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_benchmarker import sampls_benchmark_logger


@ensure_seconds_measured
def get_all_benchmarked_functions() -> list:
    """벤치마크된 모든 함수명을 반환합니다."""
    return sampls_benchmark_logger.get_all_functions()
