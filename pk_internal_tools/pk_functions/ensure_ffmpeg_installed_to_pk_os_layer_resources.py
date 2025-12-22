from functools import lru_cache


@lru_cache(maxsize=1)
def ensure_ffmpeg_installed_to_pk_os_layer_resources():
    from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS

    import os
    import zipfile
    import urllib.request
    import shutil
    import traceback
    import logging

    ffmpeg_exe_path = os.path.join(D_PK_EXTERNAL_TOOLS, "ffmpeg.exe")
    ffprobe_exe_path = os.path.join(D_PK_EXTERNAL_TOOLS, "ffprobe.exe")

    # 둘 다 있으면 바로 반환
    if os.path.exists(ffmpeg_exe_path) and os.path.exists(ffprobe_exe_path):
        logging.debug(f"[FFMPEG]  ffmpeg.exe 및 ffprobe.exe 이미 설치됨")
        return ffmpeg_exe_path, ffprobe_exe_path

    # 설치 시작
    logging.debug(f"[FFMPEG]  설치 시작")
    os.makedirs(D_PK_EXTERNAL_TOOLS, exist_ok=True)

    try:
        zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        temp_zip = os.path.join(D_PK_EXTERNAL_TOOLS, "ffmpeg_temp.zip")
        extract_dir = os.path.join(D_PK_EXTERNAL_TOOLS, "extracted_ffmpeg")

        logging.debug(f"[FFMPEG]  다운로드 중: {zip_url}")
        urllib.request.urlretrieve(zip_url, temp_zip)
        logging.debug(f"[FFMPEG]  다운로드 완료: {temp_zip}")

        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        logging.debug(f"[FFMPEG]  압축 해제 완료: {extract_dir}")

        found = False
        for root, dirs, files in os.walk(extract_dir):
            if "ffmpeg.exe" in files and "ffprobe.exe" in files:
                shutil.copy2(os.path.join(root, "ffmpeg.exe"), ffmpeg_exe_path)
                shutil.copy2(os.path.join(root, "ffprobe.exe"), ffprobe_exe_path)
                logging.debug(f"[FFMPEG]  ffmpeg.exe, ffprobe.exe 복사 완료")
                found = True
                break

        os.remove(temp_zip)
        shutil.rmtree(extract_dir, ignore_errors=True)

        if not found:
            raise FileNotFoundError("ffmpeg.exe 또는 ffprobe.exe를 찾을 수 없습니다.")

        return ffmpeg_exe_path, ffprobe_exe_path

    except Exception as e:
        logging.debug(f"[FFMPEG]  설치 실패: {e}")
        traceback.print_exc()
        return None, None
