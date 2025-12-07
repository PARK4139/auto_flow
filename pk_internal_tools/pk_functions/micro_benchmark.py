

def micro_benchmark(repeat=5, title=None):
    import time
    import statistics
    from functools import wraps
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(repeat):
                start = time.perf_counter()
                func(*args, **kwargs)
                end = time.perf_counter()
                results.append(end - start)
            avg = statistics.mean(results)
            std = statistics.stdev(results) if repeat > 1 else 0.0
            label = f"[{title or func.__name__}]"
            print(f"{label} 평균: {avg:.6f}s (σ={std:.6f}) over {repeat}회")
            return results

        return wrapper

    return decorator
