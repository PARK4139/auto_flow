from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RemoteDeviceConfig:
    ip: str
    port: int
    user_n: str
    distro_name: str
    f_local_ssh_public_key: Path
    f_local_ssh_private_key: Path
    pw: Optional[str] = None

    def to_dict(self):
        # # TTL 캐시사용을 위해 필요
        # Convert Path objects to strings for JSON serialization
        return {
            "ip": self.ip,
            "port": self.port,
            "user_n": self.user_n,
            "distro_name": self.distro_name,
            "f_local_ssh_public_key": str(self.f_local_ssh_public_key),
            "f_local_ssh_private_key": str(self.f_local_ssh_private_key),
            "pw": self.pw,
        }
