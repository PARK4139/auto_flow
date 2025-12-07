from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def export_benchmark_data(output_file: Optional[Path] = None) -> Path:

    import logging

    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs

    import json
    from datetime import datetime
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_all_benchmarked_functions import get_all_benchmarked_functions
    from pk_internal_tools.pk_functions.get_benchmark_samples import get_benchmark_samples
    from pk_internal_tools.pk_objects.pk_benchmarker import sampls_benchmark_logger

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(d_pk_logs) / f"benchmark_data_{timestamp}.json"
    else:
        # 문자열인 경우 Path 객체로 변환
        if isinstance(output_file, str):
            output_file = Path(output_file)

    # 디렉토리가 존재하지 않으면 생성
    output_file.parent.mkdir(exist_ok=True)

    all_data = {}
    for func_name in get_all_benchmarked_functions():
        samples = get_benchmark_samples(func_name)
        all_data[func_name] = {
            'samples': samples,
            'total_samples': len(samples),
            'metadata': sampls_benchmark_logger.metadata.get(func_name, {})
        }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    logging.debug(f"[저장] 벤치마크 데이터가 내보내졌습니다: {output_file}")
    return output_file
