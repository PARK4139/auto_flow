"""
Kiri 상태 관리 유틸리티 함수들
시간 기반 알림, 인사, 히스토리 등을 처리합니다.
"""
import logging
import sqlite3
from datetime import date, datetime, time

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers
from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE
from pk_internal_tools.pk_objects.pk_kiri_state import KiriMode, KiriState
from pk_internal_tools.pk_objects.pk_texts import PkTexts

logger = logging.getLogger(__name__)


def parse_time_ranges(text_list):
    """sample: ["12:00-13:00", "15:00-15:10"] -> [(time(12,0), time(13,0)), (time(15,0), time(15,10))]"""
    ranges = []
    for txt in text_list:
        try:
            start_str, end_str = txt.split("-")
            h1, m1 = map(int, start_str.strip().split(":"))
            h2, m2 = map(int, end_str.strip().split(":"))
            ranges.append((time(h1, m1), time(h2, m2)))
        except Exception as e:
            continue
    return ranges


def is_now_in_time_range(now_time, time_range):
    """현재 시간이 시간 범위 내에 있는지 확인"""
    start, end = time_range
    return start <= now_time <= end


def show_command_history(state: KiriState):
    """명령어 히스토리 표시"""
    logging.debug("명령어 히스토리:")
    for i, entry in enumerate(state.command_history[-10:], 1):  # 최근 10개
        timestamp = entry['timestamp'].strftime("%H:%M:%S")
        logging.debug(f"{i}. [{timestamp}] {entry['command']} ({entry['mode']})")


def show_current_status(state: KiriState):
    """현재 상태 표시"""
    logging.debug("Kiri 현재 상태:")
    logging.debug(f"모드: {state.current_mode.value}")
    logging.debug(f"마이크: {'연결됨' if state.microphone_available else '연결되지 않음'}")
    logging.debug(f"실행 중: {'예' if state.is_running else '아니오'}")
    logging.debug(f"명령어 수: {len(state.command_history)}")

    # 사용 가능한 프로세스 수 표시
    try:
        pk_wrappers = get_excutable_pk_wrappers()
        logging.debug(f"사용 가능한 프로세스: {len(pk_wrappers)}개")
    except Exception as e:
        logging.debug(f"사용 가능한 프로세스: 확인 불가")

    if state.last_command_time:
        logging.debug(f"마지막 명력어: {state.last_command_time.strftime('%H:%M:%S')}")


def alert(now_time, state: KiriState):
    """알림 함수: 모드에 따른 알림 방식 적용"""
    message = f"{PkTexts.ALERT_TIME} {now_time.hour}시 {now_time.minute}분입니다."
    if state.current_mode != KiriMode.SILENT:
        ensure_spoken(message)
    logging.debug(message)


def ensure_greeting_daily(state: KiriState):
    """
    일일 인사 - 시간대에 따라 아침/점심/저녁 인사
    하루에 각 인사는 1번씩만, pk.sqlite에 상태 저장/불러오기
    """
    now = datetime.now()
    hour = now.hour
    today_str = date.today().isoformat()
    if 5 <= hour < 12:
        greeting_type = "morning"
        greeting = f"{PkTexts.GOOD_MORNING}"
    elif 12 <= hour < 18:
        greeting_type = "afternoon"
        greeting = f"{PkTexts.GOOD_AFTERNOON}"
    else:
        greeting_type = "evening"
        greeting = f"{PkTexts.GOOD_EVENING}"

    db_path = F_pk_SQLITE
    greeted = False
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS greeting_log (
                date TEXT,
                type TEXT,
                PRIMARY KEY (date, type)
            )
        """)
        cur.execute(
            "SELECT 1 FROM greeting_log WHERE date=? AND type=?",
            (today_str, greeting_type)
        )
        greeted = cur.fetchone() is not None
        if not greeted:
            cur.execute(
                "INSERT INTO greeting_log (date, type) VALUES (?, ?)",
                (today_str, greeting_type)
            )
            conn.commit()
        conn.close()
    except Exception as e:
        logging.debug(f"️ 인사 기록 DB 오류: {e}")
        # DB 오류 시에도 인사 1회만 수행(중복 가능성 감수)

    if not greeted:
        if state.current_mode != KiriMode.SILENT:
            ensure_spoken(greeting)


def process_time_based_alerts(now: datetime, state: KiriState, all_time_blocks):
    """시간 기반 알림 처리"""
    now_time = now.time()

    # 1시간마다 콘솔 클리어
    if now.hour != state.last_cleared_hour:
        ensure_console_cleared()
        state.last_cleared_hour = now.hour
        state.alerted_blocks.clear()  # 새로운 시간 진입 시, 알림 상태 초기화
        if state.current_mode == KiriMode.DEBUG:
            logging.debug(f"{PkTexts.ALERT_BLOCKS}=({state.alerted_blocks})")

    # 현재 속한 구간 하나만 처리
    for idx, block in enumerate(all_time_blocks):
        if is_now_in_time_range(now_time, block):
            if idx not in state.alerted_blocks:
                alert(now_time, state)
                state.alerted_blocks.add(idx)
                break

