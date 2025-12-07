from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def download_single_youtube_video(url, output_dir):
    """단일 비디오 다운로드"""
    import logging
    import traceback
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    try:

        # 메타데이터 추출
        try:
            from pk_internal_tools.pk_functions.ensure_youtube_videos_downloaded_v_2025_05_04_0000 import ensure_youtube_videos_downloaded_v_2025_05_04_0000
            metadata = ensure_youtube_videos_downloaded_v_2025_05_04_0000(url, output_dir, extract_only=True)

            if not metadata:
                logging.debug(f"[{PkTexts.METADATA_EXTRACTION_FAILED_SKIP}] {url}")
                return None

            title = metadata.get('title', 'unknown')
            clip_id = metadata.get('id', 'unknown')
            ext = metadata.get('ext', 'mp4')

            # 디버그 정보
            logging.debug(f"[{PkTexts.DEBUG_METADATA_EXT}] = '{ext}' (타입: {type(ext)})")
            logging.debug(f"title = '{title}'")
            logging.debug(f"clip_id = '{clip_id}'")

            # 출력 파일명 생성
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_filename = f"{safe_title}_{clip_id}.{ext}"
            output_path = output_dir / output_filename

            logging.debug(f"[{PkTexts.DEBUG_OUTPUT_FILENAME}] = '{output_filename}'")

            # 실제 다운로드
            logging.debug(f"ensure_youtube_videos_downloaded_v_2025_05_04_0000 호출 - ext='{ext}'")
            result = ensure_youtube_videos_downloaded_v_2025_05_04_0000(url, output_dir, output_filename=output_filename)

            if result and output_path.exists():
                # PotPlayer 플레이리스트에 추가 (함수가 정의되지 않았으므로 주석 처리)
                # try:
                #     ensure_pot_player_playlist_added(str(output_path))
                # except Exception as e:
                #     logging.debug(f"[{PkTexts.POTPLAYER_PLAYLIST_ADD_FAILED}] {e}")

                # 파일명 정규화 확인
                normalized_filename = output_path.nick_name
                logging.debug(f"정규화된 파일명 = '{normalized_filename}'")
                logging.debug(f"clip_id 검색 = '[{clip_id}]'")

                return {
                    'url': url,
                    'title': title,
                    'clip_id': clip_id,
                    'output_path': str(output_path),
                    'success': True
                }
            else:
                return {
                    'url': url,
                    'success': False,
                    'error': 'Download failed'
                }

        except Exception as e:
            logging.debug(f"[{PkTexts.EXCEPTION_OCCURRED}] {url}\n{traceback.format_exc()}")
            return {
                'url': url,
                'success': False,
                'error': str(e)
            }

    except Exception as e:
        logging.debug(f"[{PkTexts.EXCEPTION_OCCURRED}] {e}")
        return None
