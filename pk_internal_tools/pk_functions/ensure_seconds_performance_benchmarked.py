from typing import Dict, Any, Optional


def ensure_seconds_performance_benchmarked(metadata: Optional[Dict[str, Any]] = None):
    from pk_internal_tools.pk_objects.pk_benchmarker import sampls_benchmark_logger
    import functools
    import time
    from typing import Callable

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 실행 시간 측정
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                # 성공적으로 실행된 경우만 로그에 기록
                sampls_benchmark_logger.log_execution(
                    function_name=func.__name__,
                    execution_time=execution_time,
                    sample_id=sampls_benchmark_logger.metadata.get(func.__name__, {}).get('total_samples', 0) + 1,
                    metadata=metadata
                )

                return result

            except Exception as e:
                # 오류 발생 시에도 시간 측정 (오류 처리 시간 포함)
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                error_metadata = metadata or {}
                error_metadata['error'] = str(e)
                error_metadata['error_type'] = type(e).__name__

                sampls_benchmark_logger.log_execution(
                    function_name=func.__name__,
                    execution_time=execution_time,
                    sample_id=sampls_benchmark_logger.metadata.get(func.__name__, {}).get('total_samples', 0) + 1,
                    metadata=error_metadata
                )

                # 원래 오류를 다시 발생시킴
                raise

        return wrapper

    return decorator
