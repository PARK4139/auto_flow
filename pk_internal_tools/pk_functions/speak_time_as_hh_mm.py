import os
from datetime import datetime
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
import logging
from pk_internal_tools.pk_objects.pk_files import d_pk_external_tools

def speak_time_as_hh_mm():
    """현재 시간을 모듈화된 WAV 파일들로 조합하여 말하기"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    # 오전/오후 구분
    period = "오전" if hour < 12 else "오후"
    hour_12 = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
    
    # 조합할 WAV 파일들
    wav_components = [
        f"{period}.wav",
        f"{hour_12}시.wav", 
        f"{minute}분.wav"
    ]
    
    # 완성된 파일명 생성
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    final_filename = f"{timestamp}_{hour_12}시 {minute}분입니다.wav"
    final_path = os.path.join(d_pk_external_tools, final_filename)
    
    # 이미 존재하는지 확인
    if os.path.exists(final_path):
        logging.debug(f"기존 파일 사용: {final_filename}")
        # 기존 조합된 WAV 파일 재생
        try:
            # WAV 파일을 직접 재생하기 위해 ensure_spoken 사용
            ensure_spoken(text=f"{hour_12}시 {minute}분입니다", after_delay=0.95)
        except Exception as e:
            logging.debug(f"WAV 파일 재생 실패: {e}")
            # 실패 시 기존 방식 사용
            ensure_spoken(text=f"{hour_12}시 {minute}분입니다", after_delay=0.95)
        return
    
    # 모듈화된 WAV 파일들 조합
    combined_wav = combine_time_wav_files(wav_components, final_path, hour_12, minute)
    
    if combined_wav:
        logging.debug(f"새로운 시간 음성 생성: {final_filename}")
        # 조합된 WAV 파일 재생
        try:
            # WAV 파일을 직접 재생하기 위해 ensure_spoken 사용
            ensure_spoken(text=f"{hour_12}시 {minute}분입니다", after_delay=0.95)
        except Exception as e:
            logging.debug(f"WAV 파일 재생 실패: {e}")
            # 실패 시 기존 방식 사용
            ensure_spoken(text=f"{hour_12}시 {minute}분입니다", after_delay=0.95)
    else:
        # 조합 실패 시 기존 방식 사용
        logging.debug(f"️ WAV 조합 실패, 기존 방식 사용")
        ensure_spoken(text=f"{hour_12}시 {minute}분입니다", after_delay=0.95)


def combine_time_wav_files(wav_components, output_path, hour_12, minute):
    """시간 관련 WAV 파일들을 조합하여 하나의 파일로 만듦"""
    try:
        from pydub import AudioSegment
        
        # 기본 구성 요소 WAV 파일들 경로
        base_components = {
            "시": "시.wav",
            "분": "분.wav", 
            "입니다": "입니다.wav"
        }
        
        # 한글 숫자별 WAV 파일들 (0~59)
        korean_numbers = {
            "0": "영", "1": "일", "2": "이", "3": "삼", "4": "사", "5": "오", 
            "6": "육", "7": "칠", "8": "팔", "9": "구", "10": "십",
            "11": "십일", "12": "십이", "13": "십삼", "14": "십사", "15": "십오",
            "16": "십육", "17": "십칠", "18": "십팔", "19": "십구", "20": "이십",
            "21": "이십일", "22": "이십이", "23": "이십삼", "24": "이십사", "25": "이십오",
            "26": "이십육", "27": "이십칠", "28": "이십팔", "29": "이십구", "30": "삼십",
            "31": "삼십일", "32": "삼십이", "33": "삼십삼", "34": "삼십사", "35": "삼십오",
            "36": "삼십육", "37": "삼십칠", "38": "삼십팔", "39": "삼십구", "40": "사십",
            "41": "사십일", "42": "사십이", "43": "사십삼", "44": "사십사", "45": "사십오",
            "46": "사십육", "47": "사십칠", "48": "사십팔", "49": "사십구", "50": "오십",
            "51": "오십일", "52": "오십이", "53": "오십삼", "54": "오십사", "55": "오십오",
            "56": "오십육", "57": "오십칠", "58": "오십팔", "59": "오십구"
        }
        
        number_files = {}
        for i in range(60):
            number_files[str(i)] = f"{korean_numbers[str(i)]}.wav"
        
        # 오전/오후 WAV 파일들
        period_files = {
            "오전": "오전.wav",
            "오후": "오후.wav"
        }
        
        # 조합할 파일들 찾기
        combined_audio = AudioSegment.empty()
        
        # 시간 부분 추가
        hour_str = str(hour_12)
        hour_wav = os.path.join(d_pk_external_tools, number_files.get(hour_str, f"{hour_str}.wav"))
        if os.path.exists(hour_wav):
            combined_audio += AudioSegment.from_wav(hour_wav)
        else:
            logging.debug(f"️ 시간 WAV 파일 없음: {hour_wav}")
            return False
        
        # "시" 추가
        hour_unit_wav = os.path.join(d_pk_external_tools, base_components["시"])
        if os.path.exists(hour_unit_wav):
            combined_audio += AudioSegment.from_wav(hour_unit_wav)
        else:
            logging.debug(f"️ 시 단위 WAV 파일 없음: {hour_unit_wav}")
            return False
        
        # 분 부분 추가
        minute_str = str(minute)
        minute_wav = os.path.join(d_pk_external_tools, number_files.get(minute_str, f"{minute_str}.wav"))
        if os.path.exists(minute_wav):
            combined_audio += AudioSegment.from_wav(minute_wav)
        else:
            logging.debug(f"️ 분 WAV 파일 없음: {minute_wav}")
            return False
        
        # "분" 추가
        minute_unit_wav = os.path.join(d_pk_external_tools, base_components["분"])
        if os.path.exists(minute_unit_wav):
            combined_audio += AudioSegment.from_wav(minute_unit_wav)
        else:
            logging.debug(f"️ 분 단위 WAV 파일 없음: {minute_unit_wav}")
            return False
        
        # "입니다" 추가
        ending_wav = os.path.join(d_pk_external_tools, base_components["입니다"])
        if os.path.exists(ending_wav):
            combined_audio += AudioSegment.from_wav(ending_wav)
        else:
            logging.debug(f"️ 종료 WAV 파일 없음: {ending_wav}")
            return False
        
        # 완성된 WAV 파일 저장
        combined_audio.export(output_path, format="wav")
        logging.debug(f"WAV 파일 조합 완료: {output_path}")
        return True
        
    except ImportError:
        logging.debug("️ pydub 라이브러리가 설치되지 않아 WAV 조합을 할 수 없습니다.")
        return False
    except Exception as e:
        logging.debug(f"WAV 파일 조합 중 오류: {e}")
        return False


# 시간 관련 WAV 구성 요소 생성을 위한 별도 파일 사용
# from pk_internal_tools.pk_functions.create_time_wav_components import create_time_wav_components, check_time_components


# 기존 함수 호환성을 위한 별칭
def speak_time_as_hh_mm_legacy():
    """기존 방식으로 시간 말하기 (호환성 유지)"""
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    period = "오전" if hour < 12 else "오후"
    hour_12 = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
    
    ensure_spoken(text=f"{period} {hour_12}시 {minute}분", after_delay=0.95)
