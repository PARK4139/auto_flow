import logging
import os
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, Tuple

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def _get_video_id_from_filename(filename: str) -> str | None:
    """Extracts video ID from filename like '... [video_id].mp4'"""
    match = re.search(r'\[([a-zA-Z0-9_\\-]+)\]\.', filename)
    return match.group(1) if match else None

def _get_source_duration(video_id: str) -> float | None:
    """Gets original video duration in seconds using yt-dlp."""
    if not video_id: return None
    try:
        # Assuming youtube video for simplicity, this can be expanded
        url = f"https://www.youtube.com/watch?v={video_id}"
        cmd = ['yt-dlp', '--get-duration', url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        duration_str = result.stdout.strip()
        parts = [float(p) for p in duration_str.split(':')]
        duration_sec = sum(p * (60 ** i) for i, p in enumerate(reversed(parts)))
        return duration_sec
    except Exception as e:
        logging.warning(f"원본 영상({video_id})의 재생 시간을 가져오는 데 실패했습니다: {e}")
        return None

def _get_local_file_info(video_path: Path) -> Tuple[bool, float | None]:
    """Gets local file duration if valid, returns (is_valid, duration_in_seconds)."""
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        metadata = json.loads(result.stdout)
        if 'streams' in metadata and len(metadata['streams']) > 0:
            duration_sec = float(metadata['format']['duration'])
            return True, duration_sec
        return False, None
    except FileNotFoundError:
        logging.error("'ffprobe'를 찾을 수 없습니다. FFmpeg가 설치되어 있고 PATH에 등록되어 있는지 확인해주세요.")
        return False, None
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
        logging.error(f"{video_path.name} 파일을 분석하는 중 오류 발생: {e}")
        return False, None

def _group_files_by_base_name(directory: Path) -> Dict[str, dict]:
    # (Unchanged from previous version)
    all_files = list(directory.iterdir())
    main_files = []
    junk_files = []
    junk_suffixes = ('.ytdl', '.part')
    for p in all_files:
        if not p.is_file(): continue
        if p.name.endswith(junk_suffixes) or '.part-Frag' in p.name:
            junk_files.append(p)
        else:
            main_files.append(p)
    main_file_map = {mf.name: mf for mf in main_files}
    final_groups = {mf.name: {'main': mf, 'junk': []} for mf in main_files}
    for jf in junk_files:
        possible_main_name = jf.name
        if '.part-Frag' in possible_main_name:
            possible_main_name = possible_main_name.split('.part-Frag')[0]
        for suffix in junk_suffixes:
            if possible_main_name.endswith(suffix):
                possible_main_name = possible_main_name[:-len(suffix)]
        if possible_main_name in main_file_map:
            final_groups[possible_main_name]['junk'].append(jf)
        else:
            logging.debug(f"임시 파일에 대한 메인 파일을 찾을 수 없습니다: {jf.name}")
    return final_groups

def ensure_downloaded_videos_validated(d_working: str):
    """
    Validates videos sequentially, and asks for play/cleanup for each file.
    """
    d_working = Path(d_working)
    if not d_working.is_dir():
        logging.error(f"제공된 디렉토리를 찾을 수 없습니다: {d_working}")
        return

    logging.info(f"'{d_working}' 디렉토리에서 순차적 파일 검증 및 처리를 시작합니다.")
    file_groups = _group_files_by_base_name(d_working)

    for base_name, group in sorted(file_groups.items()):
        main_file = group.get('main')
        if not main_file: continue

        logging.info(f"---\n[처리 시작] {main_file.name}")

        # n. Advanced Validation
        is_valid, local_duration = _get_local_file_info(main_file)
        if not is_valid:
            logging.warning(f"[기본 검증 실패] 파일을 읽을 수 없거나 손상되었습니다.")
            continue

        video_id = _get_video_id_from_filename(main_file.name)
        source_duration = _get_source_duration(video_id)

        if source_duration and local_duration:
            duration_diff = abs(source_duration - local_duration)
            if duration_diff > 2:  # 2-second tolerance
                logging.warning(f"[검증 실패] 재생 시간 불일치. 원본: {source_duration:.2f}s, 로컬: {local_duration:.2f}s")
                continue
            logging.info(f"[검증 성공] 재생 시간 일치 (원본: {source_duration:.2f}s, 로컬: {local_duration:.2f}s)")
        else:
            logging.info("[기본 검증 성공] 재생 시간 비교는 건너뛰었습니다.")

        # n. Ask to Play
        play_choice = ensure_value_completed_2025_10_12_0000(
            key_name=f"'{main_file.name}' 파일을 재생하시겠습니까?",
            options=["재생", "건너뛰기"]
        )
        if play_choice == "재생":
            try:
                from pk_internal_tools.pk_objects.pk_losslesscut import PkLosslesscut
                from pk_internal_tools.pk_objects.pk_system_operation_options import PlayerSelectionMode, SetupOpsForEnsureValueCompleted20251130
                from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30
                from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

                func_n = get_caller_name()
                selection_mode_options = [member.value.lower() for member in PlayerSelectionMode]
                selected_mode_str = ensure_value_completed_2025_11_30(
                    key_name="player_selection_mode_for_validation",
                    func_n=func_n,
                    guide_text="검증된 파일 재생 모드를 선택하세요:",
                    options=selection_mode_options,
                    sort_order=SetupOpsForEnsureValueCompleted20251130.HISTORY
                )
                selected_selection_mode = PlayerSelectionMode[selected_mode_str.upper()] if selected_mode_str else PlayerSelectionMode.AUTO
                
                player = PkLosslesscut(selection_mode=selected_selection_mode)
                logging.info(f"'{main_file.name}' 파일을 재생합니다...")
                player.ensure_target_file_loaded(main_file)
            except Exception as e:
                logging.error(f"파일 재생 중 오류가 발생했습니다: {e}")

        # 3. Ask to Cleanup
        if group['junk']:
            logging.info("다음 임시 파일들을 찾았습니다:")
            for junk_file in group['junk']:
                logging.info(f"[삭제 대상] {junk_file.name}")
            
            cleanup_choice = ensure_value_completed_2025_10_12_0000(
                key_name="관련 임시파일을 삭제하시겠습니까?",
                options=["삭제", "건너뛰기"]
            )
            if cleanup_choice == "삭제":
                for junk_file in group['junk']:
                    try:
                        os.remove(junk_file)
                        logging.info("[삭제됨] {junk_file.name}")
                    except OSError as e:
                        logging.error(f"파일 삭제 실패: {junk_file.name}, 오류: {e}")
                        
    logging.info("모든 파일 처리를 완료했습니다.")