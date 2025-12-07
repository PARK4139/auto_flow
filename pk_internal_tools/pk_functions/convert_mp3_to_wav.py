#!/usr/bin/env python3
"""
MP3 파일들을 WAV로 변환하는 스크립트
"""

import os
import glob
from pydub import AudioSegment
import logging
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.ensure_ffmpeg_installed_to_pk_os_layer_resources import ensure_ffmpeg_installed_to_pk_os_layer_resources
from pathlib import Path

def convert_mp3_to_wav(mp3_file, output_dir=None):
    """MP3 파일을 WAV로 변환"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            # Use built-in print function directly
            import builtins
            print = builtins.print
            PkTexts = type('PkTexts', (), {
                'CONVERSION_COMPLETE': '변환 완료',
                'CONVERSION_FAILED': '변환 실패',
                'CONVERSION_WORK_COMPLETE': '변환 작업 완료'
            })()

        if output_dir is None:
            from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
            output_dir = D_PK_WORKING
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        mp3_path = Path(mp3_file)
        if not mp3_path.exists():
            raise FileNotFoundError(f"MP3 파일을 찾을 수 없습니다: {mp3_file}")
        
        # 출력 파일명 생성
        wav_filename = mp3_path.stem + ".wav"
        wav_file = output_dir / wav_filename
        
        # FFmpeg를 사용하여 변환
        try:
            from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
            ffmpeg_path = Path(F_FFMPEG_EXE)
            
            if not ffmpeg_path.exists():
                # 시스템 PATH에서 ffmpeg 찾기
                import shutil
                ffmpeg_path = shutil.which("ffmpeg")
                if not ffmpeg_path:
                    raise FileNotFoundError("FFmpeg를 찾을 수 없습니다")
                ffmpeg_path = Path(ffmpeg_path)
            
            # 변환 명령 실행
            import subprocess
            result = subprocess.run([
                str(ffmpeg_path),
                "-i", str(mp3_path),
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                str(wav_file),
                "-y"  # 기존 파일 덮어쓰기
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and wav_file.exists():
                logging.debug(f"[{PkTexts.CONVERSION_COMPLETE}] 파일명={os.path.basename(wav_file)}")
                return str(wav_file)
            else:
                logging.debug(f"[{PkTexts.CONVERSION_FAILED}] 파일명={os.path.basename(mp3_file)} 오류={result.stderr}")
                return None
                
        except Exception as e:
            logging.debug(f"[{PkTexts.CONVERSION_FAILED}] 파일명={os.path.basename(mp3_file)} 오류={e}")
            return None
            
    except Exception as e:
        logging.debug(f"[{PkTexts.CONVERSION_FAILED}] 오류={e}")
        return None


def convert_multiple_mp3_to_wav(mp3_files, output_dir=None):
    """여러 MP3 파일을 WAV로 변환"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            # Use built-in print function directly
            import builtins
            print = builtins.print
            PkTexts = type('PkTexts', (), {
                'CONVERSION_WORK_COMPLETE': '변환 작업 완료'
            })()

        if isinstance(mp3_files, str):
            mp3_files = [mp3_files]
        
        if output_dir is None:
            from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
            output_dir = D_PK_WORKING
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        converted_files = []
        failed_files = []
        
        for mp3_file in mp3_files:
            result = convert_mp3_to_wav(mp3_file, output_dir)
            if result:
                converted_files.append(result)
            else:
                failed_files.append(mp3_file)
        
        # 결과 요약
        total_files = len(mp3_files)
        success_count = len(converted_files)
        failed_count = len(failed_files)
        
        logging.debug(f"[{PkTexts.CONVERSION_WORK_COMPLETE}] 총파일수={total_files} 성공={success_count} 실패={failed_count}")
        
        return {
            'converted_files': converted_files,
            'failed_files': failed_files,
            'total_files': total_files,
            'success_count': success_count,
            'failed_count': failed_count
        }
        
    except Exception as e:
        logging.debug(f"[{PkTexts.CONVERSION_FAILED}] 오류={e}")
        return None

def update_index_file():
    """index.json 파일의 파일 경로를 MP3에서 WAV로 업데이트합니다."""
    import json
    
    index_file = os.path.join(d_pk_external_tools, "index.json")
    
    if not os.path.exists(index_file):
        logging.debug("index.json 파일이 없습니다.")
        return
    
    try:
        # index.json 읽기
        with open(index_file, "r", encoding="utf-8") as f:
            index_data = json.load(f)
        
        updated_count = 0
        
        # 모든 경로를 MP3에서 WAV로 변경
        for key, file_path in index_data.items():
            if file_path.endswith('.mp3'):
                wav_path = file_path.replace('.mp3', '.wav')
                # WAV 파일이 실제로 존재하는지 확인
                if os.path.exists(wav_path):
                    index_data[key] = wav_path
                    updated_count += 1
                    logging.debug(f"경로 업데이트: {os.path.basename(file_path)} → {os.path.basename(wav_path)}")
        
        # 업데이트된 index.json 저장
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        logging.debug(f"index.json 업데이트 완료: {updated_count}개 경로 변경")
        
    except Exception as e:
        logging.debug(f"index.json 업데이트 실패: {e}")

def cleanup_mp3_files():
    """변환 완료 후 MP3 파일들을 삭제합니다."""
    mp3_pattern = os.path.join(d_pk_external_tools, "*.mp3")
    mp3_files = glob.glob(mp3_pattern)
    
    if not mp3_files:
        logging.debug("삭제할 MP3 파일이 없습니다.")
        return
    
    logging.debug(f"총 {len(mp3_files)}개의 MP3 파일을 삭제합니다...")
    
    deleted_count = 0
    
    for mp3_file in mp3_files:
        try:
            # 해당하는 WAV 파일이 존재하는지 확인
            wav_file = mp3_file.replace('.mp3', '.wav')
            if os.path.exists(wav_file):
                os.remove(mp3_file)
                deleted_count += 1
                logging.debug(f"삭제 완료: {os.path.basename(mp3_file)}")
            else:
                logging.debug(f"WAV 파일이 없어서 보존: {os.path.basename(mp3_file)}")
        except Exception as e:
            logging.debug(f"삭제 실패: {os.path.basename(mp3_file)} - {e}")
    
    logging.debug(f"삭제 완료: {deleted_count}개 파일 삭제")

def main():
    """메인 함수"""
    logging.debug("MP3 → WAV 변환 작업 시작")
    print(PK_UNDERLINE)
    
    # n. MP3를 WAV로 변환
    convert_mp3_to_wav()
    print()
    
    # n. index.json 업데이트
    update_index_file()
    print()
    
    # n. 사용자에게 MP3 파일 삭제 여부 확인
    response = input("변환 완료 후 MP3 파일들을 삭제하시겠습니까? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        cleanup_mp3_files()
    else:
        logging.debug("MP3 파일들이 보존되었습니다.")
    
    logging.debug("변환 작업 완료!")

if __name__ == "__main__":
    main() 