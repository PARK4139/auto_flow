import inspect
import os
from collections import defaultdict, Counter
from pathlib import Path

import logging

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.ensure_modules_saved_from_file import ensure_modules_saved_from_file
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_modules_from_file import get_modules_from_file
from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools, d_pk_root_hidden
from pk_internal_tools.pk_wrappers.pk_ensure_modules_imported_proper import collect_import_lines_from_dir



@ensure_seconds_measured
def ensure_all_import_script_printed(target_directory=None, show_statistics=True, group_by_type=True, save_to_file=True):
    """
    프로젝트 내의 모든 Python 파일에서 import 문들을 스캔하여 출력하는 함수
    기존 함수들을 활용하여 개선된 버전
    
    Args:
        target_directory: 스캔할 디렉토리 경로 (None이면 pk_external_tools 디렉토리)
        show_statistics: 통계 정보 출력 여부
        group_by_type: import 유형별로 그룹화하여 출력할지 여부  
        save_to_file: 결과를 파일로 저장할지 여부
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 기본 디렉토리 설정 - 기존 패턴 활용
    if target_directory is None:
        target_directory = d_pk_external_tools
    else:
        target_directory = Path(target_directory)

    logging.debug(f"[{PkTexts.IMPORT_SCRIPT_START}] {PK_ANSI_COLOR_MAP['CYAN']}함수명={func_n} {PK_ANSI_COLOR_MAP['RESET']}")
    logging.debug(f"스캔 디렉토리: {target_directory}")

    # 모드 선택 - 기존 패턴 활용
    if QC_MODE:
        decision = "directory_scan_mode"
    else:
        decision = ensure_value_completed_2025_10_12_0000(
            key_name=f"{PkTexts.MODE}=",
            options=["directory_scan_mode", "file_by_file_mode", "single_file_mode"]
        )

    all_imports = []
    import_by_file = defaultdict(list)

    if decision == "directory_scan_mode":
        # 기존 collect_import_lines_from_dir 함수 활용
        logging.debug("디렉토리 전체 스캔 모드")
        all_imports = collect_import_lines_from_dir(str(target_directory))

        # 파일별 세부 정보도 수집
        for py_file in Path(target_directory).rglob('*.py'):
            if should_skip_file(py_file):
                continue
            try:
                file_imports = get_modules_from_file(str(py_file))
                import_by_file[str(py_file)] = file_imports
            except Exception as e:
                logging.debug(f"[{PkTexts.IMPORT_FILE_READ_ERROR}] {PK_ANSI_COLOR_MAP['RED']}파일={py_file} 오류={str(e)} {PK_ANSI_COLOR_MAP['RESET']}")

    elif decision == "file_by_file_mode":
        # 각 파일을 개별적으로 처리 - 기존 패턴 활용
        logging.debug("파일별 개별 처리 모드")
        pnxs = get_pnxs_from_d_working(d_working=str(target_directory))

        for pnx in pnxs:
            if is_f(pnx) and pnx.endswith('.py'):
                if should_skip_file(Path(pnx)):
                    continue

                logging.debug(f"처리 중: {pnx}")
                try:
                    file_imports = get_modules_from_file(pnx)
                    import_by_file[pnx] = file_imports
                    all_imports.extend(file_imports)

                    if save_to_file:
                        # 개별 파일의 import를 저장 - 기존 함수 활용
                        save_file = ensure_modules_saved_from_file(pnx)
                        logging.debug(f"저장됨: {save_file}")

                except Exception as e:
                    logging.debug(f"[{PkTexts.IMPORT_FILE_PROCESS_ERROR}] {PK_ANSI_COLOR_MAP['RED']}파일={pnx} 오류={str(e)} {PK_ANSI_COLOR_MAP['RESET']}")

    elif decision == "single_file_mode":
        # 단일 파일 모드
        logging.debug("단일 파일 분석 모드")
        from pk_internal_tools.pk_functions.get_value_advanced_return_via_fzf_routine import get_value_advanced_return_via_fzf_routine
        from pk_internal_tools.pk_functions.get_file_id import get_file_id


        key_name = "target_file"
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        options = [str(target_directory)]
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options, editable=False)
        target_file = selected

        if is_f(target_file) and target_file.endswith('.py'):
            file_imports = get_modules_from_file(target_file)
            import_by_file[target_file] = file_imports
            all_imports = file_imports

            if save_to_file:
                save_file = ensure_modules_saved_from_file(target_file)
                ensure_pnx_opened_by_ext(save_file)

    # 통계 분석 및 분류
    standard_imports, third_party_imports, local_imports = classify_imports(all_imports)

    # 결과 출력
    print_analysis_results(
        all_imports, standard_imports, third_party_imports, local_imports,
        import_by_file, target_directory, show_statistics, group_by_type
    )

    # 전체 결과 파일로 저장
    if save_to_file and all_imports:
        save_all_imports_to_file(func_n, all_imports, standard_imports, third_party_imports, local_imports)

    logging.debug(f"[{PkTexts.IMPORT_SCRIPT_COMPLETE}] {PK_ANSI_COLOR_MAP['CYAN']}함수명={func_n} {PK_ANSI_COLOR_MAP['RESET']}")


def should_skip_file(py_file):
    """건너뛸 파일 판별"""
    skip_patterns = ['__pycache__', '.git', '.venv', 'venv', 'node_modules', '.pytest_cache']
    return any(pattern in str(py_file) for pattern in skip_patterns)


def classify_imports(all_imports):
    """import를 유형별로 분류"""
    standard_imports = set()
    third_party_imports = set()
    local_imports = set()

    # Python 표준 라이브러리 목록 확장
    standard_libs = {
        'os', 'sys', 'time', 'json', 'sqlite3', 'subprocess', 'threading', 'datetime',
        'random', 'math', 'hashlib', 'inspect', 'importlib', 're', 'string', 'pathlib',
        'collections', 'functools', 'itertools', 'base64', 'urllib', 'traceback',
        'pickle', 'csv', 'zipfile', 'shutil', 'tempfile', 'uuid', 'timeit', 'logging',
        'argparse', 'configparser', 'email', 'html', 'http', 'xml', 'socket', 'ssl',
        'asyncio', 'concurrent', 'multiprocessing', 'queue', 'weakref', 'copy',
        'operator', 'typing', 'enum', 'dataclasses', 'contextlib', 'abc'
    }

    for imp in all_imports:
        # 모듈명 추출 개선
        if imp.startswith('from '):
            # "from module import something" 형태
            parts = imp.split()
            if len(parts) >= 2:
                module_name = parts[1].split('.')[0]
            else:
                continue
        elif imp.startswith('import '):
            # "import module" 형태  
            parts = imp.split()
            if len(parts) >= 2:
                module_name = parts[1].split('.')[0].split(' as ')[0]
            else:
                continue
        else:
            continue

        # 분류
        if module_name.startswith('pk_external_tools') or module_name.startswith('.'):
            local_imports.add(imp)
        elif module_name in standard_libs:
            standard_imports.add(imp)
        else:
            third_party_imports.add(imp)

    return standard_imports, third_party_imports, local_imports


def print_analysis_results(all_imports, standard_imports, third_party_imports, local_imports,
                           import_by_file, target_directory, show_statistics, group_by_type):
    """분석 결과 출력"""
    logging.debug("=" * 80)
    logging.debug("전체 IMPORT 스크립트 분석 결과")
    logging.debug("=" * 80)

    if show_statistics:
        print_import_statistics(all_imports, standard_imports, third_party_imports, local_imports)

    if group_by_type:
        print_imports_by_type(standard_imports, third_party_imports, local_imports)
    else:
        print_all_imports_sorted(all_imports)

    # 파일별 import 정보 (요약) - 기존 패턴 활용
    if import_by_file:
        logging.debug("" + "=" * 80)
        logging.debug("파일별 IMPORT 개수 TOP 10")
        logging.debug("=" * 80)

        file_import_counts = [(len(imports), file) for file, imports in import_by_file.items()]
        file_import_counts.sort(reverse=True)

        for i, (count, file) in enumerate(file_import_counts[:10]):
            try:
                relative_path = Path(file).relative_to(target_directory)
                logging.debug(f"{i + 1:2d}. {count:3d}개 - {relative_path}")
            except ValueError:
                # relative_to 실패시 절대 경로 표시
                logging.debug(f"{i + 1:2d}. {count:3d}개 - {Path(file).name}")


def save_all_imports_to_file(func_n, all_imports, standard_imports, third_party_imports, local_imports):
    """전체 import 결과를 파일로 저장 - 기존 패턴 활용"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_config
    save_file = d_pk_config / f"{func_n}_full_analysis.txt"

    content_lines = []
    content_lines.append("=" * 80)
    content_lines.append(" 전체 IMPORT 스크립트 분석 결과")
    content_lines.append("=" * 80)
    content_lines.append("")

    # 통계 정보
    content_lines.append(f"전체 import 문 수: {len(all_imports):,}개")
    content_lines.append(f"고유 import 문 수: {len(set(all_imports)):,}개")
    content_lines.append(f"표준 라이브러리: {len(standard_imports):,}개")
    content_lines.append(f"서드파티 라이브러리: {len(third_party_imports):,}개")
    content_lines.append(f"로컬 모듈: {len(local_imports):,}개")
    content_lines.append("")

    # 유형별 분류
    if standard_imports:
        content_lines.append(f" 표준 라이브러리 ({len(standard_imports)}개)")
        content_lines.append("-" * 50)
        for imp in sorted(standard_imports):
            content_lines.append(f"  {imp}")
        content_lines.append("")

    if third_party_imports:
        content_lines.append(f" 서드파티 라이브러리 ({len(third_party_imports)}개)")
        content_lines.append("-" * 50)
        for imp in sorted(third_party_imports):
            content_lines.append(f"  {imp}")
        content_lines.append("")

    if local_imports:
        content_lines.append(f" 로컬 모듈 ({len(local_imports)}개)")
        content_lines.append("-" * 50)
        for imp in sorted(local_imports):
            content_lines.append(f"  {imp}")
        content_lines.append("")

    # 기존 함수 활용하여 파일 저장
    ensure_list_written_to_f(content_lines, save_file, mode="w")
    logging.debug(f"전체 분석 결과 저장: {save_file}")

    return save_file


