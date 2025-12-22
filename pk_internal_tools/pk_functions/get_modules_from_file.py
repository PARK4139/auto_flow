 
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_modules_from_file(f_working):
    from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
    
    lines = get_list_from_f(f=f_working)
    modules_set = set()  # 성능 향상을 위해 set 사용
    
    for line in lines:
        line = line.strip()
        # 빈 줄이나 주석만 있는 줄 건너뛰기
        if not line or line.startswith('#'):
            continue
            
        # import 문만 추출 (더 빠른 조건 검사)
        if line.startswith('import ') or line.startswith('from '):
            modules_set.add(line)
    
    # set을 바로 정렬된 리스트로 변환 (중간 과정 제거)
    return sorted(modules_set, reverse=True)


