import logging
import re
from enum import Enum, auto
import speech_recognition as sr
import asyncio
import nest_asyncio
import random

from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1200 import get_pk_time_2025_10_20_1200
# --- 기존 프로젝트 함수 임포트 ---
# 마이그레이션을 위해 기존 파일의 거의 모든 함수를 가져옵니다.
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.get_comprehensive_weather_information_from_web import get_comprehensive_weather_information_from_web
from pk_internal_tools.pk_functions.ensure_sound_file_executed import ensure_sound_file_executed
from pk_internal_tools.pk_functions.empty_recycle_bin import empty_recycle_bin
from pk_internal_tools.pk_functions.ensure_work_directory_created import ensure_work_directory_created
from pk_internal_tools.pk_functions.make_version_new import make_version_new
from pk_internal_tools.pk_functions.ensure_py_system_processes_restarted import ensure_py_system_processes_restarted
from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
from pk_internal_tools.pk_functions.move_f_via_telegram_bot_v2 import move_f_via_telegram_bot_v2
from pk_internal_tools.pk_functions.cmd_f_in_cmd_exe_like_human import cmd_f_in_cmd_exe_like_human
from pk_internal_tools.pk_functions.ensure_todo_list_guided import ensure_todo_list_guided
from pk_internal_tools.pk_functions.speak_today_info_as_korean import speak_today_info_as_korean
from pk_internal_tools.pk_functions.get_weekday import get_weekday
from pk_internal_tools.pk_functions.run_up_and_down_game import run_up_and_down_game
from pk_internal_tools.pk_functions.play_my_video_track import play_my_video_track
from pk_internal_tools.pk_functions.ensure_power_saved_as_s4 import ensure_power_saved_as_s4
from pk_internal_tools.pk_functions.ensure_screen_saved import ensure_screen_saved
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_objects.pk_directories import d_pk_root, d_pk_external_tools, D_ARCHIVED


class ConversationState(Enum):
    LISTENING = auto()
    PROCESSING = auto()
    RESPONDING = auto()
    EXIT = auto()

class KiriaContext:
    """대화의 맥락을 저장하는 클래스"""
    def __init__(self):
        self.last_intent = None
        self.last_entities = {}

def recognize_intent(text: str):
    """사용자 발화에서 의도와 엔티티를 추출합니다."""
    text = text.lower().replace(' ', '')
    
    intent_keywords = {
        "GET_WEATHER": ["날씨", "기상"],
        "PLAY_MUSIC": ["음악", "노래"],
        "EXIT": ["종료", "잘가", "퇴근해"],
        "EMPTY_TRASH": ["휴지통비워", "휴지통정리"],
        "STUDY_ENGLISH": ["영어공부"],
        "CREATE_WORK_DIR": ["업무디렉토리생성", "업무폴더생성"],
        "UPDATE_VERSION": ["버전업데이트", "버저닝"],
        "BACKUP_PROJECT": ["프로젝트백업", "백업해"],
        "BACKUP_VIA_TELEGRAM": ["텔레그램으로백업"],
        "RUN_PK_COMMAND": ["피케이"],
        "GUIDE_TODO": ["할일", "스케줄"],
        "GET_DATE": ["오늘날짜", "날짜"],
        "GET_DAY": ["요일"],
        "GET_TIME": ["시간", "몇시"],
        "PLAY_GAME": ["게임", "미니게임"],
        "PLAY_VIDEO": ["비디오", "영상"],
        "ENTER_HIBERNATE": ["최대절전모드"],
        "SAVE_SCREEN": ["화면보호기", "화면보호"],
    }

    for intent, keywords in intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            # 간단한 엔티티 추출 (향후 확장 가능)
            entities = {}
            if intent == "GET_WEATHER":
                location_match = re.search(r"(부산|서울|대전|대구|광주|인천)", text)
                entities["location"] = location_match.group(1) if location_match else "현재위치"
            return {"intent": intent, "entities": entities}

    return {"intent": "UNKNOWN", "entities": {}}

# --- 의도별 처리 함수 ---

def handle_get_weather(entities):
    location = entities.get("location", "알 수 없는 위치")
    ensure_spoken(f"{location}의 날씨를 검색합니다.")
    get_comprehensive_weather_information_from_web()
    return "날씨 정보를 화면에 표시했습니다."

def handle_play_music(entities):
    ensure_sound_file_executed()
    return "음악을 재생합니다."

def handle_exit(entities):
    return "대화를 종료합니다. 좋은 하루 되세요."

def handle_empty_trash(entities):
    empty_recycle_bin()
    return "휴지통을 비웠습니다."

def handle_study_english(entities):
    ensure_spoken("What is the weather like?")
    ensure_slept(seconds=random.randint(a=3, b=5))
    ensure_spoken("I can't directly access weather information, but if you share your location, I can guide you!")
    return "영어 공부 스크립트가 완료되었습니다."

def handle_create_work_dir(entities):
    ensure_work_directory_created()
    return "업무용 디렉토리를 생성했습니다."

