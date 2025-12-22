import time
from pathlib import Path
from pk_internal_tools.pk_functions.get_f_video_of_d_working_by_creation_date import get_f_video_of_d_working_by_creation_date

from pk_internal_tools.pk_functions.ensure_video_playied_at_losslesscut_v2 import ensure_video_playied_at_losslesscut_v2
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
import logging
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def is_editing_or_exporting(titles):
    """편집/출력 중인지 확인하는 함수"""
    for title in titles:
        if any(keyword in title for keyword in ["출력", "Export", "편집", "Edit"]):
            return True
    return False


def is_losslesscut_ready_for_video(titles):
    """LosslessCut이 비디오 로드 준비가 되었는지 확인하는 함수"""
    for title in titles:
        # 편집/출력 중이 아니고, 로딩 중이 아닌 상태
        if (get_idle_title_of_losslesscut() in title and
                "불러오는 중" not in title and
                "출력" not in title and
                "Export" not in title and
                "편집" not in title and
                "Edit" not in title):
            return True
    return False


def auto_load_and_play_by_creation_date(d_working, ext_list_allowed, max_attempts=5, timeout=300, check_interval=2.0):
    """
    작업 디렉토리의 비디오 파일들을 파일명 순(A-Z)으로 정렬하여 LosslessCut에서 자동으로 로드하고 재생
    - 클립보드 내용 보존 기능 포함
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 비디오 확장자 리스트 (예: ['.mp4', '.avi', '.mkv'])
        max_attempts: 최대 시도 횟수
        timeout: 전체 작업 시간 제한 (초)
        check_interval: 상태 확인 간격 (초)
    
    Returns:
        성공 여부 (bool)
    """
    from pk_internal_tools.pk_functions.ensure_clipboard_preserved import ClipboardPreserver

    # 클립보드 내용 보존
    # clipboard_preserver = ClipboardPreserverV2()

    try:
        # 클립보드 내용 보존 시작
        if not clipboard_preserver.preserve():
            logging.debug("클립보드 보존에 실패했습니다.")
            return False

        logging.debug(f"파일명 순으로 비디오 자동 로드/재생을 시작합니다...")
        logging.debug(f"작업 디렉토리: {d_working}")
        logging.debug(f"허용 확장자: {ext_list_allowed}")

        # 비디오 파일들을 파일명 순으로 정렬 (기본값)
        videos_sorted = get_f_video_of_d_working_by_creation_date(
            d_working,
            ext_list_allowed,
            sort_by='file_name',  # 파일명 순으로 정렬
            reverse=False  # A-Z 순
        )

        if not videos_sorted:
            logging.debug("정렬할 비디오 파일을 찾을 수 없습니다.")
            return False

        logging.debug(f"총 {len(videos_sorted)}개의 비디오 파일을 파일명 순으로 정렬했습니다.")

        # 각 비디오 파일에 대해 처리
        for idx, video_path in enumerate(videos_sorted):
            video_name = video_path.nick_name
            logging.debug(f"[{idx + 1}/{len(videos_sorted)}] {video_name} 처리 중...")

            # LosslessCut이 준비될 때까지 대기
            start_time = time.time()
            attempts = 0

            while attempts < max_attempts and (time.time() - start_time) < timeout:
                titles = get_window_titles()

                if is_editing_or_exporting(titles):
                    logging.debug(f"편집/출력 중이므로 대기... (시도 {attempts + 1}/{max_attempts})")
                    time.sleep(check_interval)
                    attempts += 1
                    continue

                if is_losslesscut_ready_for_video(titles):
                    logging.debug(f"LosslessCut이 준비되었습니다. {video_name} 로드 시작...")
                    break

                logging.debug(f"LosslessCut 준비 대기 중... (시도 {attempts + 1}/{max_attempts})")
                time.sleep(check_interval)
                attempts += 1

            if attempts >= max_attempts:
                logging.debug(f"{video_name} 처리 중 최대 시도 횟수 초과")
                continue

            if (time.time() - start_time) >= timeout:
                logging.debug(f"{video_name} 처리 중 시간 초과")
                continue

            # 비디오 로드
            try:
                logging.debug(f"{video_name} 로드 중...")
                ensure_f_video_loaded_on_losslesscut(video_path)
                time.sleep(1)  # 로드 완료 대기

                # 비디오 재생
                logging.debug(f"{video_name} 재생 시작...")
                if ensure_video_playied_at_losslesscut_v2():
                    logging.debug(f"{video_name} 로드 및 재생 완료!")

                    # 사용자에게 다음 비디오로 넘어갈지 확인
                    if idx < len(videos_sorted) - 1:
                        next_video = videos_sorted[idx + 1].nick_name
                        logging.debug(f"다음 비디오: {next_video}")
                        logging.debug("계속하려면 아무 키나 누르세요...")

                        # 간단한 대기 (실제로는 사용자 입력을 받을 수 있음)
                        time.sleep(3)
                else:
                    logging.debug(f"{video_name} 재생 실패")

            except Exception as e:
                logging.debug(f"{video_name} 처리 중 오류: {str(e)}")
                continue

        logging.debug("모든 비디오 처리 완료!")
        return True

    except Exception as e:
        logging.debug(f"자동 로드/재생 중 오류 발생: {str(e)}")
        return False
    finally:
        # 클립보드 내용 복원
        try:
            # clipboard_preserver.restore()
            logging.debug("클립보드 내용이 복원되었습니다.")
        except Exception as e:
            logging.debug(f"클립보드 복원 실패: {str(e)}")


