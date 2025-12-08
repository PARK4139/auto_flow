import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import logging


class SampleBenchmarkLogger:
    def __init__(self, log_dir: Optional[Path] = None):
        from pathlib import Path

        from pk_internal_tools.pk_objects.pk_directories import d_pk_logs

        self.log_dir = log_dir or Path(d_pk_logs)
        self.log_dir.mkdir(exist_ok=True)

        # CSV 로그 파일 경로
        self.csv_log_file = self.log_dir / "sample_benchmark_log.csv"
        self._ensure_csv_header()

        # JSON 메타데이터 파일 경로
        self.metadata_file = self.log_dir / "sample_benchmark_metadata.json"
        self._load_metadata()

    def _ensure_csv_header(self):
        """CSV 파일에 헤더가 없으면 추가합니다."""
        try:
            if not self.csv_log_file.exists():
                logging.debug(f"[디버그] CSV 파일을 새로 생성합니다: {self.csv_log_file}")
                with open(self.csv_log_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'timestamp',
                        'function_name',
                        'execution_time',
                        'sample_id',
                        'metadata'
                    ])
                logging.debug(f"[디버그] CSV 헤더가 생성되었습니다")
            else:
                # 기존 파일이 있으면 헤더 확인
                with open(self.csv_log_file, 'r', newline='', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if not first_line or not first_line.startswith('timestamp,function_name'):
                        logging.debug(f"[디버그] 기존 CSV 파일에 올바른 헤더가 없습니다. 재생성합니다.")
                        # 백업 파일 생성
                        backup_file = self.csv_log_file.with_suffix('.csv.backup')
                        import shutil
                        shutil.copy2(self.csv_log_file, backup_file)
                        logging.debug(f"[디버그] 기존 파일을 백업했습니다: {backup_file}")

                        # 새로 생성
                        with open(self.csv_log_file, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                'timestamp',
                                'function_name',
                                'execution_time',
                                'sample_id',
                                'metadata'
                            ])
                        logging.debug(f"[디버그] CSV 헤더가 재생성되었습니다")
                    else:
                        logging.debug(f"[디버그] 기존 CSV 파일에 올바른 헤더가 있습니다")
        except Exception as e:
            logging.error("CSV 헤더 생성 실패: {e}")
            # 오류 발생 시 파일 삭제 후 재시도
            try:
                if self.csv_log_file.exists():
                    self.csv_log_file.unlink()
                with open(self.csv_log_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'timestamp',
                        'function_name',
                        'execution_time',
                        'sample_id',
                        'metadata'
                    ])
                logging.debug(f"[복구] CSV 헤더가 복구되었습니다")
            except Exception as e2:
                logging.debug(f"[치명적 오류] CSV 헤더 복구 실패: {e2}")

    def _load_metadata(self):
        """메타데이터 파일을 로드합니다."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except:
                self.metadata = {}
        else:
            self.metadata = {}

    def _save_metadata(self):
        """메타데이터를 파일에 저장합니다."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    def log_execution(self,
                      function_name: str,
                      execution_time: float,
                      sample_id: int,
                      metadata: Optional[Dict[str, Any]] = None):
        """함수 실행 결과를 로그에 기록합니다."""
        timestamp = datetime.now().isoformat()

        # CSV에 기록
        with open(self.csv_log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            metadata_str = json.dumps(metadata or {}, ensure_ascii=False) if metadata else ""
            writer.writerow([
                timestamp,
                function_name,
                f"{execution_time:.9f}",
                sample_id,
                metadata_str
            ])

        # 메타데이터 업데이트
        if function_name not in self.metadata:
            self.metadata[function_name] = {
                'first_seen': timestamp,
                'total_samples': 0,
                'last_metadata': metadata or {}
            }

        self.metadata[function_name]['total_samples'] += 1
        self.metadata[function_name]['last_seen'] = timestamp
        if metadata:
            self.metadata[function_name]['last_metadata'] = metadata

        self._save_metadata()

    def get_function_samples(self, function_name: str) -> list:
        """특정 함수의 모든 샘플을 가져옵니다."""
        samples = []

        if not self.csv_log_file.exists():
            logging.debug(f"[디버그] CSV 파일이 존재하지 않습니다: {self.csv_log_file}")
            return samples

        try:
            with open(self.csv_log_file, 'r', newline='', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logging.debug(f"[디버그] CSV 파일이 비어있습니다: {self.csv_log_file}")
                    return samples

                f.seek(0)  # 파일 포인터를 다시 처음으로
                reader = csv.DictReader(f)

                # 헤더 확인
                if not reader.fieldnames:
                    logging.debug(f"[디버그] CSV 헤더가 없습니다")
                    return samples

                for row in reader:
                    if 'function_name' in row and row['function_name'] == function_name:
                        try:
                            sample = {
                                'timestamp': row['timestamp'],
                                'execution_time': float(row['execution_time']),
                                'sample_id': int(row['sample_id']),
                                'metadata': json.loads(row['metadata']) if row['metadata'] else {}
                            }
                            samples.append(sample)
                        except (ValueError, json.JSONDecodeError) as e:
                            logging.debug(f"[디버그] 샘플 파싱 오류: {e}, 행: {row}")
                            continue
                    elif 'function_name' not in row:
                        logging.debug(f"[디버그] function_name 컬럼이 없는 행: {row}")

                return samples

        except Exception as e:
            logging.error("CSV 파일 읽기 실패: {e}")
            return samples

    def get_all_functions(self) -> list:
        """벤치마크된 모든 함수명을 가져옵니다."""
        if not self.csv_log_file.exists():
            logging.debug(f"[디버그] CSV 파일이 존재하지 않습니다: {self.csv_log_file}")
            return []

        try:
            with open(self.csv_log_file, 'r', newline='', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logging.debug(f"[디버그] CSV 파일이 비어있습니다: {self.csv_log_file}")
                    return []

                # 파일 내용의 처음 몇 줄을 확인
                lines = content.split('\n')
                logging.debug(f"[디버그] CSV 파일 첫 번째 줄: {lines[0] if lines else '빈 파일'}")

                f.seek(0)  # 파일 포인터를 다시 처음으로
                reader = csv.DictReader(f)

                # 헤더 확인
                if not reader.fieldnames:
                    logging.debug(f"[디버그] CSV 헤더가 없습니다")
                    return []

                logging.debug(f"[디버그] CSV 헤더: {reader.fieldnames}")

                functions = set()
                for row in reader:
                    if 'function_name' in row and row['function_name']:
                        functions.add(row['function_name'])
                    else:
                        logging.debug(f"[디버그] 잘못된 행: {row}")

                return sorted(list(functions))

        except Exception as e:
            logging.error("CSV 파일 읽기 실패: {e}")
            return []


sampls_benchmark_logger = SampleBenchmarkLogger()
