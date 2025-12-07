from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
def get_gemini_prompt_starting():
    prompt_starting = rf"*너의 역할은 시니어 개발자, 나의 역할은 입사한 경력직 개발자, 작업수행을 위해서, GEMINI.md 의 모든 내용과 규칙들 숙지하고 대기요청"
    return prompt_starting
