from pathlib import Path

from ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import (
    ensure_pnx_opened_by_ext,
)
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
from pk_internal_tools.pk_functions.print_yellow import print_yellow

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

TASK_FLAG_FILE = "is_gemini_task_done.md"
TASK_TODO_FILE = "gemini_tasks_todo.md"
TASK_DONE_FILE = "gemini_tasks_done.md"

SLEEP_SHORT_MS = 50
SLEEP_MID_MS = 5000
SLEEP_LONG_MS = 30000
SLEEP_IDLE_MS = 100000  # TODO 없을 때 대기 시간 (ms)


def _check_gemini_action():
    """Send a short keep-alive message to gemini-cli."""
    ensure_typed("ok, keep going")
    ensure_slept(milliseconds=SLEEP_SHORT_MS)
    ensure_pressed("enter")


def _permit_gemini_action():
    """Just press enter to let gemini-cli continue."""
    ensure_pressed("enter")
    ensure_slept(milliseconds=SLEEP_SHORT_MS)


def _check_flash_mode():
    """Wait for flash mode and press '1' if needed."""
    ensure_slept(milliseconds=5000)
    ensure_pressed("1")


def _toggle_auto_mode():
    """Toggle auto mode in gemini-cli (shift + tab)."""
    ensure_pressed("shift", "tab")
    ensure_slept(milliseconds=SLEEP_SHORT_MS)


def _ensure_task_files_initialized():
    """
    Ensure that the flag/todo/done files exist.

    - TASK_FLAG_FILE: contains exactly 'False' or 'True'
    - TASK_TODO_FILE: plain text or markdown, one task per line is recommended
    - TASK_DONE_FILE: archive of completed tasks
    """
    flag_path = Path(TASK_FLAG_FILE)
    if not flag_path.exists():
        flag_path.write_text("False\n", encoding="utf-8")

    todo_path = Path(TASK_TODO_FILE)
    if not todo_path.exists():
        todo_path.write_text("", encoding="utf-8")

    done_path = Path(TASK_DONE_FILE)
    if not done_path.exists():
        done_path.write_text("", encoding="utf-8")


def _has_remaining_todo() -> bool:
    """Return True if there is any non-empty line in TASK_TODO_FILE."""
    todo_path = Path(TASK_TODO_FILE)
    if not todo_path.exists():
        return False

    content = todo_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if line.strip():
            return True
    return False


def _send_initial_protocol_to_gemini():
    """
    Explain to gemini-cli how to use the three files.

    This is a one-time system-level explanation so that gemini-cli
    understands the cyclic workflow.
    """
    message = (
        "지금부터 너는 반복 실행되는 TODO 자동화 래퍼와 함께 동작하고 있어.\n"
        f"'{TASK_TODO_FILE}' 파일에는 해야 할 작업들이 한 줄에 하나씩 적혀 있어.\n"
        f"'{TASK_DONE_FILE}' 파일은 이미 완료된 작업들을 보관하는 아카이브야.\n"
        f"'{TASK_FLAG_FILE}' 파일은 현재 작업이 완전히 끝났는지를 나타내는 단순 플래그로 사용할 거야.\n\n"
        "- 새로운 작업을 시작하기 전에 '{TASK_FLAG_FILE}' 내용이 반드시 'False'인지 확인해.\n"
        "- '{TASK_TODO_FILE}'에서 아직 처리되지 않은 다음 작업을 선택해서 수행해.\n"
        "- 작업을 구현하고, 테스트하고, Git 커밋까지 완료했다면:\n"
        "  1) 해당 작업 라인을 '{TASK_TODO_FILE}'에서 제거하고,\n"
        "  2) 같은 라인을 '{TASK_DONE_FILE}' 맨 아래에 추가하고,\n"
        "  3) '{TASK_FLAG_FILE}' 내용을 'True'로 덮어써.\n"
        "- 내가 다음 루프에서 플래그를 확인하고 다시 'False'로 되돌려 줄 거야.\n"
        "- 더 이상 처리할 TODO가 없다면 '{TASK_TODO_FILE}'를 비우고, "
        f"'{TASK_FLAG_FILE}'를 'True'로 유지해서 루프가 종료되도록 도와줘.\n"
        "  (다만 이 래퍼에서는 TODO가 없으면 종료 대신 대기 모드로 들어간다는 점을 기억해줘.)\n"
    )

    ensure_typed(message)
    ensure_pressed("enter")


