import re
from pathlib import Path


def is_non_import_from_line(line):
    # "from "으로 시작하지만, 실제 import가 아닌 경우를 판별
    # 실제 import는 "from ... import ..." 패턴
    # 예: from "xxx" to "yyy", from $Y_\nu$, from (see above figure) 등은 import가 아님
    if line.strip().startswith("from "):
        # 실제 import문은 "from ... import ..." 패턴
        if not re.match(r'^from\s+\S+\s+import\s+', line):
            return True
    return False


def remove_imports_from_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()
    # 파일 내에 "from "으로 시작하지만 import가 아닌 라인이 있는지 확인
    has_non_import_from = any(is_non_import_from_line(line) for line in lines)
    if not has_non_import_from:
        return False  # 대상 아님
    # import문 제거
    new_lines = [
        line for line in lines
        if not (line.strip().startswith("import ") or re.match(r'^from\s+\S+\s+import\s+', line))
    ]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"[REMOVED IMPORTS] {filepath}")
    return True


# pk_external_tools 이하 전체 .py 파일에 대해 적용
d_working = Path("pk_external_tools")
for pyfile in d_working.rglob("*.py"):
    remove_imports_from_file(pyfile)