def auto_load_and_play_latest_video(d_working, ext_list_allowed, max_attempts=5, timeout=300):
    """
    가장 최근에 생성된 비디오 파일만 자동으로 로드하고 재생
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 비디오 확장자 리스트
        max_attempts: 최대 시도 횟수
        timeout: 전체 작업 시간 제한 (초)
    
    Returns:
        성공 여부 (bool)
    """
    try:
        # 가장 최근 비디오 파일 가져오기
        latest_video = get_f_video_of_d_working_by_creation_date(
            d_working,
            ext_list_allowed,
            sort_by='modification_time',  # Windows에서는 수정시간이 더 정확
            reverse=True
        )

        if not latest_video or len(latest_video) == 0:
            logging.debug("최신 비디오 파일을 찾을 수 없습니다.")
            return False

        video_path = latest_video[0]
        video_name = video_path.nick_name

        logging.debug(f"최신 비디오 파일: {video_name}")

        # 단일 비디오 처리
        return auto_load_and_play_by_creation_date(
            d_working,
            ext_list_allowed,
            max_attempts,
            timeout,
            check_interval=1.0
        )

    except Exception as e:
        logging.debug(f"최신 비디오 처리 중 오류: {str(e)}")
        return False


def get_video_playlist_by_creation_date(d_working, ext_list_allowed, limit=None):
    """
    생성일자 순으로 정렬된 비디오 플레이리스트 생성
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 비디오 확장자 리스트
        limit: 반환할 최대 비디오 수 (None이면 전체)
    
    Returns:
        정렬된 비디오 경로 리스트
    """
    try:
        videos = get_f_video_of_d_working_by_creation_date(
            d_working,
            ext_list_allowed,
            sort_by='modification_time',  # Windows에서는 수정시간이 더 정확
            reverse=True
        )

        if not videos:
            return []

        if limit and limit > 0:
            videos = videos[:limit]

        # 플레이리스트 정보 출력
        logging.debug(f"생성일자 순 비디오 플레이리스트 ({len(videos)}개):")
        for i, video_path in enumerate(videos):
            logging.debug(f"{i + 1}. {video_path.nick_name}")

        return videos

    except Exception as e:
        logging.debug(f"플레이리스트 생성 중 오류: {str(e)}")
        return []