def _run_cyclic_todo_loop():
    """
    Main cyclic loop.

    - TODO가 없으면:
      - Gemini에게 '현재 TODO 없음, 대기 모드'라고 안내
      - TODO 편집을 쉽게 하도록 ensure_pnx_opened_by_ext(TASK_TODO_FILE) 호출
      - Python 쪽은 ensure_slept(SLEEP_IDLE_MS) 후 다시 TODO 확인
    - TODO가 있으면:
      - 다음 TODO 작업 처리 요청 → 구현/테스트/커밋 → 플래그/파일 업데이트 프로토콜 수행
    """
    while True:
        # 1) TODO 존재 여부 확인
        if not _has_remaining_todo():
            # Gemini에게 "지금은 TODO가 없으니 대기" 상태임을 알림
            print_yellow(
                f"No remaining TODO found in '{TASK_TODO_FILE}'. "
                "Gemini will stay idle until new TODO is added."
            )

            ensure_typed(
                f"현재 '{TASK_TODO_FILE}' 파일에 남은 TODO 항목이 없어. "
                "새로운 작업이 이 파일에 추가될 때까지 대기 상태를 유지해줘. "
                "주기적으로 파일 내용을 다시 확인해서, 새로운 TODO가 생기면 그때부터 다시 작업을 시작해줘."
            )
            ensure_pressed("enter")

            # TODO 편집을 위해 TODO 파일을 pnx(또는 확장자 연결된 프로그램)로 열어준다.
            ensure_pnx_opened_by_ext(TASK_TODO_FILE)

            # 파이썬 프로세스는 종료하지 않고, 길게 슬립 후 다시 루프 상단으로 복귀
            ensure_slept(milliseconds=SLEEP_IDLE_MS)
            continue

        # 2) TODO가 존재하면, Gemini가 계속 진행할 수 있도록 Enter 전송
        _permit_gemini_action()

        # 3) 다음 TODO 처리 요청
        ensure_typed(
            f"지금부터 '{TASK_TODO_FILE}' 파일에서 아직 처리되지 않은 다음 작업을 선택해서 구현해줘. "
            f"작업을 완료하고 테스트 및 커밋까지 모두 끝났다면, 내가 설명한 프로토콜에 따라 "
            f"'{TASK_TODO_FILE}', '{TASK_DONE_FILE}', '{TASK_FLAG_FILE}'를 업데이트해줘."
        )
        ensure_pressed("enter")

        # 구현/테스트/커밋 시간 부여
        ensure_slept(milliseconds=SLEEP_LONG_MS)

        # 4) Keep-alive 및 진행 상황 확인
        _check_gemini_action()
        ensure_slept(milliseconds=SLEEP_MID_MS)

        # 5) 플래그 파일 사용 검증 및 갱신 요청
        ensure_typed(
            f"현재 '{TASK_FLAG_FILE}' 파일의 내용을 확인해줘. "
            "만약 내용이 'True'라면, 방금 처리한 작업이 TODO에서 DONE으로 정상 이동되었는지 한 번 더 검증해. "
            "검증까지 끝났다면 '{TASK_FLAG_FILE}' 내용을 다시 'False'로 덮어쓰고, 다음 작업을 대기 상태로 만들어줘. "
            "아직 처리할 작업이 없다면 'True'를 유지해도 좋아."
        )
        ensure_pressed("enter")

        ensure_slept(milliseconds=SLEEP_MID_MS)

        # 6) 테스트 및 커밋 최종 점검 요청
        ensure_typed(
            "방금 작업에 대한 테스트 코드(또는 검증 절차)를 다시 한 번 실행해서 문제가 없는지 확인해줘. "
            "이상이 없다면 Git 커밋 상태와 브랜치 상태도 한 번 더 점검해줘."
        )
        ensure_pressed("enter")

        ensure_slept(milliseconds=SLEEP_LONG_MS)


