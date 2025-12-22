from enum import auto, Enum

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


class PkPromptGroups(Enum):
    PK_SCHEDULER = auto()
    SMART_PLUG = auto()
    ENSURE_SPOKEN = auto()
    COMMON = auto()


@ensure_seconds_measured
def ensure_pk_gemini_executed(local_gemini_root=None):
    """
    TODO :
    """
    import logging
    import textwrap

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_gemini_cli_interactive_mode_initial_prompt import get_gemini_cli_interactive_mode_initial_prompt
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_gemini_prompt_interface_title import get_pk_gemini_title
    from pk_internal_tools.pk_functions.is_gemini_cli_window_found import is_gemini_cli_window_found

    pk_gemini_title = get_pk_gemini_title(local_gemini_root=local_gemini_root)
    ensure_window_title_replaced(pk_gemini_title)
    ensure_window_to_front(pk_gemini_title)
    ensure_window_resized_and_positioned_left_half()

    # pk_prompts_favorite
    prompts_by_group = {
        PkPromptGroups.COMMON: textwrap.dedent(rf'''
                        {get_gemini_cli_interactive_mode_initial_prompt()}

                        🔧 복붙 프롬프트 (Markdown · Tapo 전부 제외 · Windows+WSL · python-matter-server 전용)
                        ⚠️ TP-Link Tapo/Kasa 로컬 API·통합·라이브러리 관련 내용은 일절 포함하지 말 것. (이번 과제는 Matter만 사용)
                        🎯 목표
                        🧰 전제
                        ✅ 출력 형식 (반드시 지킬 것)
                        🔚 요약
                    ''').strip(),
    }
    prompt_group = PkPromptGroups.COMMON
    prompts_raw = prompts_by_group.get(prompt_group, "")
    parsed_prompts = [p.strip() for p in prompts_raw.split('\n\n') if p.strip()]
    if not prompts_raw:
        logging.debug("선택된 그룹에 등록된 프롬프트가 없습니다.")

    key_name = "prompt_to_request"
    func_n = get_caller_name()
    from pk_internal_tools.pk_functions.get_gemini_shortcut_guide_text import get_gemini_shortcut_guide_text
    guide_text = get_gemini_shortcut_guide_text()
    prompt = ensure_value_completed(key_name=key_name, func_n=func_n, options=parsed_prompts, guide_text=guide_text)
    prompt = prompt.replace('\n', r'\n')
    if not is_gemini_cli_window_found(local_gemini_root=local_gemini_root):
        logging.debug("gemini cli window is not found")
        return None