from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_benchmarker import sampls_benchmark_logger


@ensure_seconds_measured
def clear_benchmark_data():
    """모든 벤치마크 데이터를 초기화합니다."""
    try:
        if sampls_benchmark_logger.csv_log_file.exists():
            sampls_benchmark_logger.csv_log_file.unlink()
            print("[삭제] CSV 로그 파일이 삭제되었습니다.")
        else:
            print("[정보] CSV 로그 파일이 이미 존재하지 않습니다.")

        if sampls_benchmark_logger.metadata_file.exists():
            sampls_benchmark_logger.metadata_file.unlink()
            print("[삭제] 메타데이터 파일이 삭제되었습니다.")
        else:
            print("[정보] 메타데이터 파일이 이미 존재하지 않습니다.")

        sampls_benchmark_logger.metadata = {}
        print("[초기화] 벤치마크 데이터가 초기화되었습니다.")

        # CSV 헤더 재생성
        sampls_benchmark_logger._ensure_csv_header()
        print("[재생성] CSV 헤더가 재생성되었습니다.")

    except Exception as e:
        print(f"[오류] 벤치마크 데이터 초기화 실패: {e}")
        # 오류 발생 시 강제로 초기화
        try:
            sampls_benchmark_logger.metadata = {}
            if sampls_benchmark_logger.csv_log_file.exists():
                sampls_benchmark_logger.csv_log_file.unlink()
            if sampls_benchmark_logger.metadata_file.exists():
                sampls_benchmark_logger.metadata_file.unlink()
            sampls_benchmark_logger._ensure_csv_header()
            print("[강제 초기화] 벤치마크 데이터가 강제로 초기화되었습니다.")
        except Exception as e2:
            print(f"[치명적 오류] 강제 초기화도 실패: {e2}")
