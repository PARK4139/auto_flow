"""
고급 성능 비교를 위한 데코레이터와 벤치마크 시스템

이 모듈은 함수들의 성능을 비교하고 분석할 수 있는 고급 도구를 제공합니다.
- 반복 측정으로 정확한 성능 데이터 수집
- 통계 분석 (평균, 표준편차, 최소/최대값)
- 성능 비교 리포트 생성
- 다양한 측정 옵션 지원
"""

import functools
import json
import statistics
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable


@dataclass
class BenchmarkResult:
    """벤치마크 결과를 저장하는 데이터 클래스"""
    function_name: str
    total_runs: int
    total_time: float
    average_time: float
    min_time: float
    max_time: float
    std_deviation: float
    individual_times: List[float]
    timestamp: str
    metadata: Dict[str, Any]


class PerformanceBenchmark:
    """고급 성능 벤치마크 시스템"""

    def __init__(self, output_dir: Optional[Path] = None):
        from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
        self.results: Dict[str, BenchmarkResult] = {}
        self.output_dir = output_dir or d_pk_logs
        self.output_dir.mkdir(exist_ok=True)

    def benchmark(self,
                  iterations: int = 10,
                  warmup_runs: int = 3,
                  save_results: bool = True,
                  metadata: Optional[Dict[str, Any]] = None) -> Callable:
        """
        성능 벤치마크 데코레이터
        
        Args:
            iterations: 측정할 반복 횟수
            warmup_runs: 워밍업 실행 횟수
            save_results: 결과를 파일로 저장할지 여부
            metadata: 추가 메타데이터
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 워밍업 실행
                for _ in range(warmup_runs):
                    try:
                        func(*args, **kwargs)
                    except Exception:
                        pass  # 워밍업 중 오류는 무시

                # 실제 측정
                times = []
                for i in range(iterations):
                    start_time = time.perf_counter()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time.perf_counter()
                        execution_time = end_time - start_time
                        times.append(execution_time)
                    except Exception as e:
                        print(f"️ 함수 실행 중 오류 발생: {e}")
                        times.append(float('inf'))  # 오류 시 무한대 값

                # 결과 분석
                valid_times = [t for t in times if t != float('inf')]
                if not valid_times:
                    print(f" 모든 실행에서 오류가 발생했습니다: {func.__name__}")
                    return None

                benchmark_result = BenchmarkResult(
                    function_name=func.__name__,
                    total_runs=len(valid_times),
                    total_time=sum(valid_times),
                    average_time=statistics.mean(valid_times),
                    min_time=min(valid_times),
                    max_time=max(valid_times),
                    std_deviation=statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
                    individual_times=valid_times,
                    timestamp=datetime.now().isoformat(),
                    metadata=metadata or {}
                )

                self.results[func.__name__] = benchmark_result

                # 결과 출력
                self._print_result(benchmark_result)

                # 결과 저장
                if save_results:
                    self._save_results()

                # 원래 함수 결과 반환
                return result

            return wrapper

        return decorator

    def _print_result(self, result: BenchmarkResult):
        """벤치마크 결과를 출력합니다."""
        print(f"{'=' * 60}")
        print(f" 성능 벤치마크 결과: {result.function_name}")
        print(f"{'=' * 60}")
        print(f" 총 실행 횟수: {result.total_runs}")
        print(f"️  총 실행 시간: {result.total_time:.6f}초")
        print(f" 평균 실행 시간: {result.average_time:.6f}초")
        print(f" 최소 실행 시간: {result.min_time:.6f}초")
        print(f" 최대 실행 시간: {result.max_time:.6f}초")
        print(f" 표준편차: {result.std_deviation:.6f}초")

        if result.metadata:
            print(f" 메타데이터: {result.metadata}")
        print(f"{'=' * 60}\n")

    def _save_results(self):
        """벤치마크 결과를 파일로 저장합니다."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_benchmark_{timestamp}.json"
        filepath = self.output_dir / filename

        # JSON 직렬화 가능한 형태로 변환
        serializable_results = {}
        for func_name, result in self.results.items():
            serializable_results[func_name] = asdict(result)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)

        print(f" 벤치마크 결과가 저장되었습니다: {filepath}")

    def compare_functions(self, function_names: List[str]) -> Dict[str, Any]:
        """여러 함수의 성능을 비교합니다."""
        if not function_names:
            return {}

        comparison = {
            "timestamp": datetime.now().isoformat(),
            "functions": {},
            "ranking": [],
            "summary": {}
        }

        # 각 함수의 결과 수집
        for func_name in function_names:
            if func_name in self.results:
                result = self.results[func_name]
                comparison["functions"][func_name] = {
                    "average_time": result.average_time,
                    "min_time": result.min_time,
                    "max_time": result.max_time,
                    "std_deviation": result.std_deviation,
                    "total_runs": result.total_runs
                }

        # 성능 순위 결정 (평균 시간 기준)
        sorted_functions = sorted(
            comparison["functions"].items(),
            key=lambda x: x[1]["average_time"]
        )

        comparison["ranking"] = [
            {"rank": i + 1, "function": name, "avg_time": data["average_time"]}
            for i, (name, data) in enumerate(sorted_functions)
        ]

        # 요약 통계
        if comparison["functions"]:
            avg_times = [data["average_time"] for data in comparison["functions"].values()]
            comparison["summary"] = {
                "fastest_function": sorted_functions[0][0],
                "fastest_time": sorted_functions[0][1]["average_time"],
                "slowest_function": sorted_functions[-1][0],
                "slowest_time": sorted_functions[-1][1]["average_time"],
                "overall_average": statistics.mean(avg_times),
                "overall_std": statistics.stdev(avg_times) if len(avg_times) > 1 else 0
            }

        return comparison

    def print_comparison(self, function_names: List[str]):
        """함수들의 성능 비교 결과를 출력합니다."""
        comparison = self.compare_functions(function_names)

        if not comparison["functions"]:
            print(" 비교할 함수 결과가 없습니다.")
            return

        print(f"{'=' * 80}")
        print(f" 성능 비교 결과")
        print(f"{'=' * 80}")

        # 순위 출력
        print(" 성능 순위:")
        for rank_info in comparison["ranking"]:
            rank = rank_info["rank"]
            func_name = rank_info["function"]
            avg_time = rank_info["avg_time"]

            if rank == 1:
                print(f" {rank:2d}위: {func_name:<30} {avg_time:.6f}초")
            elif rank == 2:
                print(f" {rank:2d}위: {func_name:<30} {avg_time:.6f}초")
            elif rank == 3:
                print(f" {rank:2d}위: {func_name:<30} {avg_time:.6f}초")
            else:
                print(f"   {rank:2d}위: {func_name:<30} {avg_time:.6f}초")

        # 요약 통계
        summary = comparison["summary"]
        print(f"\n 요약 통계:")
        print(f"    가장 빠른 함수: {summary['fastest_function']} ({summary['fastest_time']:.6f}초)")
        print(f"    가장 느린 함수: {summary['slowest_function']} ({summary['slowest_time']:.6f}초)")
        print(f"    전체 평균: {summary['overall_average']:.6f}초")
        print(f"    전체 표준편차: {summary['overall_std']:.6f}초")

        # 성능 차이 분석
        if len(comparison["functions"]) > 1:
            fastest = summary['fastest_time']
            slowest = summary['slowest_time']
            ratio = slowest / fastest if fastest > 0 else 0
            print(f"    성능 차이: 가장 느린 함수가 가장 빠른 함수보다 {ratio:.2f}배 느림")

        print(f"{'=' * 80}\n")

    def export_report(self, filename: Optional[str] = None) -> Path:
        """상세한 벤치마크 리포트를 생성합니다."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.md"

        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# 성능 벤치마크 리포트\n\n")
            f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            if not self.results:
                f.write("## 결과 없음\n\n")
                f.write("아직 벤치마크가 실행되지 않았습니다.\n")
                return filepath

            # 전체 요약
            f.write("## 전체 요약\n\n")
            total_functions = len(self.results)
            total_runs = sum(r.total_runs for r in self.results.values())
            total_time = sum(r.total_time for r in self.results.values())

            f.write(f"- 벤치마크된 함수 수: {total_functions}\n")
            f.write(f"- 총 실행 횟수: {total_runs}\n")
            f.write(f"- 총 소요 시간: {total_time:.6f}초\n\n")

            # 각 함수별 상세 결과
            f.write("## 함수별 상세 결과\n\n")
            for func_name, result in self.results.items():
                f.write(f"### {func_name}\n\n")
                f.write(f"- 총 실행 횟수: {result.total_runs}\n")
                f.write(f"- 총 실행 시간: {result.total_time:.6f}초\n")
                f.write(f"- 평균 실행 시간: {result.average_time:.6f}초\n")
                f.write(f"- 최소 실행 시간: {result.min_time:.6f}초\n")
                f.write(f"- 최대 실행 시간: {result.max_time:.6f}초\n")
                f.write(f"- 표준편차: {result.std_deviation:.6f}초\n")

                if result.metadata:
                    f.write(f"- 메타데이터: {json.dumps(result.metadata, ensure_ascii=False, indent=2)}\n")

                f.write("\n")

            # 성능 순위
            all_function_names = list(self.results.keys())
            comparison = self.compare_functions(all_function_names)

            if comparison["ranking"]:
                f.write("## 성능 순위\n\n")
                f.write("| 순위 | 함수명 | 평균 실행 시간 |\n")
                f.write("|------|--------|----------------|\n")

                for rank_info in comparison["ranking"]:
                    rank = rank_info["rank"]
                    func_name = rank_info["function"]
                    avg_time = rank_info["avg_time"]
                    f.write(f"| {rank} | {func_name} | {avg_time:.6f}초 |\n")

                f.write("\n")

        print(f" 상세 리포트가 생성되었습니다: {filepath}")
        return filepath


# 전역 벤치마크 인스턴스
_benchmark = PerformanceBenchmark()


def ensure_performance_benchmark(iterations: int = 10,
                                 warmup_runs: int = 3,
                                 save_results: bool = True,
                                 metadata: Optional[Dict[str, Any]] = None):
    """
    성능 벤치마크 데코레이터 (간편 사용)
    
    사용 예시:
    @ensure_performance_benchmark(iterations=20, warmup_runs=5)
    def my_function():
        # 함수 내용
        pass
    """
    return _benchmark.benchmark(
        iterations=iterations,
        warmup_runs=warmup_runs,
        save_results=save_results,
        metadata=metadata
    )


def print_benchmark_comparison(function_names: List[str]):
    """벤치마크된 함수들의 성능을 비교하여 출력합니다."""
    _benchmark.print_comparison(function_names)


def export_benchmark_report(filename: Optional[str] = None) -> Path:
    """벤치마크 리포트를 파일로 내보냅니다."""
    return _benchmark.export_report(filename)


def get_benchmark_results() -> Dict[str, BenchmarkResult]:
    """현재까지의 벤치마크 결과를 반환합니다."""
    return _benchmark.results.copy()


if __name__ == "__main__":
    # 데모 실행
    print(" 성능 벤치마크 시스템 데모")
    print(PK_UNDERLINE)


    # 테스트 함수들
    @ensure_performance_benchmark(iterations=5, warmup_runs=2)
    def fast_function():
        """빠른 함수"""
        time.sleep(0.01)
        return "fast"


    @ensure_performance_benchmark(iterations=5, warmup_runs=2)
    def medium_function():
        """중간 속도 함수"""
        time.sleep(0.05)
        return "medium"


    @ensure_performance_benchmark(iterations=5, warmup_runs=2)
    def slow_function():
        """느린 함수"""
        time.sleep(0.1)
        return "slow"


    # 함수들 실행
    print("테스트 함수들을 실행합니다...")
    fast_function()
    medium_function()
    slow_function()

    # 성능 비교
    print_benchmark_comparison(["fast_function", "medium_function", "slow_function"])

    # 리포트 생성
    export_benchmark_report("demo_report.md")
