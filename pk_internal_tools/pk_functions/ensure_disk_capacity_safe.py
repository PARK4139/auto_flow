from typing import Tuple, Dict

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_disk_capacity_safe(
        target_path: str = ".",
        danger_used_percent: float = 95.0,
) -> Tuple[bool, str, Dict[str, float]]:
    import os
    import shutil
    import logging

    # Resolve to an existing path to avoid surprises
    path = os.path.abspath(target_path if os.path.exists(target_path) else ".")
    total, used, free = shutil.disk_usage(path)

    total_gb = round(total / (1024 ** 3), 2)
    used_gb = round(used / (1024 ** 3), 2)
    free_gb = round(free / (1024 ** 3), 2)

    used_percent = round((used / total) * 100, 2) if total > 0 else 0.0
    free_percent = round(100 - used_percent, 2)

    metrics = {
        "total_gb": total_gb,
        "used_gb": used_gb,
        "free_gb": free_gb,
        "used_percent": used_percent,
        "free_percent": free_percent,
    }

    # Build guidance message (Korean), platform-aware tips included.
    base_info = (
        f"[디스크 상태] 총 {total_gb} GB, 사용 {used_gb} GB ({used_percent}%), "
        f"여유 {free_gb} GB ({free_percent}%). 기준 임계치: {danger_used_percent}% 사용"
    )

    if used_percent >= danger_used_percent:
        # Danger: advise to empty trash and warn not to proceed.
        os_name = os.name  # 'nt' for Windows, 'posix' for macOS/Linux
        if os_name == "nt":
            tip = "Windows: 휴지통(바탕화면)에서 '비우기'를 실행하거나, '설정 > 저장소'에서 임시 파일 정리를 수행하세요."
        else:
            tip = (
                "macOS/Linux: 파일 관리자에서 '휴지통 비우기'를 실행하거나, "
                "홈 디렉터리의 '.local/share/Trash' (배포판에 따라 경로 상이) 정리를 고려하세요."
            )
        message = (
            f"{base_info}\n"
            f"️ 사용량이 {danger_used_percent}% 이상입니다. 진행하였을때 사이드이펙트가 있을 수 있습니다.\n"
            f"Tip: {tip}"
        )
        logging.debug(message)
        return False, message, metrics
    else:
        message = f"{base_info}\n 현재 용량은 진행해도 무리가 없어 보입니다."
        logging.debug(message)
        return True, message, metrics