if __name__ == "__main__":
    try:
        import traceback

        from pk_internal_tools.pk_functions.get_caller_name import (
            get_caller_name,
        )
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import (
            ensure_exception_routine_done,
        )
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import (
            ensure_finally_routine_done,
        )
        from pk_internal_tools.pk_functions.ensure_gemini_cli_executed import (
            ensure_gemini_cli_executed,
        )
        from pk_internal_tools.pk_functions.ensure_initial_prompt_to_gemini_cli_sent import (
            ensure_initial_prompt_to_gemini_cli_sent,
        )
        from pk_internal_tools.pk_functions.ensure_killed_gemini_related_windows import (
            ensure_killed_gemini_related_windows,
        )
        from pk_internal_tools.pk_functions.ensure_pk_gemini_executed import (
            ensure_pk_gemini_executed,
        )
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import (
            ensure_pk_starting_routine_done_without_pk_log_file_logging,
        )
        from pk_internal_tools.pk_functions.ensure_window_title_replaced import (
            ensure_window_title_replaced,
        )
        from pk_internal_tools.pk_functions.ensure_window_to_front import (
            ensure_window_to_front,
        )
        from pk_internal_tools.pk_functions.ensure_value_completed import (
            ensure_value_completed,
        )
        from pk_internal_tools.pk_functions.get_pk_gemini_starter_title import (
            get_pk_gemini_starter_title,
        )
        from pk_internal_tools.pk_objects.pk_directories import (
            d_pk_root,
            D_PK_MEMO_REPO,
            D_AUTO_FLOW_REPO,
        )

        func_n = get_caller_name()

        ensure_pk_starting_routine_done_without_pk_log_file_logging(
            traced_file=__file__, traceback=traceback
        )
        # 필요하면 기존 gemini 관련 창 정리
        # ensure_killed_gemini_related_windows()

        # Gemini 스타터 창 준비
        starter_title = get_pk_gemini_starter_title()
        ensure_window_title_replaced(starter_title)
        ensure_window_to_front(starter_title)

        # Gemini를 어떤 루트 경로에서 실행할지 선택
        local_gemini_root = ensure_value_completed(
            key_name="local_gemini_root",
            func_n=func_n,
            options=[d_pk_root, D_PK_MEMO_REPO, D_AUTO_FLOW_REPO],
        )

        # 선택한 루트 경로에서 gemini-cli 실행
        ensure_gemini_cli_executed(
            local_gemini_root=local_gemini_root
        )

        # TODO/FLAG/DONE 파일 초기화
        _ensure_task_files_initialized()

        # TODO 파일을 기본 에디터로 한 번 열어줌
        ensure_command_executed(cmd=f'start "" "{TASK_TODO_FILE}"')
        print_yellow(
            f"Write TODO items to '{TASK_TODO_FILE}'. One task per line is recommended."
        )
        input("Press Enter to start cyclic gemini-cli TODO execution...")

        # Gemini 자동 모드 및 flash 모드 세팅
        _toggle_auto_mode()
        _check_flash_mode()

        # Gemini에게 파일 기반 TODO 프로토콜 1회 안내
        ensure_initial_prompt_to_gemini_cli_sent(
            initial_prompt="지금부터 TODO 자동화 래퍼와 함께 동작할거야. "
                           "이어지는 설명은 파일 기반 TODO 처리 프로토콜이야."
        )
        _send_initial_protocol_to_gemini()

        # 메인 루프 시작
        _run_cyclic_todo_loop()

    except Exception as exception:
        ensure_exception_routine_done(
            traced_file=__file__, traceback=traceback, exception=exception
        )
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
