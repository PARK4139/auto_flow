import uuid
import urllib
import platform
import os.path
import functools
import chardet
from zipfile import BadZipFile
from selenium.webdriver.chrome.options import Options
from pk_internal_tools.pk_functions.get_d_working import get_d_working

from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from PIL import Image
from moviepy import VideoFileClip
import logging

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def dynamic_image_download(thumbnail_urls, dst: str, channel_name: str, retry_limit: int = 3, delay: int = 1):
    import os
    import tqdm
    import requests
    os.makedirs(dst, exist_ok=True)
    try:
        if not thumbnail_urls:
            print(f"No thumbnails found.")
            return

        print(f"Collected {len(thumbnail_urls)} thumbnails.")

        # 프로그래스 바 설정
        with tqdm(total=len(thumbnail_urls), desc="Downloading Thumbnails", unit="file") as pbar:
            for index, url in enumerate(thumbnail_urls, start=1):
                retries = 0
                success = False

                while retries < retry_limit and not success:
                    try:
                        # 이미지 요청
                        response = requests.get(url, stream=True, timeout=10)
                        response.raise_for_status()

                        # 저장 f 경로 설정
                        f = os.path.join(dst, f"{channel_name}_thumbnail_{index}.jpg")

                        # 이미지 저장
                        with open(file=f, mode="wb") as file:
                            for chunk in response.iter_content(1024):
                                file.write(chunk)

                        # f 검증
                        from PIL import Image, ImageFont, ImageDraw, ImageFilter
                        with Image.open(f) as img:
                            img.verify()

                        if os.path.getsize(f) > 0:
                            print(f"Downloaded: {f}")
                            success = True
                        else:
                            print(f"Failed: {f} (File is empty or does not exist)")

                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            print(f"404 Not Found: {url}")
                            break  # 404 에러는 재시도하지 않음
                        else:
                            print(f"HTTP Error {e.response.status_code}: {url}")
                    except Exception as e:
                        print(f"Error downloading {url}: {str(e)}")

                    retries += 1
                    if not success and retries < retry_limit:
                        print(f"Retrying ({retries}/{retry_limit}) for {url}")
                        ensure_slept(seconds=delay)  # 지연 시간 추가

                # 진행 상황 업데이트
                pbar.update(1)

                # 모든 재시도가 실패한 경우 로그 출력
                if not success:
                    print(f"Failed to download after {retry_limit} attempts: {url}")

    except Exception as e:
        print(f"Error during Selenium image collection or download: {e}")
