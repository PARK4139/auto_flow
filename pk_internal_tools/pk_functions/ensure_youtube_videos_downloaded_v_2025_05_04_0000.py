"""
YouTube 비디오 다운로드 함수 (yt-dlp v2)
"""

import os
import sys
import yt_dlp
import logging
from pk_internal_tools.pk_objects.pk_files import F_YOUTUBE_COOKIES_TXT
from pathlib import Path


def ensure_youtube_videos_downloaded_v_2025_05_04_0000(url, output_dir=None, output_filename=None, extract_only=False):
    """YouTube 비디오 다운로드 (v2) - 기본 옵션과 fallback 옵션 사용"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'YOUTUBE_COOKIES_SETUP_FAILED_CONTINUE': 'YouTube 쿠키 파일이 없습니다',
                'OPERATION_IN_PROGRESS': '작업 진행 중',
                'OPERATION_SUCCESS': '작업 성공',
                'OPERATION_FAILED': '작업 실패',
                'FALLBACK_NEEDED': 'Fallback 옵션으로 재시도'
            })()

        # YouTube 쿠키 확인
        from pk_internal_tools.pk_objects.pk_files import F_YOUTUBE_COOKIES_TXT
        if not Path(F_YOUTUBE_COOKIES_TXT).exists():
            logging.debug(f"[{PkTexts.YOUTUBE_COOKIES_SETUP_FAILED_CONTINUE}] {F_YOUTUBE_COOKIES_TXT}")

        # 기본 옵션으로 시도
        logging.debug(f"[{PkTexts.OPERATION_IN_PROGRESS}] 1단계: 기본 옵션으로 다운로드 시도")
        
        try:
            logging.debug(f"[{PkTexts.OPERATION_IN_PROGRESS}] 기본 옵션으로 다운로드 시작: {url}")
            result = download_with_basic_options(url, output_dir, output_filename, extract_only)
            if result:
                logging.debug(f"[{PkTexts.OPERATION_SUCCESS}] 기본 옵션으로 다운로드 성공")
                return result
            else:
                error_msg = "Unknown error in basic options"
                logging.debug(f"[{PkTexts.OPERATION_FAILED}] 기본 옵션 실패: {error_msg[:100]}")
        except Exception as e:
            error_msg = str(e)
            logging.debug(f"[{PkTexts.OPERATION_FAILED}] 기본 옵션 실패: {error_msg[:100]}")

        # Fallback 옵션으로 재시도
        logging.debug(f"[{PkTexts.FALLBACK_NEEDED}]")
        
        try:
            logging.debug(f"[{PkTexts.OPERATION_IN_PROGRESS}] Fallback 옵션으로 다운로드 시작: {url}")
            result = download_with_fallback_options(url, output_dir, output_filename, extract_only)
            if result:
                logging.debug(f"[{PkTexts.OPERATION_SUCCESS}] Fallback 옵션으로 다운로드 성공")
                return result
            else:
                logging.debug(f"[{PkTexts.OPERATION_FAILED}] Fallback 옵션도 실패: 알 수 없는 오류")
                return None
        except Exception as e2:
            logging.debug(f"[{PkTexts.OPERATION_FAILED}] Fallback 옵션도 실패: {str(e2)[:100]}")
            return None

    except Exception as e:
        logging.debug(f"[{PkTexts.OPERATION_FAILED}] Fallback 옵션으로 재시도하지 않음 (알 수 없는 오류)")
        return None
