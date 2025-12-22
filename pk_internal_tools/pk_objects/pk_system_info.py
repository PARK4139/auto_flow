import platform
import json
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PkSystemInfo:
    """
    PK 시스템의 플랫폼 정보를 저장하는 데이터 클래스입니다.
    """
    system: str
    node_name: str
    release: str
    version: str
    machine: str
    processor: str
    timestamp: str

    def to_json(self) -> str:
        """
        객체의 데이터를 표준 JSON 문자열로 변환합니다.
        """
        return json.dumps(asdict(self), ensure_ascii=False, indent=4)

def get_system_platform_info() -> PkSystemInfo:
    """
    현재 시스템의 플랫폼 정보를 수집하여 PkSystemInfo 객체로 반환합니다.
    """
    return PkSystemInfo(
        system=platform.system(),
        node_name=platform.node(),
        release=platform.release(),
        version=platform.version(),
        machine=platform.machine(),
        processor=platform.processor(),
        timestamp=datetime.now().isoformat()
    )