def handle_update_version(entities):
    make_version_new(via_f_txt=True)
    return "새로운 버전을 생성했습니다."

def handle_backup_project(entities):
    ensure_py_system_processes_restarted([rf"{d_pk_external_tools}/pk_back_up_project.py"])
    return "프로젝트 백업을 시작합니다."

def handle_backup_via_telegram(entities):
    f = ensure_pnx_backed_up(pnx_working=d_pk_root, d_dst=D_ARCHIVED)
    nest_asyncio.apply()
    asyncio.run(move_f_via_telegram_bot_v2(f))
    return "백업 파일을 텔레그램으로 전송했습니다."

def handle_run_pk_command(entities):
    cmd_f_in_cmd_exe_like_human(cmd_prefix='python', f=rf"{d_pk_root}/ensure_pk_wrapper_starter_executed")
    return "PK 시스템 래퍼를 실행합니다."

def handle_guide_todo(entities):
    ensure_todo_list_guided()
    return "오늘의 할일 목록을 안내합니다."

def handle_get_date(entities):
    speak_today_info_as_korean()
    return "" # 함수가 직접 말하므로 별도 응답 없음

def handle_get_day(entities):
    return f"오늘은 {get_weekday()}입니다."

def handle_get_time(entities):
    HH = get_pk_time_2025_10_20_1200('%H')
    mm = get_pk_time_2025_10_20_1200('%M')
    return f"현재 시각은 {int(HH)}시 {int(mm)}분입니다."

def handle_play_game(entities):
    run_up_and_down_game()
    return "미니 게임을 시작합니다."

def handle_play_video(entities):
    play_my_video_track()
    return "비디오를 재생합니다."

def handle_enter_hibernate(entities):
    ensure_power_saved_as_s4()
    return "최대 절전 모드로 진입합니다."

def handle_save_screen(entities):
    ensure_screen_saved()
    return "화면 보호기를 실행합니다."

def handle_unknown(entities):
    return "죄송합니다. 무슨 말씀이신지 잘 이해하지 못했습니다."

# 의도와 함수를 연결하는 맵
INTENT_ACTION_MAP = {
    "GET_WEATHER": handle_get_weather,
    "PLAY_MUSIC": handle_play_music,
    "EXIT": handle_exit,
    "EMPTY_TRASH": handle_empty_trash,
    "STUDY_ENGLISH": handle_study_english,
    "CREATE_WORK_DIR": handle_create_work_dir,
    "UPDATE_VERSION": handle_update_version,
    "BACKUP_PROJECT": handle_backup_project,
    "BACKUP_VIA_TELEGRAM": handle_backup_via_telegram,
    "RUN_PK_COMMAND": handle_run_pk_command,
    "GUIDE_TODO": handle_guide_todo,
    "GET_DATE": handle_get_date,
    "GET_DAY": handle_get_day,
    "GET_TIME": handle_get_time,
    "PLAY_GAME": handle_play_game,
    "PLAY_VIDEO": handle_play_video,
    "ENTER_HIBERNATE": handle_enter_hibernate,
    "SAVE_SCREEN": handle_save_screen,
    "UNKNOWN": handle_unknown,
}

def ensure_kiria_executed_2025_10_22():
    """자연스러운 대화형 구조를 가진 키리아 실행 함수"""
    state = ConversationState.LISTENING
    context = KiriaContext()
    recognizer = sr.Recognizer()

    # ensure_spoken("안녕하세요. 키리아입니다. 무엇을 도와드릴까요?")
    logging.debug('kiria is ready')
    while state != ConversationState.EXIT:
        if state == ConversationState.LISTENING:
            user_input = None
            with sr.Microphone() as source:
                logging.info("듣고 있습니다...")
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    user_input = recognizer.recognize_google(audio, language="ko")
                    logging.info(f"사용자 입력: {user_input}")
                    state = ConversationState.PROCESSING
                except sr.UnknownValueError:
                    # 사용자가 요청한대로 음성 안내 제거
                    state = ConversationState.LISTENING 
                except Exception as e:
                    logging.error(f"음성 인식 중 오류 발생: {e}")
                    state = ConversationState.LISTENING

        elif state == ConversationState.PROCESSING:
            if not user_input:
                state = ConversationState.LISTENING
                continue

            recognized_info = recognize_intent(user_input)
            intent = recognized_info["intent"]
            entities = recognized_info["entities"]
            
            context.last_intent = intent
            context.last_entities = entities

            action = INTENT_ACTION_MAP.get(intent, handle_unknown)
            response_text = action(entities)
            
            if intent == "EXIT" or intent == "ENTER_HIBERNATE":
                state = ConversationState.EXIT
            else:
                state = ConversationState.RESPONDING

        elif state == ConversationState.RESPONDING:
            if response_text: # 응답할 텍스트가 있을 경우에만 말하기
                ensure_spoken(response_text)
            state = ConversationState.LISTENING

    # 종료 상태일 때 마지막 인사
    if response_text:
        ensure_spoken(response_text)
    logging.info("키리아 대화를 종료합니다.")

