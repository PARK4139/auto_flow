import traceback

from pk_internal_tools.pk_functions.ensure_gpt_answer_done import ensure_gpt_answer_done
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

from pk_internal_tools.pk_objects.pk_texts import PkTexts

def pk_ensure_gpt_answer_done(
    question: str,
    api_key: str = None,
    model: str = "gpt-4o-mini",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    system_prompt: str = None,
    save_conversation: bool = True,
    conversation_file: str = "chatgpt_conversation.json"
) -> str:
    """
    ChatGPT API를 사용하여 질문에 답변하는 함수 (호출 전용 wrapper)
    
    Args:
        question: ChatGPT에게 물어볼 질문
        api_key: OpenAI API 키 (None이면 환경변수에서 가져옴)
        model: 사용할 모델 (gpt-4o-mini, gpt-4o, gpt-3.5-turbo 등)
        max_tokens: 최대 토큰 수
        temperature: 창의성 정도 (0.0 ~ 1.0)
        system_prompt: 시스템 프롬프트 (None이면 기본값 사용)
        save_conversation: 대화 기록 저장 여부
        conversation_file: 대화 기록 파일명
    
    Returns:
        str: ChatGPT의 답변
    """
    return ensure_gpt_answer_done(
        question=question,
        api_key=api_key,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=system_prompt,
        save_conversation=save_conversation,
        conversation_file=conversation_file
    )

# 편의 함수들
def ask_simple_question(question: str) -> str:
    """간단한 질문 함수"""
    return ensure_gpt_answer_done(question)

def ask_with_custom_prompt(question: str, system_prompt: str) -> str:
    """커스텀 프롬프트로 질문"""
    return ensure_gpt_answer_done(
        question=question,
        system_prompt=system_prompt
    )

def ask_with_creative_response(question: str) -> str:
    """창의적인 답변 요청"""
    return ensure_gpt_answer_done(
        question=question,
        temperature=0.9,
        max_tokens=1500
    )

def ask_with_precise_response(question: str) -> str:
    """정확한 답변 요청"""
    return ensure_gpt_answer_done(
        question=question,
        temperature=0.1,
        max_tokens=800
    )

if __name__ == "__main__":
    # 테스트 실행
    try:
        # 간단한 질문 테스트
        question = "파이썬에서 리스트와 튜플의 차이점을 설명해주세요."
        answer = ask_simple_question(question)
        
        # 대화 기록 출력
        from pk_internal_tools.pk_functions.ensure_gpt_answer_done import print_chat_history
        print_chat_history()
        
    except Exception as e:
        import logging
        logging.debug(f"❌ {PkTexts.TEST_FAILED}: {e}")
        logging.debug(f"🔑 {PkTexts.OPENAI_API_KEY_SETUP}.")