def print_import_statistics(all_imports, standard_imports, third_party_imports, local_imports):
    """import 통계 정보 출력"""
    logging.debug(" IMPORT 통계")
    logging.debug("-" * 40)

    total_count = len(all_imports)
    unique_count = len(set(all_imports))

    logging.debug(f"전체 import 문 수: {total_count:,}개")
    logging.debug(f"고유 import 문 수: {unique_count:,}개")
    logging.debug(f"표준 라이브러리: {len(standard_imports):,}개")
    logging.debug(f"서드파티 라이브러리: {len(third_party_imports):,}개")
    logging.debug(f"로컬 모듈: {len(local_imports):,}개")

    # 가장 많이 사용된 import 문 TOP 10
    if all_imports:
        import_counter = Counter(all_imports)
        logging.debug(f" 가장 많이 사용된 IMPORT TOP 10")
        logging.debug("-" * 50)

        for i, (imp, count) in enumerate(import_counter.most_common(10)):
            logging.debug(f"{i + 1:2d}. {count:3d}회 - {imp}")


def print_imports_by_type(standard_imports, third_party_imports, local_imports):
    """import를 유형별로 분류하여 출력"""

    # 표준 라이브러리
    if standard_imports:
        logging.debug(f" 표준 라이브러리 ({len(standard_imports)}개)")
        logging.debug("-" * 50)
        for imp in sorted(standard_imports):
            logging.debug(f"{imp}")

    # 서드파티 라이브러리
    if third_party_imports:
        logging.debug(f" 서드파티 라이브러리 ({len(third_party_imports)}개)")
        logging.debug("-" * 50)
        for imp in sorted(third_party_imports):
            logging.debug(f"{imp}")

    # 로컬 모듈
    if local_imports:
        logging.debug(f" 로컬 모듈 ({len(local_imports)}개)")
        logging.debug("-" * 50)
        for imp in sorted(local_imports):
            logging.debug(f"{imp}")


def print_all_imports_sorted(all_imports):
    """모든 import를 정렬하여 출력"""
    unique_imports = sorted(set(all_imports))

    logging.info(PK_UNDERLINE)
    logging.info(f"전체 고유 IMPORT 목록 ({len(unique_imports)}개)")
    for imp in unique_imports:
        logging.info(f"{imp}")

