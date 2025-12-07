import uuid
from pathlib import Path
from typing import Union


def get_n(pnx: Union[str, Path]) -> str:
    try:
        # 문자열화 → Path 변환 → 이름 추출
        path = Path(str(pnx))
        name = path.stem if path.suffix else path.name

        # 금지 문자가 있다면 오류 발생시켜 fallback 실행
        if any(c in name for c in '<>:"/\\|?*'):
            raise ValueError("invalid characters in filename")

        return name.strip() or f"unknown_{uuid.uuid4().hex[:8]}"
    except Exception:
        return f"unknown_{uuid.uuid4().hex[:8]}"
