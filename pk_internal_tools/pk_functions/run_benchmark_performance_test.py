def run_benchmark_performance_test():
    """벤치마크 성능 테스트를 실행합니다."""
    import logging # 로깅 모듈을 함수 상단으로 이동

    # lazy import로 순환 import 문제 해결
    try:
        from pk_internal_tools.pk_functions.ensure_seconds_performance_benchmarked import (
            ensure_seconds_performance_benchmarked,
            get_benchmark_samples,
            get_all_benchmarked_functions,
            export_benchmark_data,
            clear_benchmark_data
        )
    except ImportError as e:
        logging.debug(f"벤치마크 모듈을 가져올 수 없습니다: {e}")
        return False

    logging.debug("벤치마크 성능 테스트 시작")

    try:
        # 간단한 벤치마크 테스트 실행
        logging.debug("시뮬레이션 테스트 실행 (5회)")

        # 시뮬레이션 함수들 정의 및 실행
        @ensure_seconds_performance_benchmarked(metadata={
            "category": "demo",
            "description": "빠른 함수",
            "method": "simulation_fast"
        })
        def fast_function():
            """빠른 함수"""
            import time
            time.sleep(0.001)  # 1ms
            return "fast"

        @ensure_seconds_performance_benchmarked(metadata={
            "category": "demo",
            "description": "느린 함수",
            "method": "simulation_slow"
        })
        def slow_function():
            """느린 함수"""
            import time
            time.sleep(0.1)  # 100ms
            return "slow"

        # 함수들 실행
        for i in range(5):
            logging.debug(f"실행 {i + 1}/5...")
            fast_function()
            slow_function()

        # 결과 분석
        logging.debug(" 벤치마크 결과 분석")
        all_functions = get_all_benchmarked_functions()

        if all_functions:
            logging.debug(f"총 {len(all_functions)}개 함수가 벤치마크되었습니다.")

            # 함수별 성능 통계 수집
            function_stats = []
            for func_name in all_functions:
                samples = get_benchmark_samples(func_name)
                if samples:
                    times = [s['execution_time'] for s in samples]
                    avg_time = sum(times) / len(times)
                    min_time = min(times)
                    max_time = max(times)

                    function_stats.append({
                        'name': func_name,
                        'avg_time': avg_time,
                        'min_time': min_time,
                        'max_time': max_time,
                        'samples': len(samples)
                    })

                    logging.debug(f"{func_name}:")
                    logging.debug(f"평균: {avg_time:.6f}초, 최소: {min_time:.6f}초, 최대: {max_time:.6f}초")
                    logging.debug(f"샘플 수: {len(samples)}")

            # 가장 빠른 함수 찾기
            if function_stats:
                fastest_function = min(function_stats, key=lambda x: x['avg_time'])
                logging.debug(f" 가장 빠른 함수: {fastest_function['name']}")
                logging.debug(f"평균 실행 시간: {fastest_function['avg_time']:.6f}초")

                # 로그 파일에 결과 기록
                try:
                    logger = logging.getLogger(__name__)
                    logger.info(f"벤치마크 완료 - 가장 빠른 함수: {fastest_function['name']} ({fastest_function['avg_time']:.6f}초)")

                    # 로그 파일 경로 출력 및 열기
                    for handler in logger.handlers:
                        if hasattr(handler, 'baseFilename'):
                            log_file_path = handler.baseFilename
                            logging.debug(f"로그 파일에 결과가 기록되었습니다: {log_file_path}")

                            # 로그 파일 자동 열기
                            try:
                                import os
                                if os.name == 'nt':  # Windows
                                    os.startfile(log_file_path)
                                    logging.debug("로그 파일이 자동으로 열렸습니다.")
                                else:  # Linux/macOS
                                    import subprocess
                                    subprocess.run(['xdg-open', log_file_path], check=False)
                                    logging.debug("로그 파일이 자동으로 열렸습니다.")
                            except Exception as e:
                                logging.debug(f"️ 로그 파일 자동 열기 실패: {e}")
                            break
                except Exception as e:
                    logging.debug(f"️ 로깅 실패: {e}")

            # 리포트 생성
            try:
                from pathlib import Path
                report_path = export_benchmark_data("routine_benchmark_samples_report.json")
                logging.debug(f"벤치마크 리포트 생성 완료: {report_path}")
            except Exception as e:
                logging.debug(f"️ 리포트 생성 실패: {e}")

            return True
        else:
            logging.debug("벤치마크 결과가 없습니다.")
            return False

    except Exception as e:
        logging.debug(f"벤치마크 테스트 실행 중 오류 발생: {e}")
        return False
